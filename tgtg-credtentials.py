import json
import base64
import argparse

from tgtg import TgtgClient


# Parse arguments
parser = argparse.ArgumentParser(description='Get credentials from Too Good To Go.')
parser.add_argument('-e', '--email', type=str, required=True, help='Email address to use for login.')
args = parser.parse_args()

# Get credentials from Too Good To Go
client = TgtgClient(email=args.email)
credentials = client.get_credentials()

# Encode credentials to base64
encoded_credentials = base64.b64encode(json.dumps(credentials).encode("utf-8")).decode("utf-8")

# Print encoded credentials
print("Copy the following line and paste it in your .env file. Make sure to set the TGTG_CREDTENIALS variable.")
print("----------------------------------")
print("TGTG_CREDENTIALS=" + encoded_credentials)
print("----------------------------------")
