#!/usr/bin/python
import os, sys, re
from termcolor import colored, cprint

# Function for creating the Menu Title
def createMenuTitle(menuName):
    menuName = menuName.center(40, " ")

    #Script Header
    os.system("clear")

    print(colored("""
███████ ███    ██ ██    ██ ███    ███ ████████ ██   ██ 
██      ████   ██ ██    ██ ████  ████    ██    ██  ██  
█████   ██ ██  ██ ██    ██ ██ ████ ██    ██    █████   
██      ██  ██ ██ ██    ██ ██  ██  ██    ██    ██  ██  
███████ ██   ████  ██████  ██      ██    ██    ██   ██  
        """, 'light_magenta', attrs=['bold']))

    print(colored("----------------------------------------", 'light_green', attrs=['bold']))
    print(colored(menuName, 'light_green', attrs=['bold']))
    print(colored("----------------------------------------", 'light_green', attrs=['bold']))

# Function for creating the Menu Item List
def createMenuList(menuItems):
    i = 0
    print("")

    for x in menuItems:
        i+=1
        print(colored(f"[{i}] ", 'light_cyan') + x)

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

        #Menu Title
        createMenuTitle("Main Menu")

        #Menu Display
        createMenuList(["Nmap General", "Nmap Protocol Specific", "Exit"])

        # Menu Selection
        x = input("\nSelect from menu above: ")

        # Nmap General Conditional
        if x == '1':
            nmapMenu()

        # Nmap Protocol Specific
        elif x == '2':
            print("In-Development")

        elif x == '3':
            break

        else:
            input(colored("Invalid selection, please press enter.", 'red', attrs=['bold']))
            continue

# Function for the Nmap General Menu
def nmapMenu():
    while (1):

        #Menu Title
        createMenuTitle("Nmap General Menu")

        #Menu Display
        createMenuList(["Nmap Discovery Scan (-sn)", "Nmap Syn-Stealth Scan (-sS)", "Nmap All Scan (-A)", "Go Back"])

        # Menu Selection
        x = input("\nSelect from menu above: ")

        # Nmap Discovery Scan
        if x == '1':

            # Loop until a valid IP is entered
            while True:
                ipScope = input("\nEnter the scope: (Example: 192.168.1.1/24) ")
                if validIp(ipScope):
                    break
                else:
                    print("\nInvalid IP address format. Please enter a valid IP address in CIDR notation.")

            saveOption = input("\nWould you like to save the results? (Y/N): ")

            #Saved Discovery Scan
            if (saveOption == 'y' or saveOption == 'Y'):
                scanInterface = input("\nEnter the network interface name: (Example: eth0, wlan0) ")

                #Runs Discovery Scan
                aliveHosts = os.system(f"nmap -sn {ipScope} -e {scanInterface} | grep 'Nmap scan' | cut -d ' ' -f 5 > ./discoveryScan.txt")
                savePath = os.popen(f"pwd").read()
                input(f"\nFile was saved in {savePath}/discoveryScan.txt\n\nPress Enter to Cotinue:")
                #Print statement for testing
                #print("Correct if y is chosen and IP is correct")
                break
            
            #Unsaved Discovery Scan
            elif (saveOption == 'n' or saveOption == 'N'):
                scanInterface = input("\nEnter the network interface name: (Example: eth0, wlan0) ")
                os.system(f"nmap -sn {ipScope} -e {scanInterface}")
                #Print statement for testing
                #print("Correct Unsaved discovery scan")
                break

            #Invalid Save Option Input 
            else:
                input(colored("\nInvalid Input, please press enter.", 'red', attrs=['bold']))
                continue
            
        # Syn Stealth Scan Conditional
        elif x == '2':
            importIP = input("\nWould you like to import an IP list? (Y/N) ")
            
            # Imported IP List Syn Stealth Scan
            if (importIP == 'y' or importIP == 'Y'):

                # Prompts and saves the path
                listPath = input("\nEnter the path of your list: ")

                # Saves the contents of the list
                scanIPList = os.popen(f"cat {listPath}").read()

                # Displays all the IPs that will be scanned
                input(f"{scanIPList}\nThe above IPs will be scanned, press enter to continue: ")

                # Asks for the port numbers to be scanned
                scanPort = input("\nEnter the ports you would like scanned: ")
                
                # Interface Input
                scanInterface = input("\nEnter the network interface name: (Example: eth0, wlan0) ")

                # Iterates through all the IPs in the list and scans
                with open(f"{listPath}", "r") as file:
                    for line in file:
                        ip = line.strip()
                        if ip:
                            os.system(f"sudo nmap -sS -p {scanPort} {ip} -e {scanInterface}")
                break

            # Singular IP Syn Stealth Scan
            elif (importIP == 'n' or importIP == 'N'):
                scanIP = input("\nEnter the IP: ")
                scanPort = input("\nEnter the ports you would like scanned: ")
                os.system(f"nmap -sV -p {scanPort} {scanIP}")
                #Print statement for testing
                #print("os.system(fnmap -A -p ")
                break
            
        # All Scan Conditional
        elif x == '3':
            scanIP = input("\nEnter the IP: " )
            scanPort = input("\nEnter the ports you would like scanned: ")
            os.system(f"nmap -A -p {scanPort} {scanIP}")
            #Print statement for testing
            #print("os.systemnmap -A -p scanPort scanIP")
            break

        elif x == '4':
            break

        else:
            input(colored("Invalid selection, please press enter.", 'red', attrs=['bold']))
            continue

mainMenu()