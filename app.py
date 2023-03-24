from url_class import Url
import requests


local_URL='https://www.ynetnews.com/'
local_site = Url(local_URL, depth=2)
local_site.run()
