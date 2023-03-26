from web_crawler import WebCrawler
import requests


SECOND_URL = 'https://www.pythontutorial.net/'
# SECOND_URL ="https://justdvir.online/" # WebCrawler without www
# SECOND_URL ="https://en.wikipedia.org/wiki/Moyshe_Kulbak" # WebCrawler without www
# local_URL='https://www.ynetnews.com/'

myCrawler = WebCrawler(url=SECOND_URL, depth=2, maximal_amount=5, unique_url=True)

# local_site.search_for_links(requests.get(SECOND_URL).text)

myCrawler.run()
print(myCrawler.downloaded_urls)
