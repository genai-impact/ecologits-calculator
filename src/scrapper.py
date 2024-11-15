import requests
from bs4 import BeautifulSoup
import tiktoken

tokenizer = tiktoken.get_encoding('cl100k_base')

def process_input(text):

    r = requests.get(text, verify=False)
    
    soup = BeautifulSoup(r.text, "html.parser")
    print(soup)
    list_text = str(soup).split('parts":["')
    #print(list_text)
    s = ''
    for item in list_text[1:int(len(list_text)/2)]:
        if list_text.index(item)%2 == 1:
                s = s + item.split('"]')[0]

    amout_token = tiktoken_len(s)

    return amout_token

def tiktoken_len(text):
            tokens = tokenizer.encode(
                text,
                disallowed_special=()
            )
            return len(tokens)

answer = process_input('https://chatgpt.com/share/6737b9b5-56fc-8002-a212-35339f5b1d5a')

print(answer)