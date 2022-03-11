import orm
import datetime

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

