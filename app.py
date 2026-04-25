import random
import urllib.parse
import uuid
import jwt
import datetime
from flask import Flask, request
from flask_cors import CORS
import sqlmanager
import sys
import signal

# ===================== 初始化配置 =====================
app = Flask(__name__)
CORS(app, supports_credentials=True)

# JWT 配置
SECRET_KEY = "music-platform-2025"



# ===================== 工具函数 =====================
def get_age(birth_str):
    try:
        birth_year = int(birth_str[:4])
        return 2025 - birth_year
    except:
        return 0

# ===================== 基础接口 =====================
@app.route('/')
def hello_world():
    return 'test!'

# ===================== 用户管理 =====================
@app.route('/api/user/getUser', methods=['GET', 'POST'])
def getUser():
    args = request.args
    name = args.get('name', '')
    page = int(args.get('page', 1))
    limit = int(args.get('limit', 10))

    all_users = sqlmanager.get_all_users()

    if name:
        info_list = [u for u in all_users if name in u['name']]
    else:
        info_list = all_users

    start = limit * (page - 1)
    end = limit * page
    page_list = info_list[start:end]

    return {
        'code': 20000,
        'count': len(info_list),
        'list': page_list
    }

@app.route('/api/person/get', methods=['POST'])
def getPersonInfo():
    data = request.get_json()
    user_id = data.get('id')
    all_users = sqlmanager.get_all_users()

    for item in all_users:
        if str(item['id']) == str(user_id):
            return item
    return '100'

@app.route('/api/person/change', methods=['POST'])
def changePersonInfo():
    info = request.get_json()
    sqlmanager.update_user(info)
    return {
        'code': 20000,
        'data': {'message': '编辑成功'}
    }

@app.route('/api/user/add', methods=['POST'])
def createUser():
    info = request.get_json()
    info['id'] = str(uuid.uuid1())

    if 'password' not in info:
        info['password'] = 'abc'

    if 'birth' in info:
        info['age'] = get_age(info['birth'])

    sqlmanager.add_user(info)
    return {
        'code': 20000,
        'data': {'message': '添加成功'}
    }

@app.route('/api/user/del', methods=['POST'])
def deleteUser():
    data = request.get_json()
    user_id = data.get('id', '')
    if not user_id:
        return {'code': -999, 'message': '参数不正确'}

    sqlmanager.delete_user(user_id)
    return {'code': 20000, 'message': '删除成功'}

@app.route('/api/user/edit', methods=['POST'])
def updateUser():
    info = request.get_json()
    sqlmanager.update_user(info)
    return {
        'code': 20000,
        'data': {'message': '编辑成功'}
    }

# ===================== 登录 / 权限 =====================
@app.route('/api/permission/getMenu', methods=['POST'])
def getMenu():
    data = request.get_json()
    username = data.get('name', '')
    password = data.get('password', '')

    if not username or not password:
        return {'code': -999, 'message': '用户名或密码不能为空'}

    user = sqlmanager.login_user(username, password)
    if not user:
        return {'code': -999, 'message': '用户名或密码错误'}

    payload = {
        "id": user['id'],
        "name": user['name'],
        "role": user.get('role', 'user'),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    if user.get('role') == 'admin':
        menu = [
            {"path": "/home", "name": "home", "label": "首页", "icon": "s-home", "url": "Home.vue"},
            {"path": "/search", "name": "search", "label": "音乐搜索", "icon": "video-play", "url": "searchPage.vue"},
            {"path": "/adminpage", "name": "adminpage", "label": "数据展示", "icon": "video-play", "url": "adminPage.vue"},
            {"path": "/user", "name": "user", "label": "用户管理", "icon": "user", "url": "User.vue"},
            {"path": "/songspage", "name": "songspage", "label": "歌单详情", "icon": "user", "url": "songsPage.vue"}
        ]
    else:
        menu = [
            {"path": "/home", "name": "home", "label": "首页", "icon": "s-home", "url": "Home.vue"},
            {"path": "/search", "name": "search", "label": "音乐搜索", "icon": "video-play", "url": "searchPage.vue"},
            {"path": "/songspage", "name": "songspage", "label": "歌单详情", "icon": "user", "url": "songsPage.vue"},
            {
                "label": "个人中心", "icon": "location",
                "children": [
                    {"path": "/page1", "name": "page1", "label": "页面1", "icon": "setting", "url": "PageOne.vue"},
                    {"path": "/page2", "name": "page2", "label": "页面2", "icon": "setting", "url": "PageTwo.vue"}
                ]
            }
        ]

    return {
        "code": 20000,
        "data": {"token": token, "menu": menu, "message": "登录成功"}
    }

@app.route('/api/home/logout', methods=['POST'])
def logOut():
    return {'code': 20000, 'data': {'message': '退出成功'}}

# ===================== 批量导入 =====================
@app.route('/api/getsql', methods=['POST'])
def writeSql():
    info = request.get_json()
    if not isinstance(info, list):
        return {'code': 500, 'msg': '数据格式错误'}

    for item in info:
        if 'birth' in item:
            item['age'] = get_age(item['birth'])
        sqlmanager.add_user(item)

    return {'code': 200}

# ===================== 首页图表数据 =====================
@app.route('/api/home/getData', methods=['GET', 'POST'])
def getHomeData():
    def getRandom():
        return random.randint(100, 8000)

    order_data = [
        {'苹果': getRandom(), 'vivo': getRandom(), 'oppo': getRandom(),
         '魅族': getRandom(), '三星': getRandom(), '小米': getRandom()}
        for _ in range(7)
    ]

    return {
        'code': 20000,
        'data': {
            'videoData': [
                {'name': '小米', 'value': 2999},
                {'name': '苹果', 'value': 5999},
                {'name': 'vivo', 'value': 1500},
                {'name': 'oppo', 'value': 1999},
                {'name': '魅族', 'value': 2200},
                {'name': '三星', 'value': 4500}
            ],
            'userData': [
                {'date': '周一', 'new': 5, 'active': 200},
                {'date': '周二', 'new': 10, 'active': 500},
                {'date': '周三', 'new': 12, 'active': 550},
                {'date': '周四', 'new': 60, 'active': 800},
                {'date': '周五', 'new': 65, 'active': 550},
                {'date': '周六', 'new': 53, 'active': 770},
                {'date': '周日', 'new': 33, 'active': 170}
            ],
            'orderData': {
                'date': ['20191001', '20191002', '20191003', '20191004', '20191005', '20191006', '20191007'],
                'data': order_data
            },
            'tableData': [
                {'name': 'oppo', 'todayBuy': 500, 'monthBuy': 3500, 'totalBuy': 22000},
                {'name': 'vivo', 'todayBuy': 300, 'monthBuy': 2200, 'totalBuy': 24000},
                {'name': '苹果', 'todayBuy': 800, 'monthBuy': 4500, 'totalBuy': 65000},
                {'name': '小米', 'todayBuy': 1200, 'monthBuy': 6500, 'totalBuy': 45000},
                {'name': '三星', 'todayBuy': 300, 'monthBuy': 2000, 'totalBuy': 34000},
                {'name': '魅族', 'todayBuy': 350, 'monthBuy': 3000, 'totalBuy': 22000}
            ]
        }
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True,use_reloader=True)
    # app.run(host='0.0.0.0', debug=True)