import os
import json
import base64
import time
import random
import asyncio
from dotenv import load_dotenv

from tgtg import TgtgClient
from pushbullet import Pushbullet
from telegram import Bot

load_dotenv()


# Initialize Too Good To Go client
TGTG_CREDENTIALS = os.getenv("TGTG_CREDENTIALS")
if TGTG_CREDENTIALS == None or TGTG_CREDENTIALS == "":
    print("TGTG_CREDTENIALS not set")
    exit(1)

try:
    tgtg_json = base64.b64decode(TGTG_CREDENTIALS).decode("utf-8")
    tgtg_credentials = json.loads(tgtg_json)
except:
    print("TGTG_CREDENTIALS is not a valid json")
    exit()

tgtg_client = TgtgClient(
    access_token=tgtg_credentials["access_token"],
    refresh_token=tgtg_credentials["refresh_token"],
    user_id=tgtg_credentials["user_id"],
    cookie=tgtg_credentials["cookie"],
)

# Initialize Pushbullet client
pushbullet_client = None
PUSHBULLET_TOKEN = os.getenv("PUSHBULLET_TOKEN")

if PUSHBULLET_TOKEN == None or PUSHBULLET_TOKEN == "":
    print("No Pushbullet token provided, Pushbullet notifications will not be sent")

else:
    PUSHBULLET_CHAT_ID = (
        os.getenv("PUSHBULLET_CHAT_ID")
        if os.getenv("PUSHBULLET_CHAT_ID") != ""
        else None
    )
    PUSHBULLET_DEVICE_ID = (
        os.getenv("PUSHBULLET_DEVICE_ID")
        if os.getenv("PUSHBULLET_DEVICE_ID") != ""
        else None
    )

    pushbullet_client = Pushbullet(PUSHBULLET_TOKEN)

# Initialize Telegram client
telegram_client = None
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if TELEGRAM_TOKEN == None or TELEGRAM_TOKEN == "":
    print("No Telegram token provided, Telegram notifications will not be sent")

elif TELEGRAM_CHAT_ID == None or TELEGRAM_CHAT_ID == "":
    print("No Telegram chat id provided, Telegram notifications will not be sent")

else:
    telegram_client = Bot(TELEGRAM_TOKEN)
    async_event_loop = asyncio.new_event_loop()


# Send telegram message
def send_telegram_message(title, message):
    async def telegram_message():
        await telegram_client.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=f"{title}\n{message}",
        )

    async_event_loop.run_until_complete(telegram_message())


# Send notification to Pushbullet and Telegram
def send_notification(title, message, link):
    if pushbullet_client != None:
        pushbullet_client.push_link(
            title=title,
            url=link,
            body=message,
            chat=PUSHBULLET_CHAT_ID,
            device=PUSHBULLET_DEVICE_ID,
        )

    if telegram_client != None:
        send_telegram_message(title, f"{message}\n{link}")


# Send message to Pushbullet and Telegram
def send_message(title, message):
    if pushbullet_client != None:
        pushbullet_client.push_note(
            title=title,
            body=message,
            chat=PUSHBULLET_CHAT_ID,
            device=PUSHBULLET_DEVICE_ID,
        )

    if telegram_client != None:
        send_telegram_message(title, message)


# Check if items are available
def check_items(prev_available_items, is_send_notification=True):
    # Get items
    items = tgtg_client.get_items()

    # Check if items are available
    available_items = list()
    for item in items:
        if item["items_available"] > 0:
            available_items.append(item)

    # Check if new items are available
    new_available_items = list()
    for item in available_items:
        item_id = item["item"]["item_id"]

        if item_id not in prev_available_items:
            new_available_items.append(item)

        elif item["items_available"] > prev_available_items[item_id]:
            new_available_items.append(item)

    # Send notification if new items are available
    if len(new_available_items) > 0 and is_send_notification:
        for item in new_available_items:
            item_url = f"https://share.toogoodtogo.com/item/{item['item']['item_id']}"
            notification_title = "🛒 Too Good To Go - Item Watcher"
            notification_message = f"{item['display_name']}: {item['items_available']}"

            send_notification(notification_title, notification_message, item_url)

            print("Item found", notification_message)

    # If no items are available
    if len(new_available_items) == 0:
        print("No new items found")

    # Update previous available items
    prev_available_items.clear()
    for item in available_items:
        prev_available_items[item["item"]["item_id"]] = item["items_available"]


if __name__ == "__main__":
    print("Starting Too Good To Go notification script")
    print("----------------------------------")

    # Create dictionary for previous available items
    prev_available_items = dict()

    # Send message to Pushbullet and Telegram
    send_message("🛒 Too Good To Go - Item Watcher", "The Item Watcher has started.")

    # Create error counter
    error_count = 0

    # Check if items are available every 30 seconds
    while True:
        try:
            print("Checking for items...")

            # Check if items are available
            check_items(prev_available_items, True)

            # Reset error counter
            error_count = 0

            # Wait 30 seconds plus a random number of seconds between 0 and 5 seconds
            sleep_time = 30 + random.uniform(0, 5)
            print(f"Waiting {sleep_time:.2f} seconds...\n")
            time.sleep(sleep_time)

        except KeyboardInterrupt:
            print("Keyboard interrupt detected, stopping script")

            # Send message to Pushbullet and Telegram
            send_message(
                "🛒 Too Good To Go - Item Watcher",
                "The Item Watcher has stopped by the user.",
            )

            exit()

        except Exception as e:
            print(f"An error occured: {e}\n")

            # Increase error counter
            error_count += 1

            # Send message to Pushbullet and Telegram
            send_message(
                "🛒 Too Good To Go - Item Watcher",
                f"An error occured: {e}\n\nError count: {error_count}",
            )

            # Stop script if error count is 5
            if error_count == 5:
                print("Error count is 5, stopping script")

                # Send message to Pushbullet and Telegram
                send_message(
                    "🛒 Too Good To Go - Item Watcher",
                    "The Item Watcher has stopped because the error count is 5.",
                )

                exit(1)

            # Wait 60 seconds
            print("Waiting 60 seconds...\n")
            time.sleep(60)
