import re
import os
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def clamp(x, low=0, high=10):
    return max(low, min(high, x))

def has_any(text, words):
    return any(w.lower() in text.lower() for w in words)

def extract_urls(text):
    return re.findall(r"https?://[^\s\u3000]+|www\.[^\s\u3000]+", text)

def extract_domains(urls):
    domains = []
    for u in urls:
        try:
            if u.startswith("www."):
                u = "https://" + u
            netloc = urlparse(u).netloc.lower()
            if netloc:
                domains.append(netloc)
        except Exception:
            pass
    return domains
