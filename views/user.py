import hashlib
import os
import time

from flask import jsonify, request, session, render_template, redirect, url_for

from models import db
from models.index import User, Follow, Category, News
from untils.image_qiniu import upload_image_to_qiniu
from . import user_blu, index_blu


@user_blu.route ("/user/follow", methods=["POST"])
def follow():
	# 实现关注的流程
	# 1. 提取当前作者的id
	# 2. 提取当前登录用户的id
	# 3. 判断之前是否已经关注过
	# 4. 如果未关注，则进行关注

	# 根据action 的不同来判断是否关注
	news_action = request.json.get ("action")
	# 1. 提取当前作者的id
	news_author_id = request.json.get ("user_id")

	# 2. 提取当前登录用户的id
	user_id = session.get ("user_id")

	if not user_id:
		return jsonify ({
			"errno": 3002,
			"errmsg": "请用户您先进行登录----"
		})

	if news_action == "do":

		# 3. 判断之前是否已经关注过
		news_author = db.session.query (User).filter (User.id == news_author_id).first ()

		if user_id in [x.id for x in news_author.followers]:
			print ("3001-----------------------已经关注")
			return jsonify ({
				"errno": 3001,
				"errmsg": "已经关注了，请勿重复关注"
			})

		# 4. 如果未关注，则进行关注
		try:
			follow = Follow (followed_id=news_author_id, follower_id=user_id)
			db.session.add (follow)
			db.session.commit ()
			ret = {
				"errno": 0,
				"errmsg": "关注成功"
			}

			return jsonify (ret)


		except Exception as ret:
			ret = {
				"errno": 3003,
				"errmsg": "关注失败"
			}
			print ("""-----------+++++++try--""")
			return jsonify (ret)

	else:
		try:
			follow = db.session.query (Follow).filter (Follow.followed_id == user_id,
			                                           Follow.follower_id == news_author_id).first ()

			print ("取消 ------------")
			db.session.delete (follow)
			db.session.commit ()

			ret = {
				"errno": 0,
				"errmsg": "取消关注成功"
			}

			return jsonify (ret)

		except Exception as ret:
			db.session.rollback ()
			ret = {
				"errno": 3004,
				"errmsg": "取消关注失败..."
			}

			return jsonify (ret)


@user_blu.route ("/user/center")
def user_center():
	# 获取当前用户的信息
	nick_name = session.get ("nick_name")

	# 如果用户未登录，禁止访问用户中心
	if not nick_name:
		return redirect (url_for ('index_blu.index'))
	user_id = session.get ("user_id")
	user = db.session.query (User).filter (User.id == user_id).first ()

	return render_template ("user.html", nick_name=nick_name, user=user)


@user_blu.route ("/user/user_base_info")
def user_base_info():
	return render_template ("user_base_info.html")


@user_blu.route ("/user/basic", methods=["POST"])
def user_basic():
	# 获取用户的新的信息
	nick_name = request.json.get ("nick_name")
	signature = request.json.get ("signature")
	gender = request.json.get ("gender")

	# 获取当前用户的信息
	user_id = session.get ("user_id")

	# 存储到数据库
	user = db.session.query (User).filter (User.id == user_id).first ()
	if not user:
		ret = {
			"errno": 4002,
			"errmsg": "没有此用户"
		}

		return jsonify (ret)

	# 如果查询到此用户就修改数据
	user.nick_name = nick_name
	user.signature = signature
	user.gender = gender

	db.session.commit ()

	ret = {
		"errno": 0,
		"errmsg": "修改成功..."
	}
	return jsonify (ret)


@user_blu.route ("/user/user_pass_info")
def user_pass_info():
	return render_template ("user_pass_info.html")


@user_blu.route ("/user/password", methods=["POST"])
def user_password():
	new_password = request.json.get ("new_password")
	old_password = request.json.get ("old_password")

	# 2. 提取当前用户的id
	user_id = session.get ("user_id")
	if not user_id:
		return jsonify ({
			"errno": 4001,
			"errmsg": "请先登录"
		})

	# 2. 判断旧密码与数据中的当前存储的密码是否相同
	user = db.session.query (User).filter (User.id == user_id, User.password_hash == old_password).first ()

	# 3. 如果相同，则修改
	if user:
		user.password_hash = new_password
		db.session.commit ()

		ret = {
			"errno": 0,
			"errmsg": "修改成功"
		}


	else:
		ret = {
			"errno": 4004,
			"errmsg": "原密码错误！"
		}

	# 4. 返回json
	return jsonify (ret)


@user_blu.route ("/user/user_pic_info")
def user_pic_info():
	user_id = session.get ("user_id")
	user = db.session.query (User).filter (User.id == user_id).first ()
	return render_template ("user_pic_info.html", user=user)


@user_blu.route ("/user/avatar", methods=["POST"])
def user_avatar():
	print (request.files)
	print ("这是request.files——-------")
	f = request.files.get ("avatar")

	if f:
		print (f.filename)
		# 存储到哪个路径呢？文件名叫什么呢？
		file_hash = hashlib.md5 ()
		# file_hash.update (f.filename.encode ("utf-8"))
		file_hash.update ((f.filename + time.ctime ()).encode ("utf-8"))
		file_name = file_hash.hexdigest () + f.filename[f.filename.rfind ("."):]

		local_file_path = os.path.join ("./static/index/images/sep/", file_name)

		# file_path = /static/index/upload/14729c72f17c584e91ced13c0f7606b3.jpg
		file_path = os.path.join ("./static/upload/",
		                          file_name)  # f.filename是你刚刚在浏览器选择的那个上传的图片的名字

		# 保存路径
		f.save (file_path)  # /static/index/upload/14729c72f17c584e91ced13c0f7606b3.jpg
		# 3. 将数据库中对应head_image字段值改为 刚刚保存的图片的路径

		# 将这个图片上传到七牛云
		qiniu_avatar_url = upload_image_to_qiniu (file_path, file_name)

		user = db.session.query (User).filter (User.id == session.get ("user_id")).first ()

		user.avatar_url = qiniu_avatar_url
		db.session.commit ()

		ret = {
			"errno": 0,
			"errmsg": "上传头像成功",
			# "avatar_url": file_path
		}


	else:
		ret = {
			"errno": 4005,
			"errmsg": "上传头像失败"
		}

	return jsonify (ret)


@user_blu.route ("/user/user_follow")
def user_follow():
	user_id = session.get ("user_id")

	if not user_id:
		return redirect (url_for ('index_blu.index'))

	user = db.session.query (User).filter (User.id == user_id).first ()
	if not user:
		return "非法操作"

	page = int (request.args.get ('page', 1))
	paginate = user.followers.paginate (page, 2, False)

	return render_template ("user_follow.html", user=user, paginate=paginate)


@user_blu.route ("/user/user_collection")
def user_collection():
	# 获取页码
	page = int (request.args.get ("page", 1))
	# 查询用户
	user_id = session.get ("user_id")
	user = db.session.query (User).filter (User.id == user_id).first ()
	# 查询用户收藏的文章

	paginate = user.collection_news.paginate (page, 1, False)
	return render_template ("user_collection.html", paginate=paginate)


@user_blu.route ("/user/user_news_release")
def user_news_release():
	category_list = db.session.query (Category).filter (Category.id != 1).all ()
	return render_template ("user_news_release.html", category_list=category_list)


@user_blu.route ("/user/release", methods=["POST"])
def new_release():
	title = request.form.get ("title")
	category = request.form.get ("category")
	digest = request.form.get ("digest")
	content = request.form.get ("content")
	f = request.files.get ("index_image")
	if title and category and digest and content:
		print (title, category, digest, content, f)
		news = News ()
		news.title = title
		news.category_id = category
		news.source = "个人发布"
		news.digest = digest
		news.content = content
		news.user_id = session.get ("user_id")
		news.status = 1  # 1代表 正在审核

		if f:
			file_hash = hashlib.md5 ()
			file_hash.update ((f.filename + time.ctime ()).encode ("utf-8"))
			file_name = file_hash.hexdigest () + f.filename[f.filename.rfind ("."):]

			# 将路径改为static/upload下
			path_file_name = "./static/upload/" + file_name

			# 用新的随机的名字当做图片的名字
			f.save (path_file_name)

			# 将这个图片上传到七牛云
			qiniu_image_url = upload_image_to_qiniu (path_file_name, file_name)
			news.index_image_url = qiniu_image_url

		db.session.add (news)
		db.session.commit ()
		ret = {
			"errno": 0,
			"errmsg": "成功"
		}

		return jsonify (ret)


@user_blu.route ("/user/user_news_list.html")
def user_news_list():
	# 查询当前用户
	user_id = session.get ("user_id")
	user = db.session.query (User).filter (User.id == user_id).first ()
	# 获取当前用户的所有新闻
	news = user.news
	return render_template ("user_news_list.html", news=news)
