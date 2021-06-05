from app import app
from app.models import *
from app.form import *
from flask import Flask, render_template, request,redirect,flash,url_for
from sqlalchemy.sql.functions import current_user
from flask_login.utils import *
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_ , and_, func
from flask.helpers import flash, url_for
from datetime import *
from datetime import date
from flask.json import jsonify
import json

@app.route("/api/v1/geom")
def postGIS_api_geom():
    """Return geom column"""
    nhaGeoms = db.session.query(func.ST_AsGeoJSON(func.ST_Transform\
    (Nha.geom,4326)).label('geometry')).all()
    nhaFeature=[]
    for nhaGeom in nhaGeoms:
        geometry_temp = json.dumps(nhaGeom.geometry)
        nhaFeature.append(geometry_temp)
    return jsonify({
                "features": nhaFeature
    })
@app.route("/api/v1/postGIS")
def postGIS_api():
    """Return feature in nha table"""

    nhas = db.session.query( Nha.id,Nha.diachi, Nha.loainha, Nha.sotang,\
    func.ST_AsGeoJSON(func.ST_Transform(Nha.geom,4326)).label('geometry')).all()
    nhaFeature=[]
    for nha in nhas:
        properties_temp = {
            "diaChi": nha.diachi,
            "loaiNha": nha.loainha,
            "soTang": nha.sotang,
            "id": nha.id
        }
        geometry_temp = json.dumps(nha.geometry)
        feature = {
            "type": "Feature",
            "properties": properties_temp,
            "geometry": geometry_temp
        }
        nhaFeature.append(feature)

    return jsonify({
                #"type":"FeatureCollection",
                "features": nhaFeature

        })

@app.route("/")
def index():
    return "hello"
