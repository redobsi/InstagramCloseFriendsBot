import time
import json
import random
from threading import Thread, current_thread
from instagram import Bot
from task_limiter import increment_task
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class Automation:
    
    def __init__(self, config):
        self.config = config  # : path_to_list, sleep_interval, username, password, max_adds
        self.is_running = False
        
    def check_config(self):
        required_keys = ["path_to_list", "sleep_interval", "username", "password", "max_adds"]
        
        for key in required_keys:
            if not self.config.get(key):
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid or missing configuration key: {key}")
                return False
        
        return True
        
    def resume_automation(self):
        self.is_running = True
        self.automation_thread = Thread(target=self._automation_worker)
        self.automation_thread.start()

    def _automation_worker(self):
        bot = Bot()
        assert self.check_config()
        
        try:
            session = bot.get_session()
            
        except FileNotFoundError:
            print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Session file not found. Logging in...")
            session = bot.sign_in(self.config["username"], self.config["password"])
            if not session:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Login failed.")
                return
            with open('session.json', 'w') as f:
                json.dump(session["values"], f, indent=4)
            
        failure_count = 0
        max_failures = 5  # Stop automation after 5 consecutive failures
        cooldown_time = 10  # Cooldown time in seconds after an exception

        while self.is_running:
            with open(self.config["path_to_list"], "r") as f:
                lines = f.readlines()
            
            if not lines:
                print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} All lines processed successfully. Stopping automation.")
                self.stop_automation()
                break
            
            num_lines_to_process = random.randint(0, self.config["max_adds"])
            lines_to_process = random.sample(lines, min(num_lines_to_process, len(lines)))
            
            for line in lines_to_process:
                if not self.is_running:
                    break
            
                line = line.strip()
                if not line:
                    continue
                
                try:
                    bot.add_close_friend(line)
                    increment_task()
                    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Successfully added {line} as a close friend.")
                    lines = [l for l in lines if l.strip() != line]
                    with open("added_close_friend.txt", "a") as added_file:
                        added_file.write(line + "\n")
                    failure_count = 0  # Reset failure count on success
                    time.sleep(random.uniform(0.5, 2))  # Sleep between each added close friend
                except Exception as e:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Error adding {line}: {e}")
                    lines.append(line + "\n")
                    failure_count += 1
                    if failure_count >= max_failures:
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Too many consecutive failures. Stopping automation.")
                        self.stop_automation()
                        break
                    print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Cooling down for {cooldown_time} seconds...")
                    time.sleep(cooldown_time)  # Cooldown after an exception
                    continue
            
            with open(self.config["path_to_list"], "w") as f:
                f.writelines([l.strip() + "\n" for l in lines])
            
            time.sleep(random.uniform(0, self.config["sleep_interval"]))  # Sleep between batches

    def stop_automation(self):
        self.is_running = False
        if hasattr(self, "automation_thread") and self.automation_thread != current_thread():
            self.automation_thread.join()

