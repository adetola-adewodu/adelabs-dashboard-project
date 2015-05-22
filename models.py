__author__ = 'Adetola'

"""
Models for Web Service
"""
from sqlalchemy import Column, Integer, Float, String, DECIMAL, Date, Time
import datetime
from lwazi_web_service import db

# Trip Model
class Trip(db.Model):
    id = Column(Integer, primary_key=True)
    drivername = Column(String(255))
    type = Column(String(255))
    date = Column(Date)
    tripdate = Column(Date,default=datetime.datetime)
    triptime = Column(Time, default=datetime.time)
    datetime = Column(Date,default=datetime.datetime)
    tripduration = Column(Integer)
    dayofweek= Column(String(255))
    description= Column(String(255))
    trip = Column(String(255))
    gross_fare = Column("decimal_grossfare", DECIMAL(precision=9,scale=2))
    commission = Column("decimal_commission", DECIMAL(precision=9,scale=2))
    total_payment = Column("decimal_totalpayment",DECIMAL(precision=9,scale=2))


# Schedule Model
class Schedule(db.Model):
    id = Column(Integer, primary_key=True)
    scheduledate = Column(Date,default=datetime.datetime)
    drivername = Column(String(255))
    day = Column(Integer)
    dayofweek  = Column(String(255))
    position  = Column(String(255))
    location  = Column(String(255))
    site  = Column(String(255))
    starttime = Column(Time, default=datetime.time)
    endtime = Column(Time, default=datetime.time)
    unpaidbreak = Column(Integer)
    totalhours = Column(Integer)
    hourlyrate = Column("decimal_hourlyrate",DECIMAL(precision=9,scale=2))
    laborcost = Column("decimal_laborcost",DECIMAL(precision=9,scale=2))
    notes = Column(String(255))
