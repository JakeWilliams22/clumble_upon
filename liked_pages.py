from pprint import pprint
import requests
from bs4 import BeautifulSoup
import json

''' Converts a downloaded HTML file of 'liked' pages from a user 
into a json file of URL's and some metadata '''

saveFile = 'StumbleUpon - StumbleUpon.html'
outFile = 'savedUrls.json'
numRetries = 1

def save_likes():
  stumble_urls = get_saved_urls()
  convertedUrls = process_stumble_urls(stumble_urls)
  write_list_to_file(convertedUrls)
  
def get_saved_urls():
  saveHTML = ""
  with open(saveFile, 'r') as file:
    saveHTML = file.read().replace('\n', '')
  soup = BeautifulSoup(saveHTML, "html.parser")
  anchors = soup.findAll("a")
  stumble_urls = [x.attrs['href'] for x in anchors if 'title' in x.parent['class']]
  return stumble_urls
  
def process_stumble_urls(urls):
  redirected_urls = []
  failed_urls = []
  for i, url in enumerate(urls):
    print("Getting mapping for url number " + str(i) + " of " + str(len(urls)))
    mapped = get_mapped_url(url)
    if 'url' in mapped.json():
      redirected_urls.append(mapped.json()['url']);
    else:
      failed_urls.append(url)
      print("error parsing response for url: " + str(url) + ", adding to retry queue...")
  retry_idx = 0
  attempted_retries = 0
  while attempted_retries < numRetries and len(failed_urls) > 0:
    url = failed_urls[retry_idx]
    mapped = get_mapped_url(url)
    if 'url' in mapped.json():
      redirected_urls.append(mapped.json()['url'])
      failed_urls.pop(retry_idx)
    else:
      print("Failed parsing response for url " + url)
    retry_idx += 1  
    if retry_idx == len(failed_urls):
      print("Retry attempt " + str(attempted_retries) + " completed.")
      attempted_retries += 1
      retry_idx = 0
  print("Failed to find mapping for the following urls: ")
  print(failed_urls)
  return redirected_urls
  
def get_mapped_url(url):
  id = url.split("/")[-1]
  return requests.get('https://www.stumbleupon.com/api/v2_0/url?urlid=' + id)
  
def write_list_to_file(list):
  f = open(outFile, 'w')
  json.dump(list, f)

save_likes()