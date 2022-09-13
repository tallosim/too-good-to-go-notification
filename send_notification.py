from itertools import count
from turtle import pen
from tgtg import TgtgClient
from pushbullet import Pushbullet
import json
import time
from datetime import datetime
import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()


parser = argparse.ArgumentParser(description='Send notification if Too Good To Go items are available.')

parser.add_argument('-i', '--interval', type=int, default=10, help='Interval in seconds between checks. Default is 10 seconds.')
parser.add_argument('-t', '--test', action='store_true', help='Test notification.')
parser.add_argument('-c', '--category', type=str, default="GROCERIES", help='Category to check. Default is GROCERIES.')

args = parser.parse_args()


CREDTENIALS_PATH = os.getenv('CREDTENIALS_PATH') or 'credentials.json'
with open(CREDTENIALS_PATH, 'r') as openfile:
    credentials = json.load(openfile)

tgtg_client = TgtgClient(access_token=credentials['access_token'],
                    refresh_token=credentials['refresh_token'], user_id=credentials['user_id'])


PUSHBULLET_TOKEN = os.getenv('PUSHBULLET_TOKEN')
if PUSHBULLET_TOKEN == None:
    print("PUSHBULLET_TOKEN not set")
    sys.exit()

pb = Pushbullet(PUSHBULLET_TOKEN)


print("Starting Too Good To Go notification script, press Ctrl+C to stop")
print(f"Checking for {args.category.capitalize()}...")
print()

prev_available_items = dict()


def send_notification(items, category):
    title = "Too Good To Go - " + category.capitalize()
    rows = list()

    for item in items:
        if item['items_available'] > 0:
            rows.append(f"{item['display_name']} | {item['items_available']}")
    
    if len(rows) == 0:
        return
    
    if not args.test:
        pb.push_note(title, "\n".join(rows))

    print("Notification sent")


try:
    while True:
        print(datetime.now())
        
        items = tgtg_client.get_items(item_categories=[args.category])

        send_mail = False

        for item in items:        
            if item['items_available'] > 0:
                if item['item']['item_id'] not in prev_available_items:
                    send_mail = True
                elif prev_available_items[item['item']['item_id']] == 0:
                    send_mail = True
                    
                print(f"{item['display_name']} | {item['items_available']}")
                
            prev_available_items[item['item']['item_id']] = item['items_available']
        
        if send_mail:
            send_notification(items, args.category)
        
        print("--------------------")
        time.sleep(args.interval)

except KeyboardInterrupt:
    print("Exiting...")
