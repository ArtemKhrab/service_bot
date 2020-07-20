from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from config import *

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


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    user_id = Column(String(25), unique=True)
    telephone = Column(String(25))
    username = Column(String(40))
    email = Column(String(30))
    master = Column(Boolean, nullable=False, default=False)
    placement_id = Column(Integer, ForeignKey(Placement.id))
    image = Column(Boolean, default=False)
    details = Column(String(255))
    city_id = Column(Integer, ForeignKey(City.id))
    card = Column(String(40))
    current_role = Column(Boolean, nullable=False, default=False)


class Saved_placement(Base):
    __tablename__ = 'saved_placement'

    id = Column(Integer, primary_key=True, autoincrement=True)
    placement_id = Column(Integer, ForeignKey(Placement.id))
    user_id = Column(String(25), ForeignKey(User.user_id))


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(25), ForeignKey(User.user_id))
    image = Column(String(50), nullable=False)
    description = Column(String(100))


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(25), ForeignKey(User.user_id))
    master_id = Column(String(25), ForeignKey(User.user_id))
    feedback = Column(String(512), nullable=False)


class Service_segment(Base):
    __tablename__ = 'service_segment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)


class Service_type(Base):
    __tablename__ = 'service_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    master_id = Column(String(25), ForeignKey(User.user_id))
    segment_id = Column(Integer, ForeignKey(Service_segment.id))
    money_cost = Column(String(6))
    time_cost = Column(String(5))


class Services(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    image = Column(String(50))
    master_id = Column(String(25), ForeignKey(User.user_id))
    money_cost = Column(String(5), default='0')


class Time_slot(Base):
    __tablename__ = 'time_slot'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    master_id = Column(String(25), ForeignKey(User.user_id))
    date = Column(Date, nullable=False)
    ordered = Column(Boolean, default=False)


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time_slot_id = Column(Integer, ForeignKey(Time_slot.id))
    client_id = Column(String(25), ForeignKey(User.user_id))
    master_id = Column(String(25), ForeignKey(User.user_id))
    service_id = Column(Integer, ForeignKey(Service_type.id))
    prepaid = Column(Boolean, nullable=False, default=False)
    done = Column(Boolean, nullable=False, default=False)
    canceled = Column(Boolean, nullable=False, default=False)


class Rating(Base):
    __tablename__ = 'rating'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(25), ForeignKey(User.user_id))
    master_id = Column(String(25), ForeignKey(User.user_id))
    points = Column(Integer)


class Saved_masters(Base):
    __tablename__ = 'saved_masters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(25), ForeignKey(User.user_id))
    master_id = Column(String(25), ForeignKey(User.user_id))


Base.metadata.create_all(engine)
