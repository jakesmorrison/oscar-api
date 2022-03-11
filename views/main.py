from flask import Flask, Blueprint, json, request
from queries.oscar import setup_winners, oscar_leaders, oscar_categories, user_selections, oscar_winners, submit_choices
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
    r = submit_choices(d)
    return r

@bp.route('/api/getWinners', methods=['GET'])
def get_winners ():
    df = pd.DataFrame(oscar_winners(), columns=['Year', 'Cat', 'Name', 'Weight'])
    # If the dataFrame is empty we need to populate the winners with empty data. 
    if df.empty == True:
        df_cat = pd.DataFrame(oscar_categories(), columns=['Year', 'Cat', 'Name'])
        setup_winners(list(df_cat['Cat'].unique()))
        df = pd.DataFrame(oscar_winners(), columns=['Year', 'Cat', 'Name', 'Weight'])
        return df.to_json(orient="records")
    else:
        return df.to_json(orient="records")

@bp.route('/api/getLeaderboard', methods=['GET'])
def get_leaderboard ():
    return oscar_leaders().to_json(orient="records")
