import pymysql.cursors
import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




# 连接数据库
connect = pymysql.Connect(
    host = '192.168.3.74',
    port = 50014,
    user = 'root',
    passwd = '10300',
    db = '4g_kpi_browsing',
    charset = 'utf8'
    )

# 获取游标
cursor = connect.cursor()


# 查询数据

sqlColName = "select column_name from information_schema.COLUMNS where table_name='lte_day'"     #查询列名称的sql语句
cursor.execute(sqlColName)                              #执行sqlColName 语句
colName = cursor.fetchall()                             #获取结果集中的所有行
print(colName)          


sql = "SELECT * FROM lte_day"
rowCount = cursor.execute(sql)

for row in range(1,rowCount):              
    print(cursor.fetchone())                          #取得结果集的下一行:     
print('共查找出', cursor.rowcount, '条数据')



# 关闭连接
cursor.close()
connect.close()




























'''
# 插入数据
sql = "INSERT INTO trade (name, account, saving) VALUES ( '%s', '%s', %.2f )"
data = ('雷军', '13512345678', 10000)
cursor.execute(sql % data)
connect.commit()
print('成功插入', cursor.rowcount, '条数据')

# 修改数据
sql = "UPDATE trade SET saving = %.2f WHERE account = '%s' "
data = (8888, '13512345678')
cursor.execute(sql % data)
connect.commit()
print('成功修改', cursor.rowcount, '条数据')

# 查询数据
sql = "SELECT name,saving FROM trade WHERE account = '%s' "
data = ('13512345678',)
cursor.execute(sql % data)
for row in cursor.fetchall():
    print("Name:%s\tSaving:%.2f" % row)
print('共查找出', cursor.rowcount, '条数据')

# 删除数据
sql = "DELETE FROM trade WHERE account = '%s' LIMIT %d"
data = ('13512345678', 1)
cursor.execute(sql % data)
connect.commit()
print('成功删除', cursor.rowcount, '条数据')

# 事务处理
sql_1 = "UPDATE trade SET saving = saving + 1000 WHERE account = '18012345678' "
sql_2 = "UPDATE trade SET expend = expend + 1000 WHERE account = '18012345678' "
sql_3 = "UPDATE trade SET income = income + 2000 WHERE account = '18012345678' "

try:
    cursor.execute(sql_1)  # 储蓄增加1000
    cursor.execute(sql_2)  # 支出增加1000
    cursor.execute(sql_3)  # 收入增加2000
except Exception as e:
    connect.rollback()  # 事务回滚
    print('事务处理失败', e)
else:
    connect.commit()  # 事务提交
    print('事务处理成功', cursor.rowcount)

'''





