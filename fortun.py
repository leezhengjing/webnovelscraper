import openai
import os

import requests
from bs4 import BeautifulSoup
import re

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')

client = openai.OpenAI()

def get_completion(prompt, model="gpt-4o"):
    messages = [
        {"role": "system", "content": "You are a custom GPT called Novel Translator. Novel Translator specializes in translating fantasy, wuxia, and xianxia Chinese web novels into English, focusing on accurate translations of cultural references, idiomatic expressions, and genre-specific terminology like cultivator ranks and power systems. It ensures translations are well-formatted, capitalizing only the first letter of character names and leaving them untranslated (e.g., 'Yan Jianyue'). The GPT avoids incorrect translations of names and uses appropriate pronouns, aiming to include a glossary to prevent errors. It provides translations directly without additional conversation, focusing solely on the output quality and accuracy. Novel Translator will now be able to learn from already translated chapters to maintain consistency in style, tone, and formatting as exemplified by translations provided."},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=model,    
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content

URL = "https://www.fortuneeternal.com/novel/a-regressors-tale-of-cultivation-raw-novel/chapter-287/"
# URL = "https://www.fortuneeternal.com/novel/i-became-a-flashing-genius-at-the-magic-academy-raw-novel/chapter-145/"
html_text = requests.get(URL).text
soup = BeautifulSoup(html_text, 'lxml')

# Find the chapter heading
chapter_heading = soup.find('h1', id='chapter-heading').get_text()

# Sanitize the chapter heading to create a valid filename
valid_filename = re.sub(r'[^\w\-_\. ]', '_', chapter_heading)

# Find the div with class 'text-left'
text_left_div = soup.find('div', class_='text-left')

# Find all <p> elements within this div
paragraphs = text_left_div.find_all('p')

# Combine the text of each <p> element into one string
combined_text = ' '.join(p.get_text() for p in paragraphs)

print(chapter_heading)
print(combined_text)

# Create the folder if it doesn't exist
# folder_name = 'Flashing_Genius'
folder_name = 'RTOC'
# os.makedirs(folder_name, exist_ok=True)
# with open(os.path.join(folder_name,f'{valid_filename}.txt'), 'w',encoding="utf-8") as file:
#     file.write(combined_text)

# Read the content of the text file
# with open(os.path.join(folder_name,f'{valid_filename}.txt'), 'r', encoding='utf-8') as file:
#     text = file.read()

prompt = f"""
Translate the text delimited by triple backticks into English. Make sure the text is well formatted with spacing between sentences.
```{combined_text}```
"""
response = get_completion(prompt)
# # Export as txt
# # Format the response to be more readable by separating each sentence
# response = response.replace(". ", ".\n")
# response = response.replace("! ", "!\n")
# response = response.replace("? ", "?\n")

with open(os.path.join(folder_name,f'{valid_filename}TRANSLATED.txt'), "w") as f:
    f.write(response)
print(response)