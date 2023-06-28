import pymssql

# 可以进入 connect 方法里面查看更多参数
#conn=pymssql.connect(server='frp.ofidc.com', port=51233, user='sa', password='IDpv5vJJR5ujH5sQhHM1LQ==', database='JitonData')
conn=pymssql.connect(server='frp.ofidc.com', port=51233, user='ofidc', password='Public@8080*', database='JitonData')

# 游标使用注意事项
# 一个连接一次只能有一个游标的查询处于活跃状态，如下：
cursor_1 = conn.cursor()
cursor_1.execute('SELECT TOP 1000 * FROM [JitonData].[dbo].[hisdata_E4P01]')

print("all persons")
print(cursor_1.fetchall())  # 显示出的是cursor_2游标查询出来的结果

