"""Access data in json files, then feed into database"""
import json
import re
from server import app
import datetime
from model import (User, Strain, Dispensary, Journal_Log,
                   User_Search, Anon_Search, db, update_search_db, connect_to_db)

def load_strains_data(json_file):
    """reads json file of strains & extracts relevant info"""
    with open(json_file) as f:
        strains = json.loads(f.read())['Strains']
        return strains
#keys: u'Category', u'Rating', u'ReviewCount', u'Name', u'NegativeEffects',
# u'Tags', u'Symbol', u'DisplayCategory', u'LogTags', u'Symptoms', u'CannabinoidProfile',
# u'Flavors', u'RatingCount', u'UrlName', u'KioskCuratedListScores', u'Conditions',
# u'Id', u'SortName'


def load_strains(json_file):
    """loads strains into database, calls load_strains_data()"""
    for s in load_strains_data(json_file):
        pos_effects = [ effect["DisplayLabel"] for effect in s["Tags"] ]
        neg_effects = [ effect["DisplayLabel"] for effect in s["NegativeEffects"]]
        s_type=s['Category']
        url = '{}/{}'.format(s_type.lower(), s['UrlName'])

        strain = Strain(s_name=s['Name'],
                        s_type=s_type,
                        pos_effects=pos_effects,
                        neg_effects=neg_effects,
                        leafly_url=url)
        add_to_db(strain)


# def remove_chars(string):
#     """remove non alphanueric characters from string"""
#     return re.sub("[^a-zA-Z]","", string)

def load_dispensaries():
    """reads json file & loads dispensaries into database"""
    with open('seed_data/dispensaries.json') as f:
        dispensaries = json.loads(f.read())['results']
    # dispensaries['results'][idx].keys() = [u'rating', u'name', u'reference', u'geometry',
    # u'opening_hours', u'place_id', u'photos', u'formatted_address', u'id', u'types', u'icon']
        for d in dispensaries:
            dispensary = Dispensary(name=d['name'],
                                disp_lat=d['geometry']['location']['lat'],
                                disp_lng=d['geometry']['location']['lng'],
                                address=d['formatted_address'])
            add_to_db(dispensary)

def load_test_user():
    db.session.add(User(preferred_type='Sativa',
                        age=21,
                        zipcode=94118,
                        user_type='Medical',
                        lname='lastname',
                        fname='firstname',
                        password='password',
                        email='email'))
    db.session.commit()

def add_to_db(var):
    """helper function to avoid duplicates & uniqueness errors"""
    try:
        db.session.add(var)
        db.session.commit()
        print var, 'added'
    except Exception:
        db.session.rollback()
        print var, 'duplicate'

##########################################################################################

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    load_strains('seed_data/hybrids.json')
    load_strains('seed_data/indicas.json')
    load_strains('seed_data/sativas.json')
    load_dispensaries()
    load_test_user()
