# from scrapy import Selector
#
# import requests
#
# url = "http://tools.codetutor.top/web/datasource.json"
# url_1 = "http://tools.codetutor.top/web/index.html"
#
# resp = """<class>
#
#         <student>
#           <name gender="boy">Harry Potter</name>
#           <ID>24</ID>
#         </student>
#
#         <student>
#           <name gender="girl">Li Rose<font color=red>（monitor）</font></title>
#           <ID>1</ID>
#         </student>
#
#     </class>"""
#
#
# def parsel_html(response):
# 	"""
# 	选取根元素 class。
#     注释：假如路径起始于正斜杠( / )，则此路径始终代表到某元素的绝对路径！
# 	"""
# 	# 生成xpath 对象
# 	selector = Selector (response)
# 	content1 = selector.xpath ( "/class").get()
# 	content2=selector.xpath( "/class/student").get()
#
# 	print(content1)
# 	print(content2)
#
#
#
#
#
# if __name__ == '__main__':
# 	parsel_html (resp)

from werkzeug.security import generate_password_hash, check_password_hash
hash = generate_password_hash ("123456zxc")
print(hash)