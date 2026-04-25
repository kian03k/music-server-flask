import string
import uuid
import random
import json
from flask import Flask, request, render_template, jsonify
from flask import Flask
from flask import jsonify
from flask_cors import CORS
import os
import mock
from unittest import mock
import sqlmanager
import uuid
import temp
import urllib

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"Access-Control-Allow-Origin": "*"}})
from flask import Flask, request
import sqlmanager  # 你优化后的数据库工具
import uuid
import urllib.parse

app = Flask(__name__)

# 获取数据库连接，获取游标
conn, cursor = sqlmanager.get_conn()
# 读取数据库并将数据传给列表
# total_list=sqlmanager.read(conn, cursor)

total_list = sqlmanager.read(conn, cursor)
if total_list ==():
    total_list=[]
# 执行操作
nowList = []


@app.route('/')
def hello_world():
    return 'test!'


@app.route('/api/user/getUser', methods=['GET', 'POST'])
def getUser():
    global total_list
    # params传参
    config = request.query_string
    url = str(config, 'utf-8')
    lists = url.split('&')
    obj = {}
    n = 0
    for li in lists:
        st = li.split('=')
        if (n == 0):
            # url编码以及反编码
            print(st[1])
            obj[st[0]] = urllib.parse.unquote(st[1])
        else:
            if st[1] == '':
                st1 = 0
            else:
                st1 = int(st[1])
            obj[st[0]] = st1
        n = n + 1
    infoList = []
    if obj['name'] == '':
        infoList = total_list
    else:
        for item in total_list:
            if (obj['name'] == item['name']):
                infoList.append(item)
    pageList = infoList[obj['limit'] * (obj['page'] - 1):obj['limit'] * obj['page']]
    return {
        'code': 20000,
        'count': len(infoList),
        'list': pageList
    }
@app.route('/api/person/get', methods=['GET', 'POST'])
def getPersonInfo():
    global nowList
    info = request.get_json()
    re_info = '100'
    for item in nowList:
        if item["token"] == info['id']:
            re_info = item['info']
        else:
            pass
    # print(re_info)
    return re_info

@app.route('/api/person/change', methods=['GET', 'POST'])
def changePersonInfo():
    global total_list
    info = request.get_json()
    sqlmanager.update(total_list, info)
    return {
        'code': 20000,
        'data': {
            'message': '编辑成功'
        }
    }



@app.route('/api/user/add', methods=['GET', 'POST'])
def createUser():
    global total_list
    info = request.get_json()
    info['id'] = str(uuid.uuid1())
    # print(info)
    if 'password' in info:
        pass
    else:
        info['password'] = 'abc'
    total_list.insert(0, info)
    # print(total_list)
    return {
        'code': 20000,
        'data': {
            'message': '添加成功'
        }
    }


@app.route('/api/user/del', methods=['GET', 'POST'])
def deleteUser():
    global total_list
    info = request.get_json()
    # print(info['id'])
    # print(total_list)
    if (info['id'] == ''):
        return {
            'code': -999,
            'message': '参数不正确'
        }
    else:
        sqlmanager.delete(total_list, info['id'])
        return {
            'code': 20000,
            'message': '删除成功'
        }


@app.route('/api/user/edit', methods=['GET', 'POST'])
def updateUser():
    global total_list
    info = request.get_json()
    sqlmanager.updateperson(total_list, info)
    return {
        'code': 20000,
        'data': {
            'message': '编辑成功'
        }
    }



@app.route('/api/home/logout', methods=['GET', 'POST'])
def logOut():
    global nowList
    global total_list
    info = request.get_json()
    nowList = [item for item in nowList if not item["token"] == info['id']]
    # 清空表数据
    sqlmanager.clear(conn, cursor)
    # print(total_list)
    # 将列表中的数据写入数据库
    sqlmanager.write(conn, cursor, total_list)
    return {
        'code': 20000,
        'data': {
            'message': '退出成功'
        }
    }




@app.route('/api/getsql', methods=['GET', 'POST'])
def writeSql():
    global total_list
    info = request.get_json()
    total_list.extend(info)
    # print(total_list)
    for item in total_list:
        age = temp.get_age(item['birth'].replace('-', ''))
        item['age'] = age
    # 清空表数据
    sqlmanager.clear(conn, cursor)
    # 将列表中的数据写入数据库
    sqlmanager.write(conn, cursor, info)
    # 释放资源
    # sqlmanager.close(conn, cursor)
    return {
        'code': 200
    }
@app.route('/api/permission/getMenu', methods=['GET', 'POST'])
def getMenu():
    info = request.get_json()
    # print(total_list)
    if (info['name'] == 'admin' and info['password'] == 'admin'):
        return {'code': 20000,
                'data': {
                    'menu': [
                        {
                            'path': "/home",
                            'name': "home",
                            'label': "首页",
                            'icon': "s-home",
                            'url': "Home.vue",
                        },
                        {
                            'path': '/search',
                            'name': 'search',
                            'label': '音乐搜索',
                            'icon': 'video-play',
                            'url': 'searchPage.vue'
                        },
                        {
                            'path': '/adminpage',
                            'name': 'adminpage',
                            'label': '数据展示',
                            'icon': 'video-play',
                            'url': 'adminPage.vue'
                        },
                        {
                            'path': '/user',
                            'name': 'user',
                            'label': '用户管理',
                            'icon': 'user',
                            'url': 'User.vue'
                        },
                        {
                            'path': '/songspage',
                            'name': 'songspage',
                            'label': '歌单详情',
                            'icon': 'user',
                            'url': 'songsPage.vue'
                        },
                        # {
                        #     'label': '个人中心',
                        #     'icon': 'location',
                        #     'children': [
                        #         {
                        #             'path': '/page1',
                        #             'name': 'page1',
                        #             'label': '页面1',
                        #             'icon': 'setting',
                        #             'url': 'PageOne.vue'
                        #         },
                        #         {
                        #             'path': '/page2',
                        #             'name': 'page2',
                        #             'label': '页面2',
                        #             'icon': 'setting',
                        #             'url': 'PageTwo.vue'
                        #         }
                        #     ]
                        # }

                    ],
                    'token': 2000224,
                    'message': '获取成功'
                }
                }
    elif sqlmanager.query(total_list, info['name'], info['password']) != 'null':
        token = str(uuid.uuid1())
        nowList.append({'info': sqlmanager.query(total_list, info['name'], info['password']), 'token': token})
        return {'code': 20000,
                'data': {
                    'menu': [
                        {
                            'path': "/home",
                            'name': "home",
                            'label': "首页",
                            'icon': "s-home",
                            'url': "Home.vue",
                        },
                        {
                            'path': '/songspage',
                            'name': 'songspage',
                            'label': '歌单详情',
                            'icon': 'user',
                            'url': 'songsPage.vue'
                        },
                        {
                            'path': '/search',
                            'name': 'search',
                            'label': '音乐搜索',
                            'icon': 'video-play',
                            'url': 'searchPage.vue'
                        },

                        {
                            'label': '个人中心',
                            'icon': 'location',
                            'children': [
                                {
                                    'path': '/page1',
                                    'name': 'page1',
                                    'label': '页面1',
                                    'icon': 'setting',
                                    'url': 'PageOne.vue'
                                },
                                {
                                    'path': '/page2',
                                    'name': 'page2',
                                    'label': '页面2',
                                    'icon': 'setting',
                                    'url': 'PageTwo.vue'
                                }
                            ]
                        }

                    ],
                    'token': token,
                    'message': '获取成功'
                }
                }
    else:
        return {
            'code': -999,
            'data': {
                'message': '密码错误'
            }
        }
if __name__ == '__main__':
    app.run()