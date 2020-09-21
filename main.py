from flask import Flask
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from views import index_blu
from models import db




# 创建App对象
app = Flask(__name__)

# 加载配配信息
app.config.from_pyfile('config.ini')
# 注册蓝图
app.register_blueprint(index_blu)

# 添加数据库迁移工具
manager = Manager(app)
#生成 migrate 对象，用来迁移数据库
migrate = Migrate(manager, db)
# 添加db 命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.run(port=7788)
