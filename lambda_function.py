import json
import requests
from env import DISCORD_WEBHOOK_URL, DISCORD_ROLE_ID

# take a twitch event and publish a discord message
def lambda_handler(event, context):
    return_obj = {
        "statusCode": 200,
        "body": json.dumps({ "executed": False, "rqid": context["aws_request_id"] })
    }

    # handle different data shape when using
    # aws api gateway vs directly using lambda
    data = event
    if ("stageVariables" in data):
        data = json.loads(event["body"])

    if ("subscription" not in data or data["subscription"]["status"] != "enabled" or data["subscription"]["type"] != "stream.online"):
        return_obj["body"] = json.dumps({ "executed": False, "error": "no subscription in request, or subscription type is incorrect.", "debug_event_obj": data, "rqid": context["aws_request_id"] })
        return return_obj

    mention_str = ('@everyone, ' if DISCORD_ROLE_ID == 'everyone' else '<@&' + DISCORD_ROLE_ID + '>, ')
    # cache_buster = str(datetime.utcnow().isoformat(timespec='minutes')).replace('-', '').replace(':', '')

    data = {
        "content": mention_str,
        # "embeds": [
        #     {
        #         "author": {
        #             "name": TWITCH_USERNAME,
        #             "url": "https://twitch.tv/" + TWITCH_USERNAME,
        #             "icon_url": "https://avatar.glue-bot.xyz/twitch/" + TWITCH_USERNAME
        #         },
        #         "image": {
        #             "url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_" + TWITCH_USERNAME + "-720x480.jpg?cache=" + cache_buster
        #         },
        #         "footer": {
        #             "text": "https://twitch.tv/" + TWITCH_USERNAME,
        #             "icon_url": "https://i.imgur.com/p4CqTrc.png"
        #         },
        #         "color": 8521140
        #     }
        # ]
    }

    result = requests.post(DISCORD_WEBHOOK_URL, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return_obj["body"] = json.dumps({ "executed": False, "error": "discord webhook returned an error. " + err, "rqid": context["aws_request_id"] })
    else:
        return_obj["body"] = json.dumps({ "executed": True, "rqid": context["aws_request_id"] })

    return return_obj
