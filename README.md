# Too Good To Go Notification Sender

A simple CLI tool, what can send notification to your phone if a favorite [Too Good To Go](https://toogoodtogo.com/) item becomes available.
The script talks with the [TooGoodToGo](https://toogoodtogo.com/) API via the [tgtg-python](https://github.com/ahivert/tgtg-python) client.

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
    python create_credtentials.py -e <YOUR_EMAIL@EXAMPLE.COM>
    ```

3. Get your [Pushbullet](https://www.pushbullet.com/) token and put into `.env` file.
    [How do I setup pushbullet notifications?](https://myspool.com/content/how-do-i-setup-pushbullet-notifications)
  
    ```env
    PUSHBULLET_TOKEN = "<YOUR_TOKEN>"
    ```

## Usage

```text
usage: send_notification.py [-h] [-i INTERVAL] [-c CATEGORY] [-t]

Send notification if Too Good To Go items are available.

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        Interval in seconds between checks. Default is 60 seconds.
  -c CATEGORY, --category CATEGORY
                        Category to check. Default is every item category.
  -t, --test            Test the checkers without sending notification.
```

## TODO

In this version, by default it will **only** get your favorites Too Good To Go items. In the future, I would like to add an option where you can specify it.
