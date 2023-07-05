import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import copy

from dotenv import load_dotenv
load_dotenv('../.env')


# 创建数据库连接引擎
engine = create_engine("mysql+pymysql://root:ti999@mysql-dev.ofidc.com:3306/aicrm?charset=utf8")

# 创建会话工厂
Session = sessionmaker(bind=engine)
session = Session()

# 声明基类
Base = declarative_base()

# 定义模型类
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True)
    password = Column(String(120))
    roleIds = Column(String(120))
    nickname = Column(String(100))
    mobile = Column(String(100))
    genderLabel = Column(String(10))
    avatar = Column(String(100))
    email = Column(String(100))

field = ["username"]
# 使用load_only方法选择指定字段并存储为变量
result = session.query(User).all()

# result = session.query(User).options(
#     sqlalchemy.orm.load_only(*field)
# ).all()

# 打印结果
for user in result:
    entity = copy.deepcopy(user.__dict__)
    print(entity)
    print(f"user: {user.username} {user.password}")