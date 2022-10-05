from data_manager import *
import os
from email_manager import SendMail

# ----------# SHEETY INFO #-------------------------#
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_PROJECT = os.environ.get("SHEETY_PROJECT")
SHEETY_SHEET = os.environ.get("SHEETY_SHEET")
TEQUILA_API = os.environ.get("TEQUILA_API")

# ----------# EMAIL INFO #-------------------------#

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASS = os.environ.get("MY_PASS")

# ----------# EMAIL RECEIVERS #-------------------------#
receiver_list = ["nathanflores887@gmail.com", ]

flight_checker = DataManager(SHEETY_TOKEN, SHEETY_PROJECT, SHEETY_SHEET, TEQUILA_API)
flight_checker.update_codes()
flight_checker.search_flights()

subject = "Affordable plane tickets!"
body = "Here are the available flights that are in your budget!\n\n"

for item in flight_checker.can_buy:
    body += f"Plane ticket going to {item[0]} available for {item[1]} PHP only!\nlink: {item[2]}\n\n"

email_sender = SendMail(MY_EMAIL, MY_PASS, subject, body)

for recipient in receiver_list:
    email_sender.send_email(recipient)
