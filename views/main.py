from flask import Flask, Blueprint, json, request
from queries.oscar import oscar_categories, user_selections, oscar_winners
from app import admin
import orm
from flask_admin.contrib.sqla import ModelView
import pandas as pd

bp = Blueprint('main', __name__, url_prefix='')

@bp.route('/')
def is_up():
    return 'ACTIVE'

@bp.route('/api/getCurrentOscarOptions', methods=['GET'])
def get_current_oscar_options():
    df = pd.DataFrame(oscar_categories(), columns=['Year', 'Cat', 'Name'])
    return df.to_json(orient="records")

@bp.route('/api/getCurrentUserSelections', methods=['GET'])
def get_current_user_selections ():
    if 'user' in request.args.keys():
        df = pd.DataFrame(user_selections(request.args['user']), columns=['Year', 'User', 'Cat', 'Favorite', 'Won'])
        return df.to_json(orient="records")
    else:
        return pd.DataFrame().to_json(orient="records")

@bp.route('/api/setCurrentUserSelections', methods=['POST'])
def set_current_user_selections ():
    d = request.data.decode('UTF-8')
    d = json.loads(d)
    print(d)
    return 'pass'
