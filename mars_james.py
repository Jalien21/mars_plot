import csv
import json
from xml.dom import minidom
import urllib2
import xmltodict
import simplejson
try:
    from simplejson import JSONEncoderForHTML
except:
    from simplejson.encoder import JSONEncoderForHTML
import matplotlib.pyplot as plt
from numpy.random import rand

def toGeoJSON(record):
    gj = {}
    gj['type'] = 'Feature'
    gj['geometry'] = {}
    gj['properties'] = {}
    gj['properties'] = json.loads(json.dumps(xmltodict.parse(record.toxml()).get('location')))
    solNumber = int(gj['properties']['startSol'])
    try:
        gj['properties']['image'] = siteList[solNumber]['urlList']
        gj['properties']['itemName'] = siteList[solNumber]['itemName'] + '&s=' + str(int(siteList[solNumber]['sol']))
    except:
        gj['properties']['image'] = ""
        gj['properties']['itemName'] = ""
    #print gj['properties']['image']
    #print gj['properties']['itemName']
    gj['geometry']['type'] = 'Point'
    gj['geometry']['coordinates'] = [float(gj['properties']['lon']),float( gj['properties']['lat'])]
    return gj
    
f = open('test.csv', 'wb')

locs = 'http://mars.jpl.nasa.gov/msl-raw-images/locations.xml'
print "reading: ", locs	
data = urllib2.urlopen(locs).read()
print "parsing xml..."
xmldoc = minidom.parseString(data)
print "parsing location..."
covs = xmldoc.getElementsByTagName('location')

print "building plt and geoJson..."
for cov in covs:
    geoJson = toGeoJSON(cov)
    #print geoJson['geometry']['coordinates']
    sol = geoJson['properties']['startSol']
    x = geoJson['geometry']['coordinates'][0]
    y = geoJson['geometry']['coordinates'][1]
    f.write(str(sol)+','+str(x)+','+str(y)+'\n')   
    plt.scatter(x, y, alpha=0.3, edgecolors='none')

	
f.close()

print "plotting..."
#plt.legend()
plt.grid(True)
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.show()