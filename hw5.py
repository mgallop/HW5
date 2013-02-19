import csv
import re
import urllib2
from BeautifulSoup import BeautifulSoup
import time
page = "http://citizen-statistician.org"

filename = "hw5.csv"
readFile = open(filename, 'wb')
csvwriter = csv.DictWriter(readFile, fieldnames = ("is_post", "publish_date", "author", "url", "post_title", "comment_count"))

def hwscraper(site, previous = []):
  bad = re.compile("pinterest")
  bad2 = re.compile("linkedin")
  bad3 = re.compile("jpg")
  bad4 = re.compile("png")
  if site in previous or bad.search(str(site)) or bad2.search(str(site)) or bad3.search(str(site)) or bad4.search(str(site)):
    return
# check if meta property = "article" for is post, and also author/date/etc.
  print site
  previous.append(str(site))
  time.sleep(1)
  webpage = urllib2.urlopen(site)
  soup = BeautifulSoup(webpage.read())
  links = []
  z = re.compile(r"article")
  v = re.compile("article:published_time")
  w = re.compile("og:title")
  u = re.compile("article:author")
  is_post = 0
  author = ""
  publish_date = ""
  title = ""
  for tag in soup('meta'):
    if z.search(str(tag)):
      is_post = 1
    if v.search(str(tag)):
      publish_date = str(tag).split("content=")[1].split("/>")[0]
    if w.search(str(tag)):
      title = str(tag).split("content=")[1].split("/>")[0]
    if u.search(str(tag)):
      author = str(tag).split('content="http://citizen-statistician.org/author/')[1].split("/>")[0]

  s = re.compile(r"share")
  x = re.compile(r"citizen-statistician.org")
  y = re.compile(r"comment")
  ht = re.compile("#")
  s = re.compile(r"social-all")
  comment_count = 0
  for link in soup('a'):
    if s.search(str(link)):
      comment_count = int(str(link).split("span>")[1].split(" Repl")[0])
    if x.search(link['href']) and not s.search(link['href']) and not y.search(link['href']) and not ht.search(link['href']):
      links.append(str(link['href']))
  csvwriter.writerow({"url": site, "is_post":is_post, "author":author, "publish_date": publish_date, "comment_count": comment_count})
  for link in links:
    hwscraper(link, previous)
  return None

hwscraper(page)