from app import app
from app.models import *
from flask import json, render_template, request, redirect
from flask.json import jsonify
from sqlalchemy import func
from app.forms import editBuildingForm, editTreeForm
from flask.helpers import url_for
from flask_wtf import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://nhlong:123456@localhost:5432/postGIS")
da = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
    return render_template('index.html')

#edit tree
@app.route('/tree/<int:id>', methods=['POST', 'GET'])
def editTree(id):
    form = editTreeForm()
    tree = Tree.query.get(id)

    if form.validate_on_submit():
        tree.chieucao = request.form.get("chieucao")
        tree.loaicay = request.form.get("loaicay")
        db.session.commit()
        return redirect(url_for('index'))

    return render_template("editTree.html", tree=tree, form=form)

#edit building
@app.route('/building/<int:id>', methods=['POST', 'GET'])
def editBuilding(id):
    form = editBuildingForm()
    building = Building.query.get(id)

    if form.validate_on_submit():
        building.name = form.name.data
        building.typehouse = form.typehouse.data
        building.floor = form.floor.data
        building.square = form.square.data
        building.addr_house = form.addr_house.data
        db.session.commit()
        return redirect(url_for('index'))

    return render_template("editBuilding.html", building=building, form=form)

#delete tree
@app.route("/delTree/<int:id>", methods=["POST", "GET"])
def delTree(id):
    tree = Tree.query.get(id)
    db.session.delete(tree)
    db.session.commit()
    return redirect(url_for('index'))

#delete building
@app.route("/delBuilding/<int:id>", methods=["POST", "GET"])
def delBuilding(id):
    building = Building.query.get(id)
    db.session.delete(building)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/v1/building')
def building_api():
    buildings = db.session.query(Building.id,
                                 Building.addr_house, Building.typeHouse,
                                 Building.floor, Building.square,
                                 func.ST_AsGeoJSON(func.ST_Transform(Building.geom, 4326)).label('geometry')).all()
    buidling_feature = []
    for building in buildings:
        properties_temp = {
            "diaChi": building.addr_house,
            "loaiNha": building.typeHouse,
            "soTang": building.floor,
            "dienTich": building.square,
            "id": building.id,
        }
        geometry_temp = json.loads(building.geometry)
        feature = {
            "type": "Feature",
            "properties": properties_temp,
            "geometry": geometry_temp
        }
        buidling_feature.append(feature)

    return jsonify({
        "features": buidling_feature
    })


@app.route('/api/v1/tree')
def tree_api():
    trees = db.session.query(Tree.id,
                             Tree.loaicay, Tree.chieucao,
                             func.ST_AsGeoJSON(func.ST_Transform(Tree.geom, 4326)).label('geometry')).all()
    tree_feature = []
    for tree in trees:
        properties_temp = {
            "loaicay": tree.loaicay,
            "chieucao": tree.chieucao,
            "id": tree.id,
        }
        geometry_temp = json.loads(tree.geometry)
        feature = {
            "type": "Feature",
            "properties": properties_temp,
            "geometry": geometry_temp
        }
        tree_feature.append(feature)

    return jsonify({
        "features": tree_feature
    })


@app.route('/createNewItem', methods=['POST'])
def createNewItem():
    print(request.get_json())
    data = request.get_json()
    data["features"][0]["geometry"]["crs"] = {
        "type": "name", "properties": {"name": "EPSG:4326"}}

    print(data["features"][0]["geometry"])

    result = json.dumps(data["features"][0]["geometry"])

    if data["features"][0]["geometry"]["type"] == "Point":
        tree = Tree(geom=func.ST_GeomFromGeoJSON(result))
        db.session.add(tree)
    else:
        building = Building(geom=func.ST_GeomFromGeoJSON(result))
        db.session.add(building)

    db.session.commit()
    return redirect(url_for('index'))
