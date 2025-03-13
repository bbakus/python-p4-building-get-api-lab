#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return all_bakeries

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    
    bakery = Bakery.query.get(id)

    bakery_dict = bakery.to_dict()
    bakery_dict["baked_goods"] = [baked_good.to_dict() for baked_good in bakery.baked_goods]
    
    return bakery_dict

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    
    baked_price = [baked_good.to_dict() for baked_good in baked_goods_by_price]
    
    return baked_price

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    highest_price = BakedGood.query.order_by(BakedGood.price.desc()).first()

    return jsonify(highest_price.to_dict())





if __name__ == '__main__':
    app.run(port=5555, debug=True)
