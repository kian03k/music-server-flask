# # -*- coding: utf-8 -*-
import uuid

name = "test_name"
namespace = "test_namespace"
# 基于时间戳 由MAC地址、当前时间戳、随机数生成。可以保证全球范围内的唯一性， 但MAC的使用同时带来安全性问题，局域网中可以使用IP来代替MAC。
print (type(uuid.uuid1()))

# print (uuid.uuid3(namespace, name))
# 基于随机数 由伪随机数得到，有一定的重复概率，该概率可以计算出来。
print (uuid.uuid4())
# print (uuid.uuid5(namespace, name))
import datetime
def get_age(birthday):
    # 本函数根据输入的8位出生年月日数据返回截至当天的年龄
    today = str(datetime.datetime.now().strftime('%Y-%m-%d')).split("-")
    # 取出系统当天的年月日数据为列表[年,月,日]
    n_monthandday = today[1] + today[2]
    # 将月日连接在一起
    n_year = today[0]
    # 单独列出当年年份
    r_monthandday = birthday[4:]
    # 取出输入日期的月与日
    r_year = birthday[:4]
    # 取出输入日期的年份

    if (int(n_monthandday) >= int(r_monthandday)):
        r_age = int(n_year) - int(r_year)
    else:
        r_age = int(n_year) - int(r_year) - 1
    return str(r_age)
