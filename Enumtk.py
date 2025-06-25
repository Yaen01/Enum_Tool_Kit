#!/usr/bin/env python3
import cmd
import os
import re
from termcolor import colored
from colorama import init, Fore, Style

# Banner
def show_banner():
    os.system("clear")
    init()
    ascii_art = """
    .-''-.  ,---.   .--.  ----  -- ,---.    ,---.,---------. .--.   .--.   
  .'_ _   \\ |    \\  |  |.'   /  | ||    \\  /    |\\          \\|  | _/  /    
 / ( ` )   '|  ,  \\ |  ||   |   | ||  ,  \\/  ,  | '--.  ,---'| (`` ) /     
. (_ o _)  ||  |\\_ \\|  ||   |   | ||  |\\_   /|  |    |   \\   |(_ ()_)      
|  (_`_)---||  |( )_\\  ||   |_ _| ||  |( )_/ |  |    :_ _:   | (_;_)   ---  
'  \\   .---.| (_ o _)  ||   ( v ) || (_ o _) |  |    (_v_)   |  |\\ \\  |  | 
 \\  '-'    /|  (_;_)\  ||  (_ O _)||  (_^_)  |  |   (_ O _)  |  | \\  '   / 
  \\       / |  |    |  |\\   ( ; ) /|  |      |  |    (_^_)   |  |  \\    /  
   \'-..-'   '--'    '--' ''-----'' '--'      '--'    '---'   '--'   ''-'   
"""

# Characters to color as "flower art"
    flower_chars = set("()_*oO`v^=;")

    for line in ascii_art.splitlines():
        colored_line = ''.join(
            Fore.MAGENTA + char + Style.RESET_ALL if char in flower_chars else char
            for char in line
    )
        print(colored_line)
    print(colored("------------- Enumeration Toolkit -------------", 'light_green', attrs=['bold']))

# IP validation with optional CIDR notation
def validIp(scope):
    pattern = r'^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]{1,2})?$'
    if not re.match(pattern, scope):
        return False
    ip, cidr = scope.split('/') if '/' in scope else (scope, '32')
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts) and 0 <= int(cidr) <= 32

#---------------------
# Main Shell Class
#---------------------
class EnumShell(cmd.Cmd):
    prompt = colored("enumtk> ", "green")

    def __init__(self):
        super().__init__()
        self.module = None # Current loaded module name
        self.options = {}  # Display current options 

    # Define module-specific options
    def load_module(self, module):
        self.module = module
        if module == "nmap":
            self.options = {
                "SCAN": {"value": "", "required": True, "desc": "Scan type (discovery, stealth, all)"},
                "RHOST": {"value": "", "required": True, "desc": "Target IP"},
                "PORTS": {"value": "1-1000", "required": False, "desc": "Ports to scan"},
                "INTERFACE": {"value": "eth0", "required": False, "desc": "Interface to use"},
                "MISC": {"value": "", "required": False, "desc": "Whatever Torres wants here"},
                "SAVE": {"value": "false", "required": False, "desc": "Save output (false/txt/xml/gnmap/nmap/all)"},
            }
        elif module == "nmap_protocol":
            self.options = {
                "RHOST": {"value": "", "required": True, "desc": "Target IP"},
                "PROTOCOL": {"value": "ftp", "required": True, "desc": "Protocol to scan (ftp/http/smtp)"},
            }

    # Initial menu input handler for modules
    def precmd(self, line):
        if not self.module:
            if line == "1":
                self.load_module("nmap")
                print(colored(">> Loaded nmap", "green"))
                self.do_show("options")
                return ""
            elif line == "2":
                self.load_module("nmap_protocol")
                print(colored(">> Loaded module nmap_protocol", "green"))
                self.do_show("options")
                return ""
            elif line == "3":
                return "exit"
            else:
                print(colored("Invalid selection. Type 1, 2, or 3.", "red"))
                return ""
        return line

    # Shows current module options and available modules
    def do_show(self, arg):
        "Show options, modules, or command"
        arg = arg.strip()
        if arg.strip() == "options":
            if not self.options:
                print(colored("No module loaded.", "red"))
                return
            print(f"\nOptions for module: {self.module}\n")
            print(f"{'Name':<12} {'Value':<20} Description")
            print("-" * 50)
            for key, meta in self.options.items():
                print(f"{key:<12} {meta['value']:<20} {meta['desc']}")
        elif arg == "modules":
            print("\nModules:\n  nmap\n  nmap_protocol\n")
        elif arg == "command":
            self.show_command_preview()
        else:
            print("Usage: show options | show modules | show command")

    # Tab completion (We can add more, just testing)
    def complete_show(self, text, line, beg, end):
        return [opt for opt in ['options', 'modules'] if opt.startswith(text)]

    def complete_set(self, text, line, beg, end):
        return [opt for opt in self.options if opt.startswith(text.upper())]

    # SET command
    def do_set(self, arg):
        "Set an option: set OPTION VALUE or SET SCAN"
        if not self.options:
            print(colored("Load a module first.", "yellow"))
            return

        parts = arg.strip().split(None, 1)
        if len(parts) == 0:
            print("Usage: set OPTION VALUE")
            return

        key = parts[0].upper()

        #scan modes
        if key == "SCAN" and self.module == "nmap" and len(parts) == 1:
            self.show_scan_selector()
            return
        #save modes
        if key == "SAVE" and self.module == "nmap":
            self.show_save_selector()

        if len(parts) != 2:
            print("Usage: set OPTION VALUE")
            return

        value = parts[1]
        # IP Validation implementation
        if key in ["IP", "RHOST"] and not validIp(value):
            print(colored(f"Invalid IP or CIDR format: {value}", "red"))
            return

        if key in self.options:
            self.options[key]["value"] = value
            print(f"{key} => {value}")
        else:
            print(colored(f"Invalid option: {key}", "red"))

    #---------------------
    # Scan type menu
    #---------------------
    def show_scan_selector(self):
        scan_modes = {
            "1": ("-sU", "etc"),
            "2": ("-sT", "etc"),
            "3": ("-sS", "etc"),
            "4": ("-sN", "etc"),
            "5": ("-sF", "etc"),
            "6": ("-sX", "etc")
        }

        print(colored("\nScan Types:", "white", attrs=["bold"]))
        print(f"{'ID':<4} {'Flag':<6} Description")
        print("-" * 30)
        for k, (flag, desc) in scan_modes.items():
            print(f"{k:<4} {flag:<6} {desc}")
        print()

        choice = input("Select scan type: set scan <number>\n" + colored("enumtk> ", "green"))

        if not choice.startswith("set scan"):
            print(colored("Invalid input. Use: set scan <number>", "red"))
            return

        parts = choice.strip().split()
        if len(parts) != 3 or parts[1] != "scan" or parts[2] not in scan_modes:
            print(colored("Invalid scan selection.", "red"))
            return

        flag = scan_modes[parts[2]][0]
        self.options["SCAN"]["value"] = flag
        print(f" Scan mode set to {flag} ({scan_modes[parts[2]][1]})")

    #---------------------
    # Save type menu
    #---------------------
    def show_save_selector(self):
        save_formats = {
            "1": ("txt", "Plaintext"),
            "2": ("xml", "XML format"),
            "3": ("gnmap", "Grepable format"),
            "4": ("nmap", "Standard nmap format"),
            "5": ("all", "Standard -oA (xml, gnmap, nmap)"),
            "6": ("false", "Do not save output")
        }

        print(colored("Save Formats:", "cyan", attrs=["bold"]))
        print(f"{'ID':<4} {'Flag':<8} Description")
        print("-" * 30)
        for k, (fmt, desc) in save_formats.items():
            print(f"{k:<4} {fmt:<8} {desc}")
        print()

        choice = input("Select save type: set save <number>\n" + colored("enumtk> ", "green"))

        if not choice.startswith("set save"):
            print(colored("Invalid input. Use: set save <number>", "red"))
            return

        parts = choice.strip().split()
        if len(parts) != 3 or parts[1] != "save" or parts[2] not in save_formats:
            print(colored("Invalid save selection.", "red"))
            return

        value = save_formats[parts[2]][0]
        self.options["SAVE"]["value"] = value
        print(f"{colored('>>', 'cyan')} Output save format set to: {value}")

    #---------------------
    # Show command preview
    #---------------------
    def show_command_preview(self):
        "Displays the full nmap command that would run"
        if self.module != "nmap":
            print(colored("Nmap only rn", "yellow"))
            return
        
        SCAN = self.options["SCAN"]["value"]
        rhost = self.options["RHOST"]["value"]
        ports = self.options["PORTS"]["value"]
        iface = self.options["INTERFACE"]["value"]
        misc = self.options["MISC"]["value"]
        save_fmt = self.options["SAVE"]["value"].lower()
        output_base = "scan_output"

        output_flags = ""
        if save_fmt == "txt":
            output_flags = f"> {output_base}.txt"
        elif save_fmt == "xml":
            output_flags = f"-oX {output_base}.xml"
        elif save_fmt == "gnmap":
            output_flags = f"-oG {output_base}.gnmap"
        elif save_fmt == "nmap":
            output_flags = f"-oN {output_base}.nmap"
        elif save_fmt == "all":
            output_flags = f"-oA {output_base}"

        misc_flags = misc if misc.lower() != "false" else ""

        # Determine base scan command
        if not SCAN.startswith("-s"):
            print(colored("Unknown SCAN flag: {SCAN}", "red"))

        final_cmd = f"nmap {SCAN} -p {ports} {misc_flags} {rhost} -e {iface} {output_flags}".strip()
        print(colored("\n>> Command Preview:\n", "cyan") + final_cmd + "\n")




    def do_run(self, arg):
        "Run scan"
        if not self.options:
            print(colored("Load a module first.", "yellow"))
            return

        # Checking for missing required options
        missing = [k for k, v in self.options.items() if v["required"] and not v["value"]]
        if missing:
            print(colored(f"Missing required options: {', '.join(missing)}", "red"))
            return

        # Module handler for nmap
        if self.module == "nmap":
            SCAN = self.options["SCAN"]["value"]
            rhost = self.options["RHOST"]["value"]
            ports = self.options["PORTS"]["value"]
            iface = self.options["INTERFACE"]["value"]
            misc_flags = self.options["MISC"]["value"]
            misc_flags = misc_flags if misc_flags.lower() != "false" else ""
            save_fmt = self.options["SAVE"]["value"].lower()
            output_base = "scan_output"

            output_flags = ""
            if save_fmt == "txt":
                output_flags = f"> {output_base}.txt"
            elif save_fmt == "xml":
                output_flags = f" -oX {output_base}.xml"
            elif save_fmt == "gnmap":
                output_flags = f" -oG {output_base}.gnmap"
            elif save_fmt == "nmap":
                output_flags = f" -oN {output_base}.nmap"
            elif save_fmt == "all":
                output_flags = f" -oA {output_base}"
            elif save_fmt in ["false", "no", "none"]:
                output_flags = ""
            else:
                print(colored("Invalid SAVE format. Use txt/xml/gnmap/nmap/all/false", "red"))

            if not SCAN.startswith("-s"):
                print(colored(f"Invalid SCAN value: {SCAN}", "red"))
                return

            #run final command
            final_cmd = f"sudo nmap {SCAN} -p {ports} {misc_flags} {rhost} -e {iface} {output_flags}".strip()
            print(colored(f"\n>> Running:\n{final_cmd}\n", "cyan"))
            os.system(final_cmd)

        elif self.module == "nmap_protocol":
            rhost = self.options["RHOST"]["value"]
            proto = self.options["PROTOCOL"]["value"]
            if proto == "ftp":
                os.system(f"nmap -sV -p 21 {rhost}")
            elif proto == "http":
                os.system(f"nmap -sV -p 80,443 {rhost}")
            elif proto == "smtp":
                os.system(f"nmap -sV -p 25 {rhost}")
            else:
                print(colored("Unsupported protocol.", "red"))

    def do_clear(self, arg):
        "Clear screen"
        os.system("clear")

    def do_exit(self, arg):
        "Exit shell"
        print("Goodbye.")
        return True

    def default(self, line):
        print(colored(f"Unknown command: {line}", "red"))

#---------------------
# Entry Point
#---------------------
if __name__ == "__main__":
    show_banner()
    print(colored("\n[1] Nmap", "white"))
    print(colored("[2] Nmap Protocol Specific", "white"))
    print(colored("[3] Exit", "white"))
    print()
    EnumShell().cmdloop()