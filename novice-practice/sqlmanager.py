import pymysql


def get_conn():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="MyStrongPassword123!", database="vue", charset="utf8",
                           cursorclass=pymysql.cursors.DictCursor)
    if conn == None:
        print("数据库链接失败")
    else:
        print("数据库链接成功")
    cursor = conn.cursor()
    return conn, cursor


def close(conn, cursor):
    cursor.close()
    conn.close()


def queryPerson(list, name, password):
    info = '200'
    for item in list:
        if item["name"] == name and item['password'] == password:
            info = item
        else:
            pass
    return info


# def insert (student_list):
#     id1=int(input("请输入id："))
#     name1=input("请输入name：")
#     age1=int(input("请输入age："))
#     math1=int(input("请输入math："))
#     s1 = {
#         "id": id1,
#         "name": name1,
#         "age": age1,
#         "math": math1
#     }
#     student_list.append(s1)

def delete(t_list, id):
    temp = 0
    for item in t_list:
        temp += 1
        if item["id"] == id:
            del t_list[(temp - 1)]
            return True
    return False


def update(t_list, info):
    for item in t_list:
        if item["id"] == info["id"]:
            item['name'] = info['name']
            item['addr'] = info['addr']
            item['age'] = info['age']
            item['birth'] = info['birth']
            item['sex'] = info['sex']
        else:
            pass


def updateperson(t_list, info):
    for item in t_list:
        if item["id"] == info["id"]:
            item['name'] = info['name']
            item['addr'] = info['addr']
            item['age'] = info['age']
            item['birth'] = info['birth']
            item['sex'] = info['sex']
        else:
            pass


def query(t_list, name, password):
    info = 'null'
    for item in t_list:
        if item["name"] == name and item['password'] == password:
            info = item
        else:
            pass
    return info


def show(student_list):
    for item in student_list:
        print(item)


def read(conn, cursor):
    sql = "select * from users"
    cursor.execute(sql)
    conn.commit()
    student_list = cursor.fetchall()
    print(student_list)
    return student_list


def clear(conn, cursor):
    sql = "truncate users "
    cursor.execute(sql)
    conn.commit()


def write(conn, cursor, student_list):
    for item in student_list:
        # 列字段
        keys = ','.join(item.keys())
        # 行字段
        values = ', '.join(['%s'] * len(item))
        sql = 'insert into users ({keys}) values ({values})'.format(keys=keys, values=values)
        # 将字段的value转化为元祖存入
        cursor.execute(sql, tuple(item.values()))
        conn.commit()


def sort(student_list):
    new_list = []
    # student_list.sort(key=math)
    for item in student_list:
        new_list.append(list(item.values()))
    new_list.sort(key=lambda x: x[3], reverse=True)
    print(new_list)
