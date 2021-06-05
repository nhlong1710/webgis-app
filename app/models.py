from app import db
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import String
from geoalchemy2.types import Geometry

class Building(db.Model):
    __tablename__ = "building"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    addr_house = db.Column(db.String)
    typeHouse = db.Column(db.String)
    floor = db.Column(db.Integer)
    square = db.Column(db.Float)
    geom = db.Column(Geometry('POLYGON', srid=4326))

class Tree(db.Model):
    __tablename__ = "trees-point"
    id = db.Column(db.Integer,primary_key=True)
    loaicay = db.Column(db.String)
    chieucao = db.Column(db.String)
    geom = db.Column(Geometry('POLYGON', srid=4326))