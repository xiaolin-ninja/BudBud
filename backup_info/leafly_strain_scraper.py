from bs4 import BeautifulSoup
import urllib2

# url = 'https://www.leafly.com/explore#/explore/location-san-francisco-ca(37.7957,-122.4209)'
# page = urllib2.urlopen(url)

# soup = BeautifulSoup(page, 'html.parser')

top_strains
for strain in soup.select('a[class="ga_Explore_Strain_Tile"]'):
    strain['href'].split('/')
#     # print strain['alt']
#  # doesn't work...

# # soup.img returns all code with image tag, can't access alt tag