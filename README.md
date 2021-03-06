# telegram-bot
Telegram bot prototype for SberCloud.Advanced implemented as a FunctionGraph function.
It could be used as an alarm notification channel in case of some cloud resouce metric is violated.

### Description
Input:
- event: base64-encoded JSON structure, which triggered the function (Telegram message)
- context: security context

Output:
- HTTP status code 200

Recieves the ECS name as part of the "event" parameter.
If ECS with such name exists, the bot:
- gets ECS id and CPU Util metrics for last 8 hours from the CES service using security tokens from the "context" parameter
- makes a plot
- sends back the plot as a picture using Telegram API. 

Example picture: 

![alt Example of CPU Utilization metric](https://github.com/ippeter/telegram-bot/blob/main/stats_example.jpeg)

If ECS with such name doesn't exist, simply sends back the "ECS not found" message using Telegram API.

### Dependencies
1. Requires matplotlib
2. You have registered your bot and obtained the bot token

### Installation and Configuration
Just copy the code and paste it into FunctionGraph as a Python 3.6 function.
Requeres IAM agency with ECS Viewer and CES Viewer rights.
Expects bot token as the TOKEN environment variable.

Could be exposed via API Gateway service.
The API URL could be used to set up the bot webhook to send updates to.


