import re

import requests
url = "http://tools.codetutor.top/web/datasource.json"
url_1 = "http://tools.codetutor.top/web/index.html"

rep = requests.get(url_1).text

# with open("search_txt", "a", encoding="utf-8")as f:
# 	f.write(rep)
# 	print("写入完璧")

print(rep)