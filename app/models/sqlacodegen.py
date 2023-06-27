# coding: utf-8
from sqlalchemy import Column, DateTime, Enum, Float, Index, JSON, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Setting(Base):
    __tablename__ = 'setting'
    __table_args__ = {'comment': '可修改配置'}

    id = Column(INTEGER(11), primary_key=True)
    section = Column(String(64), nullable=False, comment='节')
    key = Column(String(64), nullable=False, unique=True, comment='键')
    value = Column(Text, nullable=False, comment='值')
    description = Column(Text)


class Overview(Base):
    __tablename__ = 'overview'

    id = Column(INTEGER(11), primary_key=True)
    value = Column(Float, nullable=False)
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    roleIds = Column(String(120), nullable=False)
    nickname = Column(String(100), nullable=False)
    mobile = Column(String(100), nullable=False)
    genderLabel = Column(String(10), nullable=False)
    avatar = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    status = Column(INTEGER(11), nullable=True)
    deptId = Column(INTEGER(11), nullable=True)
    create_time = Column(String(19), nullable=False)
    update_time = Column(String(19), nullable=False)

    def create(self):
        self.add(self)
        self.commit()
        return self


class Dept(Base):
    __tablename__ = 'depts'

    id = Column(INTEGER(11), primary_key=True)
    parentId = Column(INTEGER(11), nullable=True)
    name = Column(String(200), nullable=False)
    sort = Column(INTEGER(11), nullable=True)
    status = Column(INTEGER(11), nullable=True)
    leader = Column(String(100), nullable=False)
    mobile = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    create_time = Column(String(19), nullable=False)
    update_time = Column(String(19), nullable=False)

    def create(self):
        self.add(self)
        self.commit()
        return self


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(INTEGER(11), primary_key=True)
    parentId = Column(INTEGER(11), nullable=True)
    name = Column(String(200), nullable=False)
    icon = Column(String(100), nullable=True)
    routeName = Column(String(100), nullable=True)
    path = Column(String(100), nullable=True)
    component = Column(String(100), nullable=True)
    redirect = Column(String(100), nullable=True)
    type = Column(String(100), nullable=True)
    perm = Column(String(200), nullable=False)
    sort = Column(INTEGER(11), nullable=True)
    hidden = Column(INTEGER(11), nullable=True)
    keepAlive = Column(INTEGER(11), nullable=True)
    alwaysShow = Column(INTEGER(11), nullable=True)
    visible = Column(INTEGER(11), primary_key=True)
    create_time = Column(String(19), nullable=False)
    update_time = Column(String(19), nullable=False)

    def create(self):
        self.add(self)
        self.commit()
        return self


class Role(Base):
    __tablename__ = 'roles'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False)
    menus = Column(String(100), nullable=False)
    sort = Column(INTEGER(11), nullable=True)
    status = Column(INTEGER(11), nullable=True)
    dataScope = Column(INTEGER(11), nullable=True)
    create_time = Column(String(19), nullable=False)
    update_time = Column(String(19), nullable=False)

    def create(self):
        self.add(self)
        self.commit()
        return self


class Dict(Base):
    __tablename__ = 'dict'

    id = Column(INTEGER(11), primary_key=True)
    parentId = Column(INTEGER(11), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False)
    status = Column(INTEGER(11), nullable=False)
    value = Column(String(500), nullable=False)
    remark = Column(String(100), nullable=False)
    create_time = Column(String(19), nullable=False)
    update_time = Column(String(19), nullable=False)

    def create(self):
        self.add(self)
        self.commit()
        return self


class Report(Base):
    __tablename__ = 'report'

    id = Column(INTEGER(11), primary_key=True)
    uid = Column(INTEGER(11), nullable=False)
    date = Column(String(10), nullable=False)
    agent_name = Column(String(50), nullable=False)
    company_name = Column(String(100), nullable=False)
    outbound_area = Column(String(50), nullable=False)
    outbound_count = Column(INTEGER(11), nullable=False)
    connection_rate = Column(INTEGER(11), nullable=False)
    connection_count = Column(INTEGER(11), nullable=False)
    screen_pop_count = Column(INTEGER(11), nullable=False)
    screen_pop_rate = Column(INTEGER(11), nullable=False)
    offline_screen_pop_count = Column(INTEGER(11), nullable=False)
    offline_screen_pop_rate = Column(INTEGER(11), nullable=False)
    pushed_at = Column(INTEGER(11), nullable=False)
    pushed_rate = Column(INTEGER(11), nullable=False)
    listened_at = Column(INTEGER(11), nullable=False)
    listened_rate = Column(INTEGER(11), nullable=False)
    intervention_at = Column(INTEGER(11), nullable=False)
    intervention_rate = Column(INTEGER(11), nullable=False)
    customer_count = Column(INTEGER(11), nullable=False)
    connected_customer_success_rate = Column(INTEGER(11), nullable=False)
    intervention_customer_success_rate = Column(INTEGER(11), nullable=False)
    create_time = Column(String(19), nullable=False)
    update_time = Column(String(19), nullable=False)

    def create(self):
        self.add(self)
        self.commit()
        return self


class Calllog(Base):
    __tablename__ = 'calllog'

    id = Column(INTEGER(11), primary_key=True)
    uid = Column(INTEGER(11), nullable=False)
    phone_number = Column(String(20), nullable=False)
    task_number = Column(INTEGER(11), nullable=False)
    call_time = Column(String(19), nullable=False)
    call_duration = Column(INTEGER(11), nullable=False)
    intention_level = Column(String(100), nullable=False)
    operator = Column(String(100), nullable=False)
    group_name = Column(String(100), nullable=False)
    notes = Column(String(255), nullable=False)
    download_status = Column(String(100), nullable=False)
    create_time = Column(String(19), nullable=False)
    update_time = Column(String(19), nullable=False)