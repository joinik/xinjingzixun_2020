from flask import jsonify, request, session, render_template

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
	print (news_author_id, "------->1")
	# 2. 提取当前登录用户的id
	user_id = session.get ("user_id")
	print (user_id, "------->2")

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
				"error": 0,
				"errmsg": "取消关注成功"
			}

			return jsonify (ret)

		except Exception as ret:
			db.session.rollback ()
			ret = {
				"error": 3004,
				"errmsg": "取消关注失败..."
			}

			return jsonify (ret)


@user_blu.route ("/user/center")
def user_center():
	return render_template ("user.html")


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
