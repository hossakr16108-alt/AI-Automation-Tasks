import requests 
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import trafilatura

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_website_contents(url):
     
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code >= 400:
            return ""
        
        text = trafilatura.extract(response.text, include_comments=False, include_tables=False)
        
         
        if not text:
            soup = BeautifulSoup(response.content, "html.parser")
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input", "nav", "footer"]):
                    irrelevant.decompose()
                text = soup.body.get_text(separator="\n", strip=True)
            else:
                text = ""
                
        return text[:2500] if text else ""
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def fetch_website_links(url):
     
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        links = [link.get("href") for link in soup.find_all("a")]
        return [link for link in links if link]
    except Exception:
        return []

  
def urls_filter(urls_list:list):
    valid_urls = []
    for url in urls_list:
        parsed_url = urlparse(url)
        is_syntax_valid = parsed_url.scheme in ['http', 'https'] and parsed_url.netloc
        if not is_syntax_valid:
            continue

        try:
            response = requests.get(url,headers=HEADERS, timeout=10, allow_redirects=True)
            if response.status_code < 400 :
                valid_urls.append(url)
            else:
                print(
                    f"⚠️ Link unreachable or access restricted "
                    f"({response.status_code}): {url}"
                )
        except requests.RequestException:
            print(f"❌ Connection error: {url}")

    return valid_urls

 
def get_website_content(valid_urls: list):  
  all_content=" "
  for index , url in enumerate(valid_urls,start=1):
    content=fetch_website_contents(url)
    all_content+=f'\n company{index}: {url}\n{content}\n {"_" *50}\n'
 
  return all_content




 


 
