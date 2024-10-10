
from flask import Flask, jsonify, request
import subprocess

from typing import Optional
from database.mongo_database import ItemsScrapedRepository
from configuration.settings import (get_mongo_uri, get_mongo_database)

app = Flask(__name__)

repository = ItemsScrapedRepository(get_mongo_uri(), get_mongo_database())

@app.route('/date', methods=['GET'])
def get_date():
    result = subprocess.check_output(['date']).decode('utf-8')
    return jsonify({'calendar': result.strip()})

@app.route('/docker', methods=['GET'])
def get_docker_ps():
    result = subprocess.check_output(['docker', 'ps']).decode('utf-8')
    return jsonify({'docker': result.strip()})

@app.route('/items', methods=['GET'])
def get_items_scrapped():
    min_price: Optional[float] = request.args.get("minprice", None)
    max_price: Optional[float] = request.args.get("maxprice", None)
    search_title = request.args.get("name", None)
    page = int(request.args.get("page", 1))
    platforms = request.args.getlist("plats")
    origin = request.args.get("origin", None)

    result = repository.get_all_by_params(search_title, min_price, max_price, platforms, origin, page)
    parsed_result = [r.to_dict() for r in result]

    return jsonify({'items':  parsed_result})

if __name__ == '__main__':
    app.run()
