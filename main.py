from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import random
import json


LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
BOLD = "\033[1m"
RESET = '\033[0m'
UP = "\033[1A"
CLEAR = "\x1b[2K"

TYPERACER = 'https://play.typeracer.com/'
MONKEYTYPE = 'https://monkeytype.com/'

probability = [0,0,0,0,0,1]
mistake_lst = [0, 0, 0, 0, 1, 2, 3, 4]
pause_lst = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
wrong_pause_lst = [0, 0, 0, 0.1, 0.15]
alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'")

website = ''

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

def typeRacer():
    global website

    website = 'typeracer'

    print(f'{LIGHT_GREEN}Redirect to TypeRacer{RESET}')
    driver.get(TYPERACER)

    interval = float(input(f'{BOLD}- Interval: {RESET}'))
    mistake = str(input(f'{BOLD}- Allow mistakes [y/n]: {RESET}')).strip()
    pause = str(input(f'{BOLD}- Allow pause [y/n]: {RESET}')).strip()

    lst = list(WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[unselectable="on"]'))))
    
    word_lst = []
    for i in range(len(lst)):
        if (i == len(lst)-1):
            word_lst.append(' ')
        for word in list(lst[i].text):
            word_lst.append(word)

    # print(word_lst)
    txt_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.txtInput')))
    print('Starting...')
    time.sleep(0.1) # Ensure the visibility

    st = time.time()
    for index in range(len(word_lst)):
        if random.choice(probability) == 1 and index > 2:
            if (mistake=='y'):
                m = random.choice(mistake_lst)
                for i in range(m):
                    txt_input.send_keys(random.choice(alphabet)) # Choose random letter to press
                    time.sleep(random.choice(wrong_pause_lst))
                for i in range(m):
                    txt_input.send_keys(Keys.BACKSPACE)
                    time.sleep(random.choice(wrong_pause_lst))
            if (pause=='y'):
                p = random.choice(pause_lst) # Random pause between characters
                time.sleep(p)
        txt_input.send_keys(word_lst[index])
        time.sleep(interval)

    et = time.time()
    print(f'{LIGHT_GREEN}Finished in: {str(round(et-st, 2))}{RESET}')

def monkeyType():
    global website

    website = 'monkeytype'

    print(f'{LIGHT_GREEN}Redirect to MonkeyType{RESET}')
    driver.get(MONKEYTYPE)

    start_type = str(input('Choose type: ')).strip().lower()

    if start_type == 'time' or start_type == 'word':

        interval = float(input(f'{BOLD}- Interval: {RESET}'))
        mistake = str(input(f'{BOLD}- Allow mistakes [y/n]: {RESET}')).strip()
        pause = str(input(f'{BOLD}- Allow pause [y/n]: {RESET}')).strip()

        driver.find_element(By.CSS_SELECTOR, '#words').click()
        txt_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#wordsInput')))
        print('Starting...')
        time.sleep(0.1) # Ensure the visibility

        # Start typing
        txt_input.send_keys('a')
        txt_input.send_keys(Keys.BACKSPACE)
        

        st = time.time()
        while 'hidden' not in driver.find_element(By.CSS_SELECTOR, '#miniTimerAndLiveWpm .time').get_attribute('class'):
            try:
                # Maintain focus
                driver.find_element(By.CSS_SELECTOR, '#words').click()

                word_active = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.word.active')))
                letter = [i.text for i in word_active.find_elements(By.CSS_SELECTOR, 'letter')]
                # print(letter)
                word_length = len(letter)

                for index in range(len(letter)):
                    if random.choice(probability) == 1 and index > 2:
                        if (mistake=='y'):
                            m = random.randint(1, word_length)
                            for i in range(m):
                                txt_input.send_keys(random.choice(alphabet))
                                time.sleep(random.choice(wrong_pause_lst))
                            for i in range(m):
                                txt_input.send_keys(Keys.BACKSPACE)
                                time.sleep(random.choice(wrong_pause_lst))
                        if (pause=='y'):
                            p = random.choice(pause_lst)
                            time.sleep(p)
                    
                    txt_input.send_keys(letter[index])
                    time.sleep(interval)
                txt_input.send_keys(Keys.SPACE)
            
            except:
                # Stop when the timer goes off (even typing words)
                break

        et = time.time()
        print(f'{LIGHT_GREEN}Finished in: {str(round(et-st, 2))}{RESET}')

def main():
    while True:
        cmd = str(input('>> COMMAND: ')).strip().lower()

        if cmd == 'restart':
            if website != '':
                if website == 'typeracer':
                    typeRacer()
                elif website == 'monkeytype':
                    monkeyType()
            else:
                print('No website saved')

        elif cmd == 'start typeracer':
            typeRacer()
            
        elif cmd == 'start monkeytype':
            monkeyType()
        
        elif cmd == 'load typeracer':

            driver.get(TYPERACER)

            load_cookies = str(input(f'{BOLD}- Path to JSON: {RESET}')).strip()

            if (load_cookies != ''):
                try:
                    # ./typeracer-cheat/typeracer-cookies.json
                    with open(load_cookies, encoding='utf-8') as f:
                        data = json.load(f)
                        cookies = data['cookies']
                        for cookie in cookies:
                            if 'sameSite' in cookie:
                                cookie['sameSite'] = 'Strict'
                            driver.add_cookie(cookie)

                    driver.refresh()
                
                except FileNotFoundError as e:
                    print(e)

        elif cmd == 'load monkeytype':
            driver.get(MONKEYTYPE)

            load_cookies = str(input(f'{BOLD}- Path to JSON: {RESET}')).strip()

            if (load_cookies != ''):
                try:
                    # ./typeracer-cheat/typeracer-cookies.json
                    with open(load_cookies, encoding='utf-8') as f:
                        data = json.load(f)
                        cookies = data['cookies']
                        for cookie in cookies:
                            if 'sameSite' in cookie:
                                cookie['sameSite'] = 'Strict'
                            driver.add_cookie(cookie)

                    driver.refresh()
                
                except FileNotFoundError as e:
                    print(e)
        
        elif cmd == 'quit':
            print(f'{LIGHT_GREEN}Quited the game!{RESET}')
            break

        else:
            print(f'{LIGHT_RED}Command not found!{RESET}')

if __name__ == '__main__':
    main()