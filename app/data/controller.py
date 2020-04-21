from app import cache
from app.data import data_bp
from app.extensions import cache, mongo
from flask import jsonify, request, make_response, abort, Response
from flask_caching import Cache
import json

CACHE_TIMEOUT = 600*1 # 10 min

entries_collection = mongo.db.entries
    
@data_bp.route('/api/v1/states')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='states')
def states():
    e = entries_collection.find({}, {'state':1}).distinct('state')
    e = tuple(e)
    return jsonify({
        'result': e
    })

@data_bp.route('/api/v1/state/<string:state>')
@cache.memoize(timeout=CACHE_TIMEOUT)
def state_view(state):
    e = entries_collection.find({'state': state}, {'_id':0})
    e = tuple(e)
    return jsonify({
        'result': e
    })

@data_bp.route('/api/v1/state/<string:state>/<string:category>')
@cache.memoize(timeout=CACHE_TIMEOUT)
def state_w_category(state, category):
    e = entries_collection.find({'state':state, 'category':category}, {'_id':0})
    e = tuple(e)
    return jsonify({
        'result': e
    })


