# Superfeedr for Discord Webhook
## A rudimentary AWS lambda function for notifying your discord server when your Superfeedr feed updates

[![DeepSource](https://deepsource.io/gh/dylmye/superfeedr-discord.svg/?label=active+issues)](https://deepsource.io/gh/dylmye/superfeedr-discord/?ref=repository-badge) [![CodeQL](https://github.com/dylmye/superfeedr-discord/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/dylmye/superfeedr-discord/actions/workflows/codeql-analysis.yml)

This lambda function acts as a callback for a Superfeedr endpoint. Full instructions for usage will be in a blog post soon.

## Requirements

* Python 3.x
* Internet connection
* A Superfeedr account

## Install

To install dependencies in a manner ready for sending to AWS, run the following:
``` bash
$ pip install --target . -r requirements.txt
```

## Usage

This function is intended to run on AWS Lambda. See the blog post for more information.
Make sure to make a copy of env.example.py, rename it to env.py and fill out the required values:

* `DISCORD_WEBHOOK_URL`: the URL Discord provides for its channel webhook
* `DISCORD_ROLE_ID`: the ID of the role to @ in your message. Set this to 'everyone' if you want to @ everyone
