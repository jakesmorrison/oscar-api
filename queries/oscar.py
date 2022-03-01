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
    query = "SELECT Year,Cat,Name,Weight WHERE Year={} FROM oscar_winners".format(year)
    return orm.query(query)


