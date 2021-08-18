import json
import requests
import base64
from bs4 import BeautifulSoup, Tag

from env import DISCORD_WEBHOOK_URL, DISCORD_ROLE_ID

def lambda_handler(event, context):
    return_obj = {
        "statusCode": 200,
        "body": json.dumps({ "executed": False, "rqid": context.aws_request_id })
    }

    soup = BeautifulSoup(event["body"])
    entry = soup.entry

    if not entry:
        return_obj["body"] = json.dumps({ "executed": False, "rqid": context.aws_request_id, "error": "No entry found" })
        return return_obj

    title = entry.title
    link = entry.find("link", rel="alternate")
    channel = entry.author.id

    return_obj["body"] = json.dumps({ "executed": False, "rqid": context.aws_request_id, "title": title.string })

    mention_str = ('@....everyone, ' if DISCORD_ROLE_ID == 'everyone' else '<@&' + DISCORD_ROLE_ID + '>, ')

    data = {
        "content": "Hey " + mention_str + "**" + channel.string + "** just uploaded a video! Check out '" + title.string + "' here:\n" + link.get("href")
    }

    result = requests.post(DISCORD_WEBHOOK_URL, json = data)
    result.raise_for_status()

    return return_obj
