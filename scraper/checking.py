from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin

BASE_URL = "https://www.zomato.com" 
ROBOTS_TXT = urljoin(BASE_URL, "/robots.txt")

rp = RobotFileParser()
rp.set_url(ROBOTS_TXT)
rp.read()

USER_AGENT = "*"
SCRAPE_PATH = "/"

if rp.can_fetch(USER_AGENT, urljoin(BASE_URL, SCRAPE_PATH)):
    print("✅ Scraping allowed")
else:
    print("❌ Scraping disallowed by robots.txt. Exiting.")
