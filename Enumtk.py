#!/usr/bin/python
import os, sys, re
from termcolor import colored, cprint

# Function for creating the Menu Title
def createMenuTitle(menuName):
    menuName = menuName.center(40, " ")

    print("----------------------------------------")
    print(menuName)
    print("----------------------------------------")

# Function for creating the Menu Item List
def createMenuList(menuItems):
    i = 0

    for x in menuItems:
        i+=1
        print(f"[{i}] " + x)
    print("\nSelect from menu above: ")

# Function for input validation for IP with CIDR notation
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

# Function for the Main Menu
def mainMenu():
    while (1):
        #Script Header
        print(colored("""
        ███████ ███    ██ ██    ██ ███    ███ ████████ ██   ██ 
        ██      ████   ██ ██    ██ ████  ████    ██    ██  ██  
        █████   ██ ██  ██ ██    ██ ██ ████ ██    ██    █████   
        ██      ██  ██ ██ ██    ██ ██  ██  ██    ██    ██  ██  
        ███████ ██   ████  ██████  ██      ██    ██    ██   ██  
                                                                        
                                                                        """, 'red', attrs=['blink']))

        #Menu Title
        createMenuTitle("Main Menu")

        #Menu Display
        createMenuList(["Nmap General", "Nmap Protocol Specific", "Exit"])

        # Menu Selection
        x = input()

        # Nmap General Conditional
        if x == '1':
            nmapMenu()

        # Nmap Protocol Specific
        elif x == '2':
            print("")

        elif x == '3':
            break

        else:
            print("Invalid selection, please try again.")
            continue

# Function for the Nmap General Menu
def nmapMenu():
    #Menu Title
    createMenuTitle("Nmap General Menu")

    #Menu Display
    createMenuList(["Nmap Ping Sweep", "Nmap Service Scan", "Nmap All Scan", "Exit"])

    while (1):

        # Menu Selection
        x = input()

        # Ping Sweep Conditional
        if x == '1':
            ipScope = input("\nEnter the scope: (Example: 192.168.1.1/24)\n")
            if validIp(ipScope):
                os.system(f"nmap -sn {ipScope}")
                break
            else:
                print("\nInvalid IP address format. Please enter a valid IP address in CIDR notation.")
                continue

        # Service Scan Conditional
        elif x == '2':
            scanIP = input("\nEnter the IP: " )
            scanPort = input("\nEnter the ports you would like scanned: ")
            os.system(f"nmap -sV -p {scanPort} {scanIP}")
            break
            
        # All Scan Conditional
        elif x == '3':
            scanIP = input("\nEnter the IP: " )
            scanPort = input("\nEnter the ports you would like scanned: ")
            os.system(f"nmap -A -p {scanPort} {scanIP}")
            break

        elif x == '4':
            break

        else:
            print("Invalid selection, please try again.")
            continue

mainMenu()