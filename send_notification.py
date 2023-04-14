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


parser = argparse.ArgumentParser(
    description='Send notification if Too Good To Go items are available.')

parser.add_argument('-i', '--interval', type=int, default=60,
                    help='Interval in seconds between checks. Default is 60 seconds.')
parser.add_argument('-c', '--category', type=str, default=None,
                    help='Category to check. Default is every item category.')
parser.add_argument('-t', '--test', action='store_true',
                    help='Test the checkers without sending notification.')

args = parser.parse_args()


CREDTENIALS_PATH = os.getenv('CREDTENIALS_PATH') or 'credentials.json'
with open(CREDTENIALS_PATH, 'r') as openfile:
    credentials = json.load(openfile)

tgtg_client = TgtgClient(access_token=credentials['access_token'],
                         refresh_token=credentials['refresh_token'],
                         user_id=credentials['user_id'],
                         cookie=credentials['cookie'])


PUSHBULLET_TOKEN = os.getenv('PUSHBULLET_TOKEN')
if PUSHBULLET_TOKEN == None:
    print("PUSHBULLET_TOKEN not set")
    sys.exit()

pb = Pushbullet(PUSHBULLET_TOKEN)


print("Starting Too Good To Go notification script, press Ctrl+C to stop")
print(f"Checking for {'items' if args.category == None else args.category.capitalize()}...\n")

prev_available_items = dict()


def send_notification(items, category):
    title = "🛒 Too Good To Go - " + \
        "Item Watcher" if category == None else category.capitalize()

    for item in items:
        if item['items_available'] > 0:
            pb.push_link(title=title,
                         url=f"https://share.toogoodtogo.com/item/{item['item']['item_id']}",
                         body=f"{item['display_name']}: {item['items_available']} ")

    print("Notification sent")


error_count = 0

while True:
    try:
        print(datetime.now())

        if args.category == None:
            items = tgtg_client.get_items()
        else:
            items = tgtg_client.get_items(item_categories=[args.category])

        send_mail = False

        new_available_items = list()
        for item in items:
            item_id = item['item']['item_id']

            if item['items_available'] > 0 and \
                item_id in prev_available_items and \
                    item['items_available'] > prev_available_items[item_id]:
                new_available_items.append(item_id)

            prev_available_items[item_id] = item['items_available']

        if len(new_available_items) > 0 and not args.test:
            send_notification(items, args.category)

        print("----------------------------------")
        time.sleep(args.interval)

    except KeyboardInterrupt:
        print("Exiting...")
        break

    except Exception as e:
        print(e)
        if not args.test:
            pb.push_note("Too Good To Go - Error", str(e))

        error_count += 1
        if error_count >= 3:
            print("Too many errors, exiting...")
            break

        print(f"Retrying in {args.interval} seconds...")
        time.sleep(args.interval)

sys.exit()
