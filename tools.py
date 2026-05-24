from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

tavily=TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

#Tavily call tool
@tool 
def web_search(query:str)->str:
    """Search the web for recent and reliable information on a topic.Returns titles,URL's and snippets"""
    results=tavily.search(query=query,max_results=5)
    # return results
# print(web_search.invoke('What are recent news of war'))
    out=[]
    for r in results['results']:
        out.append(
            f"Title:{r['title']}\nURL:{r['url']}\nSnippet:{r['content'][:300]}\n"
        )
    return "\n---\n".join(out)
# print(web_search.invoke('what is recent news of war'))




#beautiful soup scrap tool
@tool
def scrape_url(url:str)->str:
    """Scrape and return clean text content from a given URL for deeper reading"""
    try:
        resp=requests.get(url,timeout=8,headers={'User-Agent':'Mozilla/5.0'})
        soup=BeautifulSoup(resp.text,'html.parser')
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ",strip=True)[:3000]
    except Exception as e:
        return f'Could not scrape URL:{str(e)}' 
    
# print(scrape_url.invoke('https://news.un.org/en/story/2026/05/1167542'))


        