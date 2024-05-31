import requests
import re

def scrape_jina_ai(url: str):
    response = requests.get("https://r.jina.ai/" + url)
    return response.text


def extract_conversations(text):
    # Regex pattern to match text in double quotes
    pattern = r'\"(.*?)\"'
    
    # Find all matches
    matches = re.findall(pattern, text)
    
    return matches

print(extract_conversations(scrape_jina_ai("https://www.literotica.com/s/virtual-to-real-pt-01")))
