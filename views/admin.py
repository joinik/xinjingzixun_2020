from flask import render_template, request, jsonify

from models import db
from models.index import User, Category
from . import admin_blu


@admin_blu.route ("/admin")
def admin():
	return render_template ("admin/index.html")


@admin_blu.route ("/admin/user_count.html")
def user_count():
	return render_template ("admin/user_count.html")


@admin_blu.route ("/admin/user_list.html")
def user_list():
	page = int (request.args.get ("page", 1))

	# 查询用户数据 列表
	pag_users = db.session.query (User).filter ().paginate (page, 3, False)

	if pag_users:
		pass
	return render_template ("admin/user_list.html", pages=pag_users)


@admin_blu.route ("/admin/news_edit.html")
def news_edit():
	return render_template ("admin/news_edit.html")


@admin_blu.route ("/admin/news_edit_detail.html")
def news_edit_detail():
	return render_template ("admin/news_edit_detail.html")


@admin_blu.route ("/admin/news_review.html")
def news_review():
	return render_template ("admin/news_review.html")


@admin_blu.route ("/admin/news_review_detail.html")
def news_review_detail():
	return render_template ("admin/news_review_detail.html")


@admin_blu.route ("/admin/news_type.html")
def news_type():
	news_types = db.session.query (Category).filter (Category.id != 1).all ()
	return render_template ("admin/news_type.html", news_types=news_types)


@admin_blu.route ("/admin/news_type", methods=["POST"])
def news_type_edit():
	# 提取参数
	category_id = request.json.get ("id")
	category_name = request.json.get ("name")

	# 如果有id，那么就是表示编辑，否则认为是添加
	if category_id:
		# 编辑
		category = db.session.query (Category).filter (Category.id == category_id).first ()
		if not category:
			ret = {
				"errno": 5001,
				"errmsg": "没有要修改的分类"
			}

			return jsonify (ret)

		category.name = category_name
		db.session.commit ()
		ret = {
			"errno": 0,
			"errmsg": "成功"
		}

		return jsonify (ret)

	else:
		# 添加
		new_category = Category ()
		new_category.name = category_name
		db.session.add (new_category)
		db.session.commit ()
		ret = {
			"errno": 0,
			"errmsg": "成功"
		}

		return jsonify (ret)

