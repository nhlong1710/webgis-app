from flask import render_template, request, flash, redirect, url_for, jsonify
from app import app
from app.models import *
from app.form import *
#from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from sqlalchemy import and_
import requests
import json

# #----------GET API for leaflet from postGIS ----------------
from sqlalchemy import func
import json

# API get geom column from nha table
@app.route("/api/v1/geom")
def postGIS_api_geom():
    """Return geom column"""
    nhaGeoms = db.session.query(func.ST_AsGeoJSON(func.ST_Transform\
    (Nha.geom,4326)).label('geometry')).all()
    nhaFeature=[]
    for nhaGeom in nhaGeoms:
        geometry_temp = json.loads(nhaGeom.geometry)
        nhaFeature.append(geometry_temp)
    return jsonify({
                "features": nhaFeature
    })

# API get data from nha table
@app.route("/api/v1/postGIS")
def postGIS_api():
    """Return feature in nha table"""

    nhas = db.session.query(Nha.id, Nha.diaChi, Nha.loaiNha, Nha.soTang, Nha.dienTich,\
    func.ST_AsGeoJSON(func.ST_Transform(Nha.geom,4326)).label('geometry')).all()
    nhaFeature=[]
    for nha in nhas:
        properties_temp = {
            "diaChi": nha.diaChi,
            "loaiNha": nha.loaiNha,
            "soTang": nha.soTang,
            "dienTich": nha.dienTich,
            "id": nha.id
        }
        geometry_temp = json.loads(nha.geometry)
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

# API get data from nha table
@app.route("/api/v1/postGIS_BT")
def postGIS_api_BT():
    """Return feature in nha table"""

    nhas = db.session.query(BaiTap.id, BaiTap.diachi, BaiTap.loainha, BaiTap.sotang, BaiTap.dientich,\
    func.ST_AsGeoJSON(BaiTap.geom).label('geometry')).all()
    nhaFeature=[]
    for nha in nhas:
        properties_temp = {
            "diaChi": nha.diachi,
            "loaiNha": nha.loainha,
            "soTang": nha.sotang,
            "dienTich": nha.dientich,
            "id": nha.id
        }
        geometry_temp = json.loads(nha.geometry)
        feature = {
            "type": "Feature",
            "properties": properties_temp,
            "geometry": geometry_temp
        }
        geometry_temp = json.loads(nha.geometry)
        nhaFeature.append(feature)

    # for nha in nhas:
    #     geometry_temp = json.loads(nha.geometry)
    #     return nha.geometry
    return jsonify({
                #"type":"FeatureCollection",
                "features": nhaFeature
        })

# #----------GET API for leaflet from postGIS search by loai nha ----------------
@app.route("/api/v1/postGIS/<string:loaiNha>")
def postGIS_api_filter(loaiNha):
    """Return feature in point table"""

    nhas = db.session.query(Nha.id, Nha.diaChi, Nha.loaiNha, Nha.soTang, Nha.dienTich, \
    func.ST_AsGeoJSON(func.ST_Transform(Nha.geom,4326)).label('geometry')).filter(Nha.loaiNha==loaiNha).all()
    nhaFeature=[]
    for nha in nhas:
        properties_temp = {
            "diaChi": nha.diaChi,
            "loaiNha": nha.loaiNha,
            "soTang": nha.soTang,
            "dienTich": nha.dienTich,
            "id": nha.id
        }
        geometry_temp = json.loads(nha.geometry)
        p = {
            "type": "Feature",
            "properties": properties_temp,
            "geometry": geometry_temp
        }
        nhaFeature.append(p)

    return jsonify({
                "features": nhaFeature
        })

# #----------GET API for leaflet from postGIS search by loai nha ----------------
@app.route("/api/v1/postGIS/filterById/<string:id>")
def postGIS_api_filter_by_id(id):
    """Return feature in point table"""

    nha = db.session.query(Nha.id, Nha.diaChi, Nha.loaiNha, Nha.soTang, Nha.dienTich,\
    func.ST_AsGeoJSON(func.ST_Transform(Nha.geom,4326)).label('geometry'),\
    func.ST_AsGeoJSON(func.ST_Centroid(func.ST_Transform(Nha.geom,4326))).label('zoomCoords')).filter(Nha.id==id).first()
    properties_temp = {
        "diaChi": nha.diaChi,
        "loaiNha": nha.loaiNha,
        "soTang": nha.soTang,
        "dienTich": nha.dienTich,
        "id": nha.id
    }
    geometry_temp = json.loads(nha.geometry)
    nhaObject= {
        "type": "Feature",
        "properties": properties_temp,
        "geometry": geometry_temp,
    }
    nhaFeature=[]
    nhaFeature.append(nhaObject)
    zoomCoords_temp = json.loads(nha.zoomCoords)
    return jsonify({
                "features": nhaFeature
        })

# #----------open leaflet file in Flask ----------------
@app.route("/leaflet_Geojson")
def leaflet_geojson():
    """Return leaflet map"""
    url = "http://localhost:5000/api/v1/postGIS"
    res = requests.get(url)
    data = res.json()
    datajson = json.dumps(data)
    #data ="123"
    #datageojson = json.loads(datajson)
    return render_template('16 GeoJson_from_postGIS_search_and_zoom_plugin.html', data=datajson)

# API get data from nha table
@app.route("/CORS")
def CORS():
    return render_template('14 GeoJson_from_postGIS_JQuery_asyncTrue.html')

# API get data from nha table
@app.route("/insert_point")
def insert_point():
    lat = 105.789
    lng = 21.545
    loaicay = "pine"
    chieucao = 2.8

    newTree = Tree(geom=func.ST_GeomFromText(f'MULTIPOINT(({lat} {lng}))', 4326), loaicay=loaicay, chieucao=chieucao)
    db.session.add(newTree)
    db.session.commit()
    return render_template('14 GeoJson_from_postGIS_JQuery_asyncTrue.html')
