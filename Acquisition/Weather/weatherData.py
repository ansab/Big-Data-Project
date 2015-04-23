import urllib2
import json
f = urllib2.urlopen('http://api.wunderground.com/api/cc7750cde6c9a984/geolookup/conditions/q/CA/El_monte.json')
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_f']
rain = parsed_json['current_observation']['pressure_in']
print "Current temperature in %s is: %s" % (location, temp_f)
print "Rainfall Measured is: %s" % (rain)

f.close()