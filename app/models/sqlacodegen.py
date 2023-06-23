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
    roles = Column(String(120), nullable=False)

    def create(self):
        self.add(self)
        self.commit()
        return self


class Report(Base):
    __tablename__ = 'report'

    id = Column(INTEGER(11), primary_key=True)
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