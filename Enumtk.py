#!/usr/bin/python
import os, sys, re
from termcolor import colored, cprint

def validIp(scope):
    # Input validation for IP address
    pattern = r'^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]{1,2})?$'
    if not re.match(pattern, scope):
        return False
    ip, cidr = scope.split('/') if '/' in scope else (scope, '32')
    parts = ip.split('.')
    if all(0 <= int(part) <= 255 for part in parts) and 0 <= int(cidr) <= 32:
        return True
    return False

while (1):
    #Script Header
    print(colored("""
███████ ███    ██ ██    ██ ███    ███ ████████ ██   ██ 
██      ████   ██ ██    ██ ████  ████    ██    ██  ██  
█████   ██ ██  ██ ██    ██ ██ ████ ██    ██    █████   
██      ██  ██ ██ ██    ██ ██  ██  ██    ██    ██  ██  
███████ ██   ████  ██████  ██      ██    ██    ██   ██  
                                                                
                                                                """, 'red', attrs=['blink']))

    #Menu Display
    print(colored("[1] ", 'cyan') + "Run NMAP to conduct a ping sweep.")
    print(colored("[2] ", 'cyan') + "Run NMAP Service Scan")
    print(colored("[3] ", 'cyan') + "Run NMAP All Scan")
    print(colored("[4] ", 'cyan') + "Exit")
    print("")
    print("Select from menu above: ")

    # Menu Selection
    x = input()

    # Ping Sweep Conditional
    if x == '1':
        print("")
        ipScope = input("Enter the scope: (Example: 192.168.1.1/24)\n")
        if validIp(ipScope):
            os.system(f"nmap -sn {ipScope}")
        else:
            print("Invalid IP address format. Please enter a valid IP address in CIDR notation.")
            continue

        break

    # Service Scan Conditional
    elif x == '2':
        print("")
        scanIP = input("Enter the IP: " )
        scanPort = input("Enter the ports you would like scanned: ")
        os.system(f"nmap -sV -p {scanPort} {scanIP}")
        break
        
    # All Scan Conditional
    elif x == '3':
        print("")
        scanIP = input("Enter the IP: " )
        scanPort = input("Enter the ports you would like scanned: ")
        os.system(f"nmap -A -p {scanPort} {scanIP}")
        break

    elif x == '4':
        break

    else:
        print("Invalid selection, please try again.")
        continue
