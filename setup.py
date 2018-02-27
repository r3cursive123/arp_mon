#!/usr/bin/env python
import os
import subprocess
from termcolor import colored

# Check if we are running as root
if os.geteuid() != 0:
    print('You must run this script as root!!!')
    exit()

# Check if arp-scan utility is installed on system
exist = subprocess.call('command -v ' + 'arp-scan ' + '>> /dev/null', shell=True)
if exist != 0:
    print('You do not have arp-scan installed!!!')
    answer = raw_input('Would you like us to install it? (Y/N)')
    if answer.lower() == 'y':
        os.system('sudo apt-get install arp-scan -y')
    elif answer.lower() == 'n':
        print colored('This program is required to run!!!','red')
        exit()
    else:
        print('Wrong answer dumbass...')
        exit()

# Check if nmap utility is installed on system (used for aggressive mode)
exist = subprocess.call('command -v ' + 'nmap ' + '>> /dev/null', shell=True)
if exist != 0:
    print('You do not have nmap installed!!!')
    answer = raw_input('Would you like us to install it? (Y/N)')
    if answer.lower() == 'y':
        os.system('sudo apt-get install nmap -y')
    elif answer.lower() == 'n':
        print colored('This program is required to run!!!','red')
        exit()
    else:
        print('Wrong answer dumbass...')
        exit()
os.system('clear')

# Ask for email settings
print('')
print colored(' ::: EMAIL SETTINGS :::','yellow')
email = raw_input(colored('Enter Email Address (user@email.com) >> ','red'))
pw = raw_input(colored('Enter email password >> ','red'))

# Write settings to main program
os.system('sed -i s/YOUR_EMAIL_ADDRESS/'+email+'/g arp_mon.py')
os.system('sed -i s/YOUR_EMAIL_PASSWORD/'+pw+'/g arp_mon.py')

# Let user know we did some shit...
print (colored('Updated arp_mon.py with custom email address settings!!','blue'))
print('')

# Ask for email server settings
print colored(' ::: EMAIL SERVER SETTINGS ::: ','yellow')
smail = raw_input(colored('Enter Email SMTP Server (smtp.gmail.com) >> ','red'))
sport = raw_input(colored('Enter SMTP Email Server Port (587) >> ','red'))

# Write SMTP settings
os.system('sed -i s/YOUR_SMTP/' + smail + '/g arp_mon.py')
os.system('sed -i s/YOUR_SPORT/' + sport + '/g arp_mon.py')

# Yeah...we did some shit again...
print(colored('Updated arp_mon.py with SMTP Server settings!!','blue'))
print('')
print('')
# Remind user not to fuck up :(
print('Remember to edit allow_list in main program (arp_mon.py)')
print('')
print('')
print('Set frequency of scan using :: ')
print colored('sudo crontab -e -u root','red')
print('')
print('Then add this entry for execution every 5 minutes :: ')
print colored('*/5 * * * * /absolute/path/to/arp_mon.py ','red')
print('')
print('')
print('')
print('')
print colored('(^)Picard Out(^)!!','yellow')
print('')
print('')
print('')
print('')
