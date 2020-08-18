from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from config import *
import datetime
from datetime import timedelta

Base = declarative_base()


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), nullable=False)


class Placement(Base):
    __tablename__ = 'placement'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    longitude = Column(String(10), nullable=False)
    latitude = Column(String(10), nullable=False)
    address = Column(String(100))
    telephone = Column(String(25))
    image = Column(String(50))
    instagram_url = Column(String(50))
    city_id = Column(Integer, ForeignKey(City.id))


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    user_id = Column(String(25), unique=True)
    telephone = Column(String(25))
    username = Column(String(40))
    email = Column(String(30))
    city_id = Column(Integer, ForeignKey(City.id))


class Master(Base):
    __tablename__ = 'master'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    user_id = Column(String(25), unique=True)
    telephone = Column(String(25))
    username = Column(String(40))
    email = Column(String(30))
    city_id = Column(Integer, ForeignKey(City.id))
    placement_id = Column(Integer, ForeignKey(Placement.id))
    image = Column(Boolean, default=False)
    details = Column(String(255))
    card = Column(String(40))
    cur_role = Column(Boolean, default=True)


class User_role(Base):
    __tablename__ = 'user_role'

    id = Column(String(25), primary_key=True)
    master = Column(Boolean, default=False)
    client_admin = Column(Boolean, default=False)
    master_admin = Column(Boolean, default=False)
    super_admin = Column(Boolean, default=False)


class Saved_placement(Base):
    __tablename__ = 'saved_placement'

    id = Column(Integer, primary_key=True, autoincrement=True)
    placement_id = Column(Integer, ForeignKey(Placement.id))
    user_id = Column(String(25), ForeignKey(Client.user_id))


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(25), ForeignKey(Master.user_id))
    image = Column(String(50), nullable=False)
    description = Column(String(100))


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(25), ForeignKey(Client.user_id))
    client_id_master_acc = Column(String(25), ForeignKey(Master.user_id))
    master_id = Column(String(25), ForeignKey(Master.user_id))
    feedback = Column(String(512), nullable=False)


class Service_segment(Base):
    __tablename__ = 'service_segment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)


class Service_type(Base):
    __tablename__ = 'service_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    master_id = Column(String(25), ForeignKey(Master.user_id))
    segment_id = Column(Integer, ForeignKey(Service_segment.id))
    money_cost = Column(String(6))
    time_cost = Column(String(5))


class Services(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    image = Column(String(50))
    master_id = Column(String(25), ForeignKey(Master.user_id))
    money_cost = Column(String(5), default='0')


class Working_days(Base):
    __tablename__ = 'working_days'

    id = Column(Integer, primary_key=True, autoincrement=True)
    day_name = Column(String(2), nullable=False)
    master_id = Column(String(25), ForeignKey(Master.user_id), nullable=False)
    working_hours = Column(String(11))
    day_num = Column(Integer, nullable=False)
    non_active = Column(Boolean, default=False)


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(25), ForeignKey(Client.user_id))
    client_id_master_acc = Column(String(25), ForeignKey(Master.user_id))
    master_id = Column(String(25), ForeignKey(Master.user_id))
    service_id = Column(Integer, ForeignKey(Service_type.id))
    day_id = Column(Integer, ForeignKey(Working_days.id))
    order_date = Column(Date)
    time = Column(String(11))
    prepaid = Column(Boolean, default=False)
    done = Column(Boolean, default=False)
    money_cost = Column(String(6))
    next_week = Column(Boolean)
    g_calendar_id = Column(String(100))
    self_res = Column(Boolean, default=False)
    description = Column(String(256))
    order_free_time = Column(Boolean, default=False)
    canceled_by_client = Column(Boolean, default=False)
    canceled_by_master = Column(Boolean, default=False)
    canceled_by_system = Column(Boolean, default=False)


class Rating(Base):
    __tablename__ = 'rating'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(25), ForeignKey(Client.user_id))
    client_id_master_acc = Column(String(25), ForeignKey(Master.user_id))
    master_id = Column(String(25), ForeignKey(Master.user_id))
    points = Column(Integer)


class Saved_masters(Base):
    __tablename__ = 'saved_masters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(25), ForeignKey(Client.user_id))
    client_id_master_acc = Column(String(25), ForeignKey(Master.user_id))
    master_id = Column(String(25), ForeignKey(Master.user_id))


class Updates(Base):
    __tablename__ = 'updates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    daily = Column(Boolean, default=False)
    weekly = Column(Boolean, default=False)
    date = Column(DateTime, default=DateTime)
    done = Column(Boolean, default=False)


Base.metadata.create_all(engine)