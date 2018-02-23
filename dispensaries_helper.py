from bs4 import BeautifulSoup
import urllib2
from server import *
import requests

#---------------------------------------------------------------------------------#

def get_dispensaries(strain):
    """scrape leafly page for a specific strain given url,
    return dispensaries in SF that offer the strain

    >>> get_dispensaries('indica/bubba-kush')
    set([u'Trestl', u'Community Gardens', u'Blum - Oakland', u'{{model.locationName}}', u'Elevated San Francisco', u'Cannabis Express', u'Verde Local', u'Top Shelf Express Delivery', u'BayQueen Delivery'])

    """
    url = 'https://www.leafly.com/{}/availability/san-francisco-ca'.format(strain)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # import pdb; pdb.set_trace()
    # html = list(soup.children)[2]
    # body = list(html.children)[3]
    return set(d.get('title') for d in soup.find_all('a')
                     if ( d.get('title') is not None) )


def get_locations(url):
    """helper function that scrapes for all dispensaries that offer this strain (from Leafly),
    checks if it's in the DB, returns a dictionary"""
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