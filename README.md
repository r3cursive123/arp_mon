# arp_mon

Description: This script/program leverages arp-scan and nmap to profile your internal network and determine if there is a MAC address that should not belong (according to an 'allow_list')! 
If MAC address should not belong then an email notification is generated. 
If you are in aggressive mode,  the program will try to invoke 'nmap' to get more detail and email this as an attachment - 
otherwise - it will just send an email with MAC address and manufacturer.

Dependencies: arp-scan, nmap

Should be run on linux or raspberry pi

Install:
1. git clone https://github.com/r3cursive123/arp_mon.git
2. sudo chmod +x setup.py
3. sudo python setup.py
4. Anwser questions (this will setup configurations for later...if you are un-easy about it - then just edit arp_mon.py yourself)
5. Make sure you add this program to your crontab -- else it will not run! 
