from flask import Flask


# 创建App对象
app = Flask(__name__)

@app.route('/')
def index():
	return 'hello world'

if __name__ == '__main__':
    app.run(port=7788)
