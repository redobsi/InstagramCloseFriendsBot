import json
from automation import Automation
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
 ██████╗██╗      ██████╗ ███████╗███████╗██████╗ 
██╔════╝██║     ██╔═══██╗██╔════╝██╔════╝██╔══██╗
██║     ██║     ██║   ██║███████╗█████╗  ██████╔╝
██║     ██║     ██║   ██║╚════██║██╔══╝  ██╔══██╗
╚██████╗███████╗╚██████╔╝███████║███████╗██║  ██║
 ╚═════╝╚══════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
{Style.RESET_ALL}
"""
    print(banner)

def main():
    # Load configuration from config.json
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Initialize the Automation class
    automation = Automation(config)

    print_banner()
    print(Fore.YELLOW + "Commands:")
    print(f"{Fore.GREEN}start{Style.RESET_ALL} - {Fore.CYAN}Start the automation")
    print(f"{Fore.GREEN}stop{Style.RESET_ALL} - {Fore.CYAN}Stop the automation")
    print(f"{Fore.GREEN}resume{Style.RESET_ALL} - {Fore.CYAN}Resume the automation")
    print(f"{Fore.GREEN}exit{Style.RESET_ALL} - {Fore.CYAN}Exit the application")

    while True:
        command = input(Fore.GREEN + "Enter command: ").strip().lower()

        if command == "start":
            if automation.is_running:
                print(Fore.RED + "Automation is already running.")
            else:
                print(Fore.BLUE + "Starting automation...")
                automation.resume_automation()

        elif command == "stop":
            if not automation.is_running:
                print(Fore.RED + "Automation is not running.")
            else:
                print(Fore.BLUE + "Stopping automation...")
                automation.stop_automation()

        elif command == "resume":
            if automation.is_running:
                print(Fore.RED + "Automation is already running.")
            else:
                print(Fore.BLUE + "Resuming automation...")
                automation.resume_automation()

        elif command == "exit":
            print(Fore.MAGENTA + "Exiting application...")
            if automation.is_running:
                automation.stop_automation()
            break

        else:
            print(Fore.RED + "Invalid command. Please use:")
            print(f"{Fore.GREEN}start{Style.RESET_ALL}, {Fore.GREEN}stop{Style.RESET_ALL}, {Fore.GREEN}resume{Style.RESET_ALL}, or {Fore.GREEN}exit{Style.RESET_ALL}.")

if __name__ == "__main__":
    main()