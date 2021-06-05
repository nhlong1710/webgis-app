import datetime
from app import db
from flask import Flask, render_template, request,redirect,flash,url_for
from app import login
from werkzeug.security import generate_password_hash,check_password_hash
from geoalchemy2 import Geometry
from flask_login import UserMixin
class Nha(db.Model):
   __tablename__="nha"
   id =db.Column(db.Integer, primary_key=True)
   geom=db.Column(Geometry('POLYGON'))
   diachi=db.Column(db.String, nullable=False)
   loainha=db.Column(db.String, nullable=False)
   sotang=db.Column(db.String, nullable=False)
   dientich=db.Column(db.String, nullable=False)

class Tree(db.Model):
    __tablename__="tree"
    id =db.Column(db.Integer, primary_key=True)
    geom=db.Column(Geometry('MULTIPOINT'))
    loaicay=db.Column(db.String, nullable=False)
    chieucao=db.Column(db.Float, nullable=False)
@login.user_loader
def load_user(id):
    return 1
