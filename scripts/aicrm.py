import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv('.env')

# 遍历文件夹下的所有Excel文件
folder_path = 'aicrm'  # 文件夹路径
file_extension = '.xlsx'  # 文件扩展名

# 建立数据库连接
conn = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))
print(conn)

# 遍历文件夹下的所有Excel文件
for file in os.listdir(folder_path):
    if file.endswith(file_extension):
        file_path = os.path.join(folder_path, file)

        # 读取Excel文件数据
        print(file_path)
        df = pd.read_excel(file_path)

        # 将数据插入到MySQL数据库中的表中
        table_name = 'bus_phone'  # 表名
        df.to_sql(name=table_name, con=conn, if_exists='append', index=True, index_label='id')

# 关闭数据库连接
conn.close()
