import pymysql

def get_conn():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="hdsx", charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    if conn == None:
        print("数据库链接失败")
    else:
        print("数据库链接成功")
    cursor = conn.cursor()
    return conn, cursor


def close(conn, cursor):
    cursor.close()
    conn.close()

def menu():
    print("1.增加学生")
    print("2.删除学生")
    print("3.修改学生")
    print("4.查找学生")
    print("5.显示全部")
    print("6.显示成绩并排序")
    print('7.获取最高、最低、平均成绩')

def getSeason(season,student_list):

    if season == 1:
        insert(student_list)
    elif season == 2:
        delete(student_list)
    elif season == 3:
        update(student_list)
    elif season == 4:
        query(student_list)
    elif season == 5:
        show(student_list)
    elif season==6:
        sort(student_list)
    else:
        return 0

def insert (student_list):
    id1=int(input("请输入id："))
    name1=input("请输入name：")
    age1=int(input("请输入age："))
    math1=int(input("请输入math："))
    s1 = {
        "id": id1,
        "name": name1,
        "age": age1,
        "math": math1
    }
    student_list.append(s1)

def delete(student_list):
    id2=int(input("请输入要删除的学生的id："))
    temp=0
    for item in student_list:
        temp+=1
        if item["id"] == id2:
            break
    del student_list[(temp-1)]

def update(student_list):
    id2=int(input("请输入要更改的学生的id："))
    value=int(input("请输入正确的数值"))
    for item in student_list:
        if item["id"] == id2:
            item["math"]=value
        else:
            pass

def query(student_list):
    id2=int(input("请输入要查找的学生的id："))
    for item in student_list:
        if item["id"] == id2:
            print(item)
        else:
            pass
def show(student_list):
    for item in student_list:
        print(item)

def read(conn,cursor):
    sql= "select * from student"
    cursor.execute(sql)
    conn.commit()
    student_list=cursor.fetchall()
    print(student_list)
    return student_list

def clear(conn,cursor):
    sql="truncate student "
    cursor.execute(sql)
    conn.commit()

def write(conn,cursor,student_list):
    for item in student_list:
        # 列字段
        keys = ','.join(item.keys())
        # 行字段
        values = ', '.join(['%s'] * len(item))
        sql = 'insert into student ({keys}) values ({values})'.format(keys=keys, values=values)
        # 将字段的value转化为元祖存入
        cursor.execute(sql,tuple(item.values()))
        conn.commit()

def sort(student_list):
    new_list=[]
    # student_list.sort(key=math)
    for item in student_list:
        new_list.append(list(item.values()))
    new_list.sort(key=lambda x:x[3],reverse=True)
    print(new_list)

