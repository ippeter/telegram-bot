# telegram-bot
Telegram bot example for SberCloud.Advanced

### Description
Input:
- event: base64-encoded JSON structure, which triggered the function (Telegram message)
- context: security context
Output:
- HTTP status code 200

Recieves the ECS name as part of the "event" parameter.
If ECS with such name exists, the bot gets CPU Util metrics for last 8 hours from the CES service, makes a plot and sends back the plot as a picture using Telegram API.
If ECS with such name doesn't exist, simply sends back the "ECS not found" message using Telegram API.

Gets ECS name and corresponding CES metrics using security tokens from the "context" parameter.

### Dependencies
Requires matplotlib

### Installation and Configuration
Requeres IAM agency with ECS Viewer and CES Viewer rights.

Could be exposed via API Gateway service.
The API URL could be used to set up the bot webhook to send updates to.

Expects bot token as the TOKEN environment variable.
