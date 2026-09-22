import datetime
import urllib.request
import xml.etree.ElementTree as ET


def fetch_tech_headlines():
  # Fetches latest tech news via BBC Tech RSS feed (no API key required)
  url = "https://feeds.bbci.co.uk/news/technology/rss.xml"
  req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

  with urllib.request.urlopen(req) as response:
    xml_data = response.read()

  root = ET.fromstring(xml_data)
  items = root.findall(".//item")[:5]

  headlines = []
  for item in items:
    title = item.find("title").text
    link = item.find("link").text
    headlines.append(f"- [{title}]({link})")

  return headlines


def update_log():
  now = datetime.datetime.now(datetime.timezone.utc).strftime(
      "%Y-%m-%d %H:%M:%S UTC"
  )
  headlines = fetch_tech_headlines()

  log_entry = f"\n### Update: {now}\n" + "\n".join(headlines) + "\n"

  with open("LATEST_NEWS.md", "a", encoding="utf-8") as f:
    f.write(log_entry)

  print(f"Successfully logged 5 headlines at {now}")


if __name__ == "__main__":
  update_log()
