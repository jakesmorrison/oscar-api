import orm
import datetime
import pandas as pd
import numpy as np

@orm.Session()
def oscar_categories ():
    year = datetime.datetime.now().year
    query = "SELECT Year,Cat,Name FROM oscar_oscarcategories WHERE Year={}".format(year)
    return orm.query(query)

@orm.Session()
def user_selections (user):
    year = datetime.datetime.now().year
    query = "SELECT Year,User,Cat,Favorite,Won FROM oscar_users WHERE Year={} AND User='{}'".format(year, user)
    return orm.query(query)

@orm.Session()
def oscar_winners ():
    year = datetime.datetime.now().year
    query = "SELECT Year,Cat,Name,Weight FROM oscar_winners WHERE Year={}".format(year)
    return orm.query(query)

@orm.Session()
def submit_choices (data):
    user = data['user']
    win = data['win']
    fav = data['fav']
    year = datetime.datetime.now().year
    return orm.postUser(user, year, win, fav)

@orm.Session()
def setup_winners (cat):
    year = datetime.datetime.now().year
    return orm.postWinners(year, cat)
    
@orm.Session()
def oscar_leaders():
    year = datetime.datetime.now().year
    query = "SELECT User,Cat,Favorite,Won FROM oscar_users WHERE Year={}".format(year)
    df_users = pd.DataFrame(orm.query(query), columns=['User', 'Cat', 'Favorite', 'Won'])

    query = "SELECT Cat,Name,Weight FROM oscar_winners WHERE Year={}".format(year)
    df_winners = pd.DataFrame(orm.query(query), columns=['Cat', 'Name', 'Weight'])

    df_merge = df_users.merge(df_winners, left_on='Cat', right_on='Cat', how='outer')
    del df_merge["Favorite"]
    df_merge = df_merge.reset_index()

    df_merge["Points"] = np.where((df_merge['Won'] == df_merge['Name']), 1*df_merge["Weight"], 0)
    # df_merge = df_merge[df_merge["Points"]>0]
    rankings = df_merge.groupby(["User"]).agg({'Points': ['count', 'sum']}).reset_index()
    rankings.columns = ['User', 'Correct Answers', 'Total Points']
    rankings.sort_values(['Total Points', 'Correct Answers'])
    return rankings

@orm.Session()
def oscar_favorites():
    year = datetime.datetime.now().year
    query = "SELECT User,Cat,Favorite,Won FROM oscar_users WHERE Year={}".format(year)
    df_users = pd.DataFrame(orm.query(query), columns=['User', 'Cat', 'Favorite', 'Won'])
    rankings = df_users.groupby(['Cat', 'Favorite'])['User'].count().reset_index()
    rankings = rankings.groupby('Cat').max().reset_index()
    rankings.columns = ['Category', 'Name', 'Votes']
    rankings.sort_values(['Votes'])
    return rankings

