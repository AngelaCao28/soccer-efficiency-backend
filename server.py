import json

from flask import Flask, request
from flask_cors import *

from impact_factor import *
from team_detail import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/indicatorInfo',methods=['POST'])
@cross_origin()
def handle_indicator_info():
    frontend_data = request.get_json()
    return get_impact_factors(frontend_data)

@app.route('/detailInfo',methods=['POST'])
@cross_origin()
def handle_detail_info():
    frontend_data_2 = request.get_json()
    return get_team_details(frontend_data_2)

if __name__ == '__main__':

    app.run(port=5050, debug=True)