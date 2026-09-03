import requests 
from bs4 import BeautifulSoup
 
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
  
def fetch_website_contents(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code >= 400:
            return ""

        soup = BeautifulSoup(response.content, "html.parser")
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input", "nav", "footer"]):
                irrelevant.decompose()
            return soup.body.get_text(separator=' ', strip=True)
            
        return ""
    except Exception as e:
        return ""

def fetch_website_links(url):
     
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        links = [link.get("href") for link in soup.find_all("a")]
        return [link for link in links if link]
    except Exception:
        return []

 
