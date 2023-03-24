from url_class import WebCrawler
import requests


SECOND_URL ="https://justdvir.online/" # WebCrawler without www
local_URL='https://www.ynetnews.com/'
local_site = WebCrawler(url=SECOND_URL, depth=0, maximal_amount=1)

local_site.search_for_links()

# print(f"Valid-Name:-{local_site.get_valid_file_name()}")
# local_site.run()
