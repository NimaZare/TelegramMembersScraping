from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import sys
import csv
import random
import time

# Application Verson : 1.0
# Developer: Nima Zare
# Web : www.nimazare.net
 
api_id = YOUR_APP_ID
api_hash = 'YOUR_APP_API_HASH_CODE'
phone = '+981111111111'
client = TelegramClient(phone, api_id, api_hash)

SLEEP_TIME = 30
 
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))
 
input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)
 
mode = int(input("Enter 1 to send by user ID or 2 to send by username: "))
 
messages= ["سلام {} 😍 حالت چطوره؟", "سلام {}، خوبی حالت تنظیمه ؟ 😊", "سلاااام بر تو {} ، چه خبرا ؟ 😎"]
 
for user in users:
    if mode == 2:
        if user['username'] == "":
            continue
        receiver = client.get_input_entity(user['username'])
    elif mode == 1:
        receiver = InputPeerUser(user['id'],user['access_hash'])
    else:
        print("Invalid Mode. Exiting.")
        client.disconnect()
        sys.exit()
    message = random.choice(messages)
    try:
        print("Sending Message to:", user['name'])
        client.send_message(receiver, message.format(user['name']))
        print("Waiting {} seconds".format(SLEEP_TIME))
        time.sleep(SLEEP_TIME)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        client.disconnect()
        sys.exit()
    except Exception as e:
        print("Error:", e)
        print("Trying to continue...")
        continue

client.disconnect()
print("Done. Message sent to all users. [www.nimazare.net]")
