#!/usr/bin/env python3

import smtplib

from email.message import EmailMessage

def sendToAddress(content,subject='IAS notification',sender='ias.platform5@gmail.com',receiver='ronitray95@gmail.com'):
	
	# msg = EmailMessage()
	# msg.set_content(content)

	# msg['Subject'] = subject
	# msg['From'] = sender
	# msg['To'] = receiver

	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls() 
	s.login('ias.platform5@gmail.com','iasplat1@5') 
	s.sendmail(sender, receiver, content)
	# s.send_message(msg)
	s.quit()
