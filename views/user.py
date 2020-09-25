from flask import jsonify

from . import user_blu


@user_blu.route("")
def xxx():
	ret = {
		"errno":0,
		"errmsg": "关注成功"
	}
	return jsonify(ret)