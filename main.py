from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from untils.common import show_top_6_news_style, show_news_status_name, show_news_status_style_name, \
	set_after_request_handle_fuc
from views import index_blu, passport_blu, user_blu, news_blu, admin_blu
from models import db

# 创建App对象
app = Flask (__name__)

# 注册蓝图
app.register_blueprint (index_blu)
app.register_blueprint (passport_blu)
app.register_blueprint (user_blu)
app.register_blueprint (news_blu)
app.register_blueprint (admin_blu)

# 加载配配信息
app.config.from_pyfile ("config.ini")

# db初始化配置App
db.init_app (app)

# 添加过滤器
app.add_template_filter (show_top_6_news_style)
app.add_template_filter (show_news_status_name)
app.add_template_filter (show_news_status_style_name)

# 设置钩子函数，可以在调用视图函数之前自动执行
set_after_request_handle_fuc (app)

# 添加数据库迁移工具
manager = Manager (app)
# 生成 migrate 对象，用来迁移数据库
migrate = Migrate (app, db)
# 添加db 命令
manager.add_command ('db', MigrateCommand)

if __name__ == '__main__':
	# app.run(port=7788)
	manager.run ()
