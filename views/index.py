from flask import render_template, request, jsonify, session
from models import db
from models.index import News, User

from . import index_blu


@index_blu.route ('/')
def index():
	# return "主页index ----"
	# 查询点击量最多的前6个新闻信息

	clicks_top_6_news = db.session.query (News).order_by (-News.clicks).limit (6)

	# 查询用户是否已经登录
	user_id = session.get ("user_id", 0)
	nick_name = session.get ("nick_name", "")

	return render_template ("index.html", clicks_top_6_news=clicks_top_6_news, nick_name=nick_name)


@index_blu.route ("/newslist")
def category_news():
	# 1. 获取前端的传来的数据， 就是提取URL中的数据
	# http:、、127.0.0.1:8899、newslist？page=1&cid=1&per_page=10
	page = request.args.get ("page")  # 前端要的是哪一页数据
	cid = int (request.args.get ("cid"))  # 前端要的是哪个分类的数据，是股市，债市，，，
	per_page = request.args.get ("per_page")  # 前端要的是每一页的新闻的个数

	if cid == 0:
		# # 最新分类， 按更新时间来查找
		# 	paginate = db.session.query (News).order_by (-News.update_time).paginate (page=int (page),
		# 	                                                                          per_page=int (per_page),
		# 	                                                                          error_out=False)
		# else:
		# 	cid += 1  # 由于测试数据分类中从0开始，而数据库中是从1开始的，所以用户点击的1实际上是2
		#
		# 	paginate = db.session.query (News).filter (News.category_id == cid).paginate (page=int (page),
		# 	                                                                              per_page=int (per_page),
		# 	                                                                              error_out=False)

		paginate = db.session.query (News).filter (News.status == 0).order_by (-News.create_time).paginate (
			page=int (page), per_page=int (per_page), error_out=False)
	else:
		cid += 1  # 由于测试数据分类中从0开始，而数据库中是从1开始的，所以用户点击的1实际上是2
		paginate = db.session.query (News).filter (News.category_id == cid, News.status == 0).order_by (
			-News.create_time).paginate (page=int (page), per_page=int (per_page), error_out=False)

	ret = {
		"totalPage": paginate.pages,  # 总页数
		"newsList": [news.to_dict () for news in paginate.items]
	}
	# 4. 将ret字典转换为json样子的字符串，返回
	return jsonify (ret)


@index_blu.route ("/detail/<int:news_id>")
def detail(news_id):
	# 提取url中的 参数（数字）
	news = db.session.query (News).filter (News.id == news_id).first ()

	# 查询这个新闻的作者
	news_author = news.user
	news_author.news_num = news_author.news.count ()
	news_author.follwer_num = news_author.followers.count ()
	# 查询用户是否已经登录
	user_id = session.get ("user_id", 0)
	nick_name = session.get ("nick_name", "")

	# password = request.json.get ("password")

	# 2. 查询，如果存在表示登录成功，否则失败
	# user = db.session.query (User).filter (User.mobile == nick_name, User.user.id == user_id).first ()
	# if user:
	# 	ret = {
	# 		"errno": 0,
	# 		"errmsg": "登录成功"
	# 	}
	# 	return jsonify (ret)
	#
	# else:
	# 	ret = {
	# 		"errno": 2001,
	# 		"errmsg": "用户名或者密码错误"
	# 	}
	#
	# 	return jsonify (ret)

	news_author_followers_id = [x.id for x in news_author.followers]
	if user_id in news_author_followers_id:
		news_author.can_follow = False  # 已经关注了作者，就不能在关注了
	else:
		news_author.can_follow = True  # 可以关注

	# 计算当前用户是否收藏了这个篇文章
	news_collected_user_id = [x.id for x in news.collected_user]
	if user_id in news_collected_user_id:
		news.can_collect = False  # 已经收藏了，就不要在收藏了
	else:
		news.can_collect = True  # 可以收藏

	# 获取评论
	comments = news.comments.order_by (-Comment.create_time)

	return render_template ("detail.html", news=news, nick_name=nick_name, news_author=news_author,
	                        click_detail_news_sex=click_detail_news_sex, comments=comments)

