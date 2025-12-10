import requests
a=input("Ask your query:")

def check_api():
    if "news" in a or "article" in a or "happen" in a:
        return "news"
        
    elif "meaning" in a or "means" in a or "define":
        return "dictionary"
    else:
        return "unknown"
    

def news_api():
    response=requests.post(
        url=f"https://gnews.io/api/v4/{endpoint}?{parameters}&apikey=YOUR_API_KEY"
    )