#!/usr/bin/env python
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import urllib2
import json
import codecs
import os


# ****************************************************************************
# Author: Will Kent                                                          |
# GitHub: https://github.com/r3cursive123                                    |
# Description: This is a quick script that can be used with crontab to run   |
#              on a defined basis.                                           |
#              We will scan local network using arp-scan and match results   |
#              based on a defined list (allow_list)                          |
#              If MAC is not in our list we will send an email alert to the  |
#              user with MAC and company                                     |
#              Set to aggressive to enable an nmap scan of MAC address       |
#              Aggressive mode will save a file 'report.txt' to the local   |
#              directory and email it as an attachment                       |
# ****************************************************************************

# Email setup variables:
emailaddr = 'YOUR_EMAIL_ADDRESS'
emailpass = 'YOUR_EMAIL_PASSWORD'
smail = 'YOUR_SMTP'
sport = 'YOUR_SPORT'


# Is set to 0 - you will be notified of mac and vendor only
# If set to 1 - an nmap scan will be done on the target MAC address and a 
sent as an attachment
aggressive = 0


# Set frequency of scan using 'sudo crontab -e -u root'
# Then add this entry for every 5 minutes: */5 * * * * /absolute/path/to/arp_mon.py


# Check if we are running as root
if os.geteuid() != 0:
    print('You must run this script as root!!!')
    exit()

# Allowed MAC on network
# Example = ['11:22:33:44:55:66','77:88:99:10:11:12']
allow_list = []


# Website to lookup MAC info
url = "http://macvendors.co/api/"

# DEFINE FUNCTIONS
# Craft an email alert with MAC and vendor info
def send_alert(mac,result):
    fromaddr = emailaddr
    toaddr = emailaddr
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "New Device Alert!" # Change this if you want

    body = "A new device has been detected on your network MAC: " + mac + "Device: " + str(result)
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP(smail, sport) # Your email provider smtp settings
    server.starttls()
    server.login(fromaddr, emailpass) # Use environment variables for production use!!!
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def send_alert_aggressive(mac,result):
    fromaddr = emailaddr
    toaddr = emailaddr

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "New Device Alert!"

    body = "A new device has been detected on your network MAC: " + mac + "Device: " + str(result)

    msg.attach(MIMEText(body, 'plain'))

    filename = "report.txt"
    attachment = open("report.txt", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP(smail, sport) # Your email provider smtp settings
    server.starttls()
    server.login(fromaddr, emailpass) # Use environment variables for production use!!!
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# START PROGRAM
# Get MAC address listing
arp = subprocess.Popen(['sudo arp-scan --localnet | awk {\'print $2\'} | sed \'1,2d\' | head  -n  -3'],shell=True,stdout=subprocess.PIPE)

# Parse results and send email if necessary
mac = arp.stdout.readline()
while mac != '':
    if mac.rstrip() in allow_list:
        mac = arp.stdout.readline()
    else:
        mac_address = mac
        request = urllib2.Request(url + mac_address, headers={'User-Agent': "API Browser"})
        response = urllib2.urlopen(request)
        reader = codecs.getreader("utf-8")
        obj = json.load(reader(response))
        result = (obj['result']['company'] + "<br/>");
        if aggressive == 0:
            send_alert(mac,result)
            print('Alert Sent!')
            mac = arp.stdout.readline()
        else:
            command = ['sudo arp-scan --localnet | grep '+mac]
            scanner = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            ip = scanner.stdout.readline()[0:12].rstrip()
            os.system('nmap -A ' + ip + ' -oN report.txt >> /dev/null')
            send_alert_aggressive(mac,result)
            print('Alert Sent Aggressive!')
            mac = arp.stdout.readline()
