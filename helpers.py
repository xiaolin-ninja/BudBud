from bs4 import BeautifulSoup
import urllib2
from server import *
import requests

#-----------------------------------------------------------------------------#

def get_dispensaries(route):
    """scrape leafly page for a specific strain given url,
    return dispensaries in SF that offer the strain

    >>> get_dispensaries('indica/bubba-kush')
    set([u'Trestl', u'Community Gardens', u'Blum - Oakland', u'{{model.locationName}}', u'Elevated San Francisco', u'Cannabis Express', u'Verde Local', u'Top Shelf Express Delivery', u'BayQueen Delivery'])

    """
    url = 'https://www.leafly.com/{}/availability/san-francisco-ca'.format(route)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # import pdb; pdb.set_trace()
    # html = list(soup.children)[2]
    # body = list(html.children)[3]
    return set(d.get('title') for d in soup.find_all('a')
                     if ( d.get('title') is not None) )


def get_locations(url):
    """helper function that scrapes for all dispensaries that offer this strain
    (from Leafly), checks if it's in the DB, returns a dictionary"""
    dispensaries = get_dispensaries(url)

    disp_json = {}
    # if dispensary is in the database
    for dispensary in dispensaries:
        d = Dispensary.query.filter_by(name=dispensary).first()
        if d:
            print d.name, 'found in db'
            disp_json[d.dispensary_id] = {
                "name": d.name,
                "lat": d.disp_lat,
                "lng": d.disp_lng,
                "address": d.address,
            }

    print 'succesfully created json file of dispensaries'
    return disp_json


def get_strain_info(route):
    """Get description of strains from Leafly"""
    url = 'https://www.leafly.com/{}'.format(route)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.findAll("div", {"class": "description"})[0].text


def check_strain(user_input):
    """Check if strain is in database,
    takes in either strain name or ID"""
    print "I am checking if {} is in the database.".format(user_input)
    strain = Strain.query.filter(func.lower(Strain.s_name)==func.lower
        (user_input)).first()
    # if can't check by name, check by ID.
    if not strain:
        try:
            strain = Strain.query.get(user_input)
        except:
            # if strain not found, return empty string
            return ""
    return "success"

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    import doctest

    print
    result = doctest.testmod()
    if not result.failed:
        print "ALL TESTS PASSED. GOOD WORK!"
    print