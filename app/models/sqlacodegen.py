# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BusCalllog(Base):
    __tablename__ = 'bus_calllog'

    __uid__ = Column(INTEGER(100), index=True, comment='数据源')
    phone = Column(String(20), comment='手机号')
    sn = Column(String(100), primary_key=True, server_default=text("''"))
    source = Column(String(100), comment='任务编号')
    started_at = Column(DateTime, comment='外呼时间')
    talktimes = Column(INTEGER(11), comment='通话时长')
    status = Column(String(100), comment='意向等级')
    status_manual = Column(String(100), comment='人工分类')
    operator = Column(String(100), comment='话务员')
    team_name = Column(String(100), comment='分组')
    notes = Column(String(255), comment='备注')
    download_status = Column(String(20), comment='下载状态')
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')


class BusReport(Base):
    __tablename__ = 'bus_report'
    __table_args__ = (
        Index('索引 2', 'date', 'agent_name', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True, comment='编号')
    __uid__ = Column(INTEGER(11), comment='数据源')
    date = Column(Date, comment='日期')
    agent_name = Column(String(50), comment='坐席名字')
    company_name = Column(String(100), comment='公司名')
    outbound_area = Column(String(50), comment='外呼地区')
    outbound_count = Column(INTEGER(11), comment='外呼数量')
    connection_rate = Column(DECIMAL(5, 2), comment='接通率')
    connection_count = Column(INTEGER(11), comment='接通数量')
    screen_pop_count = Column(INTEGER(11), comment='可弹屏数')
    screen_pop_rate = Column(DECIMAL(5, 2), comment='可弹屏率')
    offline_screen_pop_count = Column(INTEGER(11), comment='未在线弹屏')
    offline_screen_pop_rate = Column(DECIMAL(5, 2), comment='未在线弹屏率')
    pushed_at = Column(INTEGER(11), comment='弹屏数量')
    pushed_rate = Column(DECIMAL(5, 2), comment='弹屏率')
    listened_at = Column(INTEGER(11), comment='监听数量')
    listened_rate = Column(DECIMAL(5, 2), comment='监听率')
    intervention_at = Column(INTEGER(11), comment='介入数量')
    intervention_rate = Column(DECIMAL(5, 2), comment='介入率')
    customer_count = Column(INTEGER(11), comment='客户数量')
    connected_customer_success_rate = Column(DECIMAL(5, 2), comment='接通客户成功率')
    intervention_customer_success_rate = Column(DECIMAL(5, 2), comment='介入客户成功率')
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class Dept(Base):
    __tablename__ = 'depts'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(200), nullable=False, server_default=text("''"))
    parentId = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    sort = Column(INTEGER(11))
    status = Column(INTEGER(11))
    leader = Column(String(100))
    mobile = Column(String(100))
    email = Column(String(100))
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Dict(Base):
    __tablename__ = 'dict'

    id = Column(INTEGER(11), primary_key=True)
    parentId = Column(INTEGER(11), index=True)
    remark = Column(String(100))
    name = Column(String(50))
    code = Column(String(50), index=True)
    status = Column(INTEGER(11))
    value = Column(String(500))
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(INTEGER(11), primary_key=True)
    parentId = Column(INTEGER(11), nullable=False)
    name = Column(String(100))
    icon = Column(String(100))
    routeName = Column(String(100))
    path = Column(String(100))
    component = Column(String(100))
    redirect = Column(String(100))
    type = Column(String(100))
    perm = Column(String(100))
    sort = Column(INTEGER(11))
    alwaysShow = Column(INTEGER(11))
    hidden = Column(INTEGER(11))
    keepAlive = Column(INTEGER(11))
    visible = Column(INTEGER(11))
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Role(Base):
    __tablename__ = 'roles'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(100))
    code = Column(String(50), unique=True)
    dataScope = Column(INTEGER(11))
    status = Column(INTEGER(11))
    sort = Column(INTEGER(11))
    menus = Column(String(100))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class Setting(Base):
    __tablename__ = 'setting'
    __table_args__ = {'comment': '可修改配置'}

    id = Column(INTEGER(11), primary_key=True)
    section = Column(String(64), nullable=False, comment='节')
    key = Column(String(64), nullable=False, unique=True, comment='键')
    value = Column(Text, nullable=False, comment='值')
    description = Column(Text)


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(120), unique=True)
    password = Column(String(120))
    roleIds = Column(String(120))
    nickname = Column(String(100))
    mobile = Column(String(100))
    genderLabel = Column(String(10))
    avatar = Column(String(100))
    email = Column(String(100))
    status = Column(INTEGER(11))
    deptId = Column(INTEGER(11))
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
