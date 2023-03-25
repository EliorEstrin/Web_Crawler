from url_class import WebCrawler
import requests


# SECOND_URL ="https://justdvir.online/" # WebCrawler without www
SECOND_URL ="https://en.wikipedia.org/wiki/Moyshe_Kulbak" # WebCrawler without www

local_URL='https://www.ynetnews.com/'
local_site = WebCrawler(url=SECOND_URL, depth=2, maximal_amount=2)

# local_site.search_for_links(requests.get(SECOND_URL).text)

local_site.run()
