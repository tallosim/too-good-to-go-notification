from tgtg import TgtgClient
import json
import os
import sys
from dotenv import load_dotenv
import argparse

load_dotenv()

parser = argparse.ArgumentParser(description='Get credentials from Too Good To Go.')

parser.add_argument('-e', '--email', type=str, help='Email address to use for login.')

args = parser.parse_args()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS') or args.email
if EMAIL_ADDRESS == None:
    print("EMAIL_ADDRESS not set")
    sys.exit(1)

client = TgtgClient(email=EMAIL_ADDRESS)
credentials = client.get_credentials()


CREDTENIALS_PATH = os.getenv('CREDTENIALS_PATH') or 'credentials.json'

json_object = json.dumps(credentials, indent=4)
with open(CREDTENIALS_PATH, 'w') as outfile:
    outfile.write(json_object)
