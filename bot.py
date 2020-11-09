# -*- coding:utf-8 -*-
import json, base64, requests, os
import matplotlib.pyplot as plt

from PIL import Image
from datetime import datetime


def handler(event, context):    
    # Decode request body and convert to dict
    body = json.loads(base64.b64decode(event["body"]).decode("utf-8"))
    host_name = body["message"]["text"]

    # Get security token and project id from the security context, as well as get Telegram bot token 
    sb_token = context.getToken()
    project_id = context.getProjectID() 
    tg_token = os.environ["TOKEN"]

    # Build Header and Body of the GET requests to SberCloud.Advanced API
    hdr = {'Content-Type': 'application/json;charset=utf8', 'X-Auth-Token': sb_token}

    #
    # Do GET request to get host_id by host_name
    #
    resp = requests.get(f"https://ecs.ru-moscow-1.hc.sbercloud.ru/v1/{project_id}/cloudservers/detail", headers=hdr)
    servers = resp.json().get("servers")

    host_id = ""
    for server in servers:
        if (server["name"] == host_name):
            host_id = server["id"] 
            break

    if (host_id == ""):
        # Prepare the request to Telegram
        data = {
            "chat_id": body["message"]["chat"]["id"], 
            "text": "<b>ECS with such name was not found!</b>",
            "parse_mode": "HTML",
            "reply_to_message_id" : body["message"]["message_id"]
        }

        resp = requests.post(f"https://api.telegram.org/bot{tg_token}/sendMessage", data=data)

        print(f"ECS with name of {host_name} was not found.")

        # Prepare the output
        result = {}
        result["headers"] = {"Content-Type": "application/json"}
        result["statusCode"] = 200

        return result

    # Prepare timestamps
    time_to = int(datetime.now().timestamp()) * 1000
    time_from = time_to - 8 * 3600 * 1000

    #
    # Do GET request to get CPU Util metric
    #
    resp = requests.get(f"https://ces.ru-moscow-1.hc.sbercloud.ru/V1.0/{project_id}/metric-data?namespace=SYS.ECS&metric_name=cpu_util&dim.0=instance_id,{host_id}&from={time_from}&to={time_to}&period=300&filter=max", headers=hdr)

    # Prepare data points for the plot
    datapoints = [item["max"] for item in resp.json().get("datapoints")]
    timestamps = [datetime.strftime(datetime.fromtimestamp(item["timestamp"] / 1000), "%H:%M") for item in resp.json().get("datapoints")]

    # Draw virtual plot
    fig, ax = plt.subplots()
    ax.plot(timestamps, datapoints)
    ax.set(xlabel='Time', ylabel='CPU Util, %', title=f"ECS {host_name} CPU Load for last 8 hours")

    # Decrease the number of ticks on the X axis
    timestamps_ticks = []

    for idx, item in enumerate(timestamps[::-1]):
        if (idx % 10 == 0):
            timestamps_ticks.append(timestamps[::-1][idx])
            
    timestamps_ticks = timestamps_ticks[::-1]

    plt.xticks(timestamps_ticks)
    
    # Convert plot to PNG image
    plt.savefig("/tmp/stats.png", format='png')

    # Prepare the request to Telegram
    data = {
        "chat_id": body["message"]["chat"]["id"], 
        "caption": f"CPU Util for host {host_name}",
        "reply_to_message_id" : body["message"]["message_id"]
    }
        
    #
    # Do POST request to Telegram API
    #
    with open("/tmp/stats.png", "rb") as image_file:
        resp = requests.post(f"https://api.telegram.org/bot{tg_token}/sendPhoto", data=data, files={"photo": image_file})

    print(f"Function completed with code {resp.status_code}")

    # Prepare the output
    result = {}
    result["headers"] = {"Content-Type": "application/json"}
    result["statusCode"] = 200

    return result
