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
    sn = Column(String(100), primary_key=True, server_default=text("''"), comment='\t流水sn')
    source = Column(String(100), comment='任务编号')
    started_at = Column(DateTime, comment='外呼时间')
    talktimes = Column(INTEGER(11), comment='通话时长')
    status = Column(String(100), comment='意向等级')
    status_manual = Column(String(100), comment='人工分类')
    operator = Column(String(100), comment='话务员')
    user_name = Column(String(100), comment='子账号')
    team_name = Column(String(100), comment='分组')
    mark = Column(String(255), comment='备注')
    download_time = Column(DateTime, comment='下载时间(首次)')
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')


class BusDialtask(Base):
    __tablename__ = 'bus_dialtask'

    dial_task_main_id = Column(String(255), comment='任务ID')
    __uid__ = Column(INTEGER(11), comment='主账号id')
    user_name = Column(String(255), comment='子账号名称')
    source = Column(String(255), comment='任务名称')
    dial_task_main_sn = Column(String(255), primary_key=True, server_default=text("''"), comment='任务唯一编号')
    status = Column(String(50), comment='外呼状态；0：发送中 1：已发送 4：暂停发送')
    user_sn = Column(String(255), comment='子账号唯一编号')
    team_sn = Column(String(255), comment='团队编号')
    team_name = Column(String(255), comment='团队名称')
    created_at = Column(DateTime, comment='创建时间')
    last_modify = Column(DateTime, comment='最后修改时间')
    started_at = Column(DateTime, comment='开始时间')
    stopped_at = Column(DateTime, comment='结束时间')
    total_count = Column(INTEGER(11), comment='总呼数量')
    send_count = Column(INTEGER(11), comment='已呼数量')
    unsend_count = Column(INTEGER(11), comment='未呼数量')
    success = Column(INTEGER(11), comment='成功数')
    fail = Column(INTEGER(11), comment='失败数')
    stops = Column(INTEGER(11), comment='暂停数')
    percent = Column(String(50), comment='成功率')
    project_sn = Column(String(255), comment='项目编号')
    project_caption = Column(String(255), comment='项目名称')
    operator = Column(String(255), comment='创建人')
    percentage = Column(String(255), comment='预测式倍率（6.6版本添加）')
    task_type = Column(INTEGER(11), comment='任务类型；0：AI外呼，1：人工预测式，2：人工预览式，3：AI预测式（6.6版本添加）')
    ai_distribution_type = Column(String(255), comment='预览式；1：抢拨，0：平均（6.6版本添加）')
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='记录创建时间')
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='记录更新')


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
    typeCode = Column(String(50), index=True)
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
