# -*- coding: utf-8 -*-
import json
import urllib.request
import os

def lambda_handler(event, context):
    deviceid = event['detail']['DeviceId']
    webhook_url = os.environ['DISCORD_WEBHOOK_URL']
    lon = event['detail']['Position'][0]
    lat = event['detail']['Position'][1]
    eventType = event['detail']['EventType']
    
    message = "%s、いってらっしゃい！" % deviceid
    
    if eventType == "ENTER":
        message = "%s、おかえりなさい！" % deviceid
    
    # Discordのwebhook用のペイロード
    payload = {
        "content": message
    }
    
    # HTTPリクエストの作成
    headers = {
        "Content-Type": "application/json"
    }
    
    data = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(webhook_url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            print(event)
            print(response_body)
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}")
        print(e.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }