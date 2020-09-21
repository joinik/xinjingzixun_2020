from flask import Flask

from views import index_blu
from models import db




# 创建App对象
app = Flask(__name__)

# 加载配配信息
app.config.from_pyfile('config.ini')
# 注册蓝图
app.register_blueprint(index_blu)

if __name__ == '__main__':
    app.run(port=7788)
