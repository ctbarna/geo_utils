import json
import urllib
import urllib2

class GeoLookup:
    """

    GeoCode a list of geometries with the bing API and make GeoJSON.

    """

    API_URL = "http://dev.virtualearth.net/REST/v1/Locations"

    def __init__(self, key, srcfile):
        """
        Open the sourcefile and load the resources into a variable.
        """
        self.API_KEY = key
        f = open(srcfile)
        self.ogdata = json.loads(f.read())
        self.geodata = []

    def pullGeoCodes(self):
        """
        Pull the geocodes for each point.
        """
        for entity in self.ogdata:
            params = entity
            params['key'] = self.API_KEY

            query_params = urllib.urlencode(params)
            data = urllib2.urlopen("%s?%s" % (self.API_URL,
                query_params)).read()

            temp_json = json.loads(data)
            lat = temp_json['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
            lon = temp_json['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
            temp_dict = {
                    'locality': params['locality'],
                    'adminDistrict': params['adminDistrict'],
                    'lat': lat,
                    'lon': lon
                    }

            self.geodata.append(temp_dict)

    def getGeoJSON(self):
        geojson = {"type": "FeatureCollection",
                "features": []}

        for geo in self.geodata:
            temp = {"type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [geo['lat'], geo['lon']]
                        },
                    "properties": {
                        "locality": geo['locality'],
                        "adminDistrict": geo['adminDistrict']
                        }}
            geojson['features'].append(temp)

        return json.dumps(geojson)
