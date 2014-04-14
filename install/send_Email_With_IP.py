#!/usr/bin/env python
"""Startup Script used to inform the new DHCP obtained Adress"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import smtplib
import socket

SERVER = "smtp.ist.utl.pt"

FROM = "Raspberry@tagus.ist.utl.pt"
TO = ["aliensgoo@Gmail.com"] # must be a list

SUBJECT = "My New IP"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
print(s.getsockname()[0])
TEXT = s.getsockname()[0]
s.close()
# Prepare actual message

message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

# Send the mail

server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, message)
server.quit()

