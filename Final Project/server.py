#!/usr/bin/env python3
import socket
import sys
import time
import requests
import zipcode
import json


def get_OWM(zipcode):
    cloud_list = []
    user_token = '9738f6dd8889617a46ed1ab4109dffb6'
    full_api_url = 'http://api.openweathermap.org/data/2.5/weather?zip=' + zipcode + ',us&cnt=16&units=imperial&APPID=' + user_token
    if len(zipcode) != 5:
        print('Error: Invalid zipcode in get_OWM(zipcode) call!')
        sys.exit()
    try:
        r = requests.get(full_api_url)
    except:
        print('Error: Weather API request error!')
        sys.exit()
    try:
        weather_data = json.loads(r.text)
        weather_list = weather_data['list']
        for i in range(0,16):
            cloud_list.append(weather_list[i]['clouds'])
        return cloud_list
    except:
        print('Error: Invalid response from weather API')
        sys.exit()
def get_Trail(activity, city, state, radius):
	full_api_url = 'https://trailapi-trailapi.p.mashape.com/?lon=-&q[activities_activity_type_name_eq]=' + activity + '&q[city_cont]=' + city+ '&q[country_cont]=United+State&q[state_cont]=' + state +'&radius=' +radius;
	response = requests.get(full_api_url, headers={ "X-Mashape-Key": "kopJS5O41PmshhVPxUeXCkLj8rOQp14geTqjsnSiGdq8SoUTWR", "Accept": "tapplication/json"})
	return json.loads(response.text);

def main():       
	host = ''
	port = 50003
	backlog = 5
	size = 1024
	s = None
	#example of using trail API with activity, city, state, and radius
	# there are only 2 types of activites:  
	#to-do: parse zipcode to city and state
	trail_data = get_Trail('hiking', 'Blacksburg', 'virginia', '25')
	print (trail_data)
	try:
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object that use IPv4 and TCP
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    s.bind((host, port))
	    s.listen(backlog)
	except socket.error as message:  # error handling
	    if s:
	        s.close()
	    print("Could not open socket: " + str(message))
	    sys.exit(1)
	print('Server Connected')
	while 1:
	    wclient, address = s.accept()  # accept request from a client
	    pickled_data = wclient.recv(size)  # received a  data



	    wclient.close()

if __name__ == "__main__":
    main()