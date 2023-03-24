from url_class import Url
import requests


local_URL='https://www.ynetnews.com/'
local_site = Url(url=local_URL, depth=0)

print(f"Valid-Name:-{local_site.get_valid_file_name()}")
# local_site.run()
