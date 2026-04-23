import homework2
import sqlmanager
"""
学生信息
一、学生信息
id
name
age
math
二、
增加学生
删除学生
修改学生
查找学生
显示全部
三、
要求数据要对数据库做增删改查
四、
做成WEB版
"""
# 显示菜单
homework2.menu()
# 获取数据库连接，获取游标
conn, cursor=homework2.get_conn()
# 读取数据库并将数据传给列表
student_list=homework2.read(conn, cursor)
# 执行操作
num=1
while num>=1:
    num = int(input("请输入要选择的操作:"))
    homework2.getSeason(num,student_list)
# 清空表数据
homework2.clear(conn,cursor)
# 将列表中的数据写入数据库
homework2.write(conn,cursor,student_list)
# 释放资源
homework2.close(conn, cursor)