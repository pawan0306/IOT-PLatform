#!/usr/bin/env python3

import sys
from twilio.rest import Client


def sms(content='Notification Alert',receiver='8961803800'):
    account_sid = 'ACf04f42c1380680da1b54f2bb8e63e0b7'
    auth_token = '3c9cb62debc85d84556f6048fb3dfedd'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+18045910823', body=content, to='+91' + receiver)

    print(message.sid)

sms()