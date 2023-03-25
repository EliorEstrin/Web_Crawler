from url_class import WebCrawler
import requests


SECOND_URL ="https://justdvir.online/" # WebCrawler without www
local_URL='https://www.ynetnews.com/'

local_site = WebCrawler(url=SECOND_URL, depth=0, maximal_amount=1)

local_site.run()
