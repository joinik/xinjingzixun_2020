import hashlib
import os

from flask import jsonify, request, session, render_template, redirect, url_for

from models import db
from models.index import User, Follow
from . import user_blu


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
			follow = db.session.query (Follow).filter (Follow.followed_id == news_author_id,
			                                           Follow.follower_id == user_id).first ()
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

	return render_template ("user.html", nick_name=nick_name)


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

@user_blu.route("/user/password", methods=["POST"])
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


@user_blu.route("/user/user_pic_info")
def user_pic_info():
	return render_template("user_pic_info.html")


@user_blu.route("/user/avatar", methods=["POST"])
def user_avatar():
	print (request.files)
	print("这是啥——-------")
	f = request.files.get ("avatar")

	if f:
		print (f.filename)
		# 存储到哪个路径呢？文件名叫什么呢？
		file_hash = hashlib.md5 ()
		file_hash.update (f.filename.encode ("utf-8"))
		file_name = file_hash.hexdigest () + f.filename[f.filename.rfind ("."):]

		local_file_path = os.path.join ("/static/index/images/sep/", file_name)
		# file_path = /Users/wangmingdong/Desktop/个人简历7/app/static/upload/images/'dfa72f3bf97b709023b6136d4e5a0566.png
		file_path = os.path.join ("/static/index/images/sep/",
		                          file_name)  # f.filename是你刚刚在浏览器选择的那个上传的图片的名字

		print(file_path)


		f.save (file_path)  # a/b/c/123.png
		# 3. 将数据库中对应head_image字段值改为 刚刚保存的图片的路径

		user = db.session.query(User).filter(User.id == session.get("user_id")).first()

		user.avatar_url = local_file_path
		db.session.commit ()

		ret = {
			"errno": 0,
			"errmsg": "上传头像成功",
			"avatar_url": local_file_path
		}

		return jsonify (ret)
	else:
		ret = {
			"errno": 4005,
			"errmsg": "上传头像失败"
		}

		return jsonify (ret)