# Too Good To Go Notification Sender

A simple CLI tool, what can send notification to your phone if a favorite [Too Good To Go](https://toogoodtogo.com/) item becomes available.
The script talks with the [TooGoodToGo](https://toogoodtogo.com/) API via the [tgtg-python](https://github.com/ahivert/tgtg-python) client.

It can send notification to your phone via [Pushbullet](https://www.pushbullet.com/) or [Telegram](https://telegram.org/).

Python version: 3.7+

## Disclaimer

This Project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Too Good To Go, or any of its subsidiaries or its affiliates.

Too Good To Go explicitly forbids the usege of their platform the way this tool does if you use it. In their Terms and Conditions it says: "The Consumer must not misuse the Platform (including hacking or 'scraping')."

If you use this tool you do it at your own risk. Too Good To Go may stop you from doing so by (temporarily) blocking your access and may even delete your account.

## Install

1. Clone the repository and install requirements.

    ```bash
    git clone https://github.com/tallosim/too-good-to-go-notification.git
    cd too-good-to-go-notification
    pip install -r requirements.txt
    ```

2. Create [Too Good To Go](https://toogoodtogo.com/) Credentials.
    You should receive an email from *Too Good To Go*. It will wait until you validate the login by clicking the link inside the email.
    Once you clicked the link, you will get credentials and be able to use them

    ```bash
    python ctgtg-credtentials.py -e <YOUR_EMAIL@EXAMPLE.COM>
    ```

3. Add your credentials, API tokens and other settings to `.env` file. To get your Pushbullet token, you can follow the [How do I setup pushbullet notifications?](https://myspool.com/content/how-do-i-setup-pushbullet-notifications) guide. To get your Telegram token, you can follow the [Telegram: From BotFather to 'Hello World'](https://core.telegram.org/bots/tutorial) guide.

    ```conf
    # Too Good To Go Credentials - JSON base64 encoded
    TGTG_CREDENTIALS=<base64 encoded json>

    # Pushbullet credentials, chat id and device id
    PUSHBULLET_TOKEN=<token>
    PUSHBULLET_CHAT_ID=<chat id>
    PUSHBULLET_DEVICE_ID=<device id>

    # Telegram credentials and chat id
    TELEGRAM_TOKEN=<token>
    TELEGRAM_CHAT_ID=<chat id>
    ```

## Usage

If you want to run the script manually, you can do it with the following command:

```bash
python tgtg-notification.py
```

Or you can use the docker image:

```bash
docker run -d --name tgtg-notification \
    -e TGTG_CREDENTIALS=<base64_encoded_json> \
    -e PUSHBULLET_TOKEN=<token> \
    -e PUSHBULLET_CHAT_ID=<chat_id> \
    -e PUSHBULLET_DEVICE_ID=<device_id> \
    -e TELEGRAM_TOKEN=<token> \
    -e TELEGRAM_CHAT_ID=<chat_id> \
    tallosim/tgtg-notification
```

## TODO

In this version, by default it will **only** get your favorites Too Good To Go items. In the future, I would like to add an option where you can specify it.
