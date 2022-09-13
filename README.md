# Too Good To Go Notification Sender

A simple CLI tool, what can send notification to your phone if a favorite [Too Good To Go](https://toogoodtogo.com/) item becomes available.
The script talks with the [TooGoodToGo](https://toogoodtogo.com/) API via the [tgtg-python](https://github.com/ahivert/tgtg-python) client.

Python version: 3.7+

## Install

1. Clone the repository and install requirements.

    ```bash
    git clone https://github.com/tallosim/too-good-to-go-notification.git
    pip install -r requirements.txt
    ```

2. Create [Too Good To Go](https://toogoodtogo.com/) Credentials.
    You should receive an email from *Too Good To Go*. The will wait until you validate the login by clicking the link inside the email.
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
usage: send_notification.py [-h] [-i INTERVAL] [-t] [-c CATEGORY]

Send notification if Too Good To Go items are available.

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        Interval in seconds between checks. Default is 10 seconds.
  -t, --test            Test notification.
  -c CATEGORY, --category CATEGORY
                        Category to check. Default is GROCERIES
```

## TODO

In this version, by default it will **only** get your favorites Too Good To Go items. In the future, I would like to add an option where you can specify it.
