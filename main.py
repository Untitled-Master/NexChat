import json
from g4f.client import Client
from colorama import Fore, Style, init
import requests
from tqdm import tqdm
import time
from datetime import datetime

# Initialize colorama
init(autoreset=True)

HISTORY_FILE = 'history.json'
PROMPT_FILE = 'prompt.json'
MAX_HISTORY = 20
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
client = Client()

# Custom bar format with green color using colorama
bar_format = "{l_bar}%s{bar}%s| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {rate_fmt} - {postfix}" % (Fore.GREEN, Fore.RESET)

def start():
    print(Fore.GREEN +'''
 __    _  _______  __   __  _______  _______  __   __  _______  _______ 
|  |  | ||       ||  |_|  ||       ||       ||  | |  ||   _   ||       |
|   |_| ||    ___||       ||   _   ||       ||  |_|  ||  |_|  ||_     _|
|       ||   |___ |       ||  | |  ||       ||       ||       |  |   |  
|  _    ||    ___| |     | |  |_|  ||      _||       ||       |  |   |  
| | |   ||   |___ |   _   ||       ||     |_ |   _   ||   _   |  |   |  
|_|  |__||_______||__| |__||_______||_______||__| |__||__| |__|  |___|    \n''')
    print(f"[+] Time: {current_time}")
    # Loop with customized green progress bar
    with tqdm(total=100, bar_format=bar_format, ncols=80) as pbar:
        for i in range(100):
            # Simulate work with time.sleep()
            time.sleep(0.01)
            
            # Update progress and set custom postfix text
            pbar.set_postfix_str("Opening NexChat...")
            pbar.update(1)
    print("NexChat opened successfully!")

start()

def load_history():
    try:
        with open(HISTORY_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
def load_prompt():
    try:
        with open(PROMPT_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_history(history):
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history, file)

history = load_history()
pr = load_prompt()
prompt = pr[0]['content']

while True:
    user_input = input(Fore.GREEN + "[+] You: " + Style.RESET_ALL)
    if user_input.lower() in ['exit', 'quit']:
        break
    prompted = (f"{prompt}: {user_input}")
    history.append({"role": "user", "content": prompted})
    
    if len(history) > MAX_HISTORY:
        history.pop(0)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history,
    )
    bot_response = response.choices[0].message.content
    print(Fore.CYAN + "[+] Bot: " + bot_response + Style.RESET_ALL)

    history.append({"role": "assistant", "content": bot_response})
    if len(history) > MAX_HISTORY:
        history.pop(0)

    save_history(history)