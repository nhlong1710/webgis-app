from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash,check_password_hash
from geoalchemy2 import Geometry
import datetime

class Nha(db.Model):
    __tablename__ = "nha"
    id = db.Column(db.Integer, primary_key=True)
    geom = db.Column(Geometry('POLYGON'))
    diaChi = db.Column(db.String, nullable=False)
    loaiNha = db.Column(db.String, nullable=False)
    soTang = db.Column(db.Float, nullable=False)
    dienTich = db.Column(db.Float, nullable=False)

class BaiTap(db.Model):
    __tablename__ = "baiTap"
    id = db.Column(db.Integer, primary_key=True)
    geom = db.Column(Geometry('POLYGON'))
    diachi = db.Column(db.String, nullable=False)
    loainha = db.Column(db.String, nullable=False)
    sotang = db.Column(db.Float, nullable=False)
    dientich = db.Column(db.Float, nullable=False)

class Tree(db.Model):
    __tablename__="tree"
    id =db.Column(db.Integer, primary_key=True)
    geom=db.Column(Geometry('MULTIPOINT'))
    loaicay=db.Column(db.String, nullable=False)
    chieucao=db.Column(db.Float, nullable=False)

@login.user_loader
def load_user(id):
    return 1
