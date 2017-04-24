#!/usr/bin/env python3
import socket
import sys
import time
import requests
import zipcode
import json

# Function for command line arguments
def get_args():
    opt_in_opt = "ERROR: cannot take another opt flag as a parameter"
    cmd_args = sys.argv
    cmd_len = len(cmd_args)
    a_check, c_check, s_check, r_check = False, False, False, False
    a_opt, c_opt, s_opt, r_opt = '', '', '', ''
    for i in range(1, cmd_len):
        if cmd_args[i] == a_opt or cmd_args[i] == c_opt or cmd_args[i] == s_opt or cmd_args[i] == r_opt:
            continue
        if cmd_args[i] == '-a':
            try:
                a_opt = cmd_args[i + 1]  # raise out of range
                if a_opt == '-a' or a_opt == '-c' or a_opt == '-s' or a_opt == '-r':
                    print(opt_in_opt, '1')
                    sys.exit()  # raise SystemExit
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no Activity given")
                raise SystemExit
            a_check = True
        elif cmd_args[i] == '-s':
            try:
                s_opt = cmd_args[i + 1]
                if s_opt == '-a' or s_opt == '-c' or s_opt == '-s' or s_opt == '-r':
                    print(opt_in_opt, '2')
                    sys.exit()
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no State given")
                raise SystemExit
            s_check = True
        elif cmd_args[i] == '-c':
            try:
                c_opt = cmd_args[i + 1]
                if c_opt == '-a' or c_opt == '-c' or c_opt == '-s' or c_opt == '-r':
                    print(opt_in_opt, '3')
                    sys.exit()
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no City given")
                raise SystemExit
            c_check = True
        elif cmd_args[i] == '-r':
            try:
                r_opt = cmd_args[i + 1]
                if r_opt == '-a' or r_opt == '-c' or r_opt == '-s' or r_opt == '-r':
                    print(opt_in_opt, '4')
                    sys.exit()
            except SystemExit:
                raise SystemExit
            except:
                print("ERROR: no Radius given")
                raise SystemExit
            r_check = True
        elif cmd_args[i].startswith('-'):
            print("ERROR: incorrect opt flag")
            sys.exit()
        else:
            print("ERROR: ELSE", cmd_args[i])
            sys.exit()
    if a_check and c_check and s_check and r_check:
        return a_opt, c_opt, s_opt, r_opt
    else:
        print("ERROR: all parameters need to be set")
        sys.exit()

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
	
	activity, city, state, radius = get_args()
	print(activity, city, state, radius)
	#example of using trail API with activity, city, state, and radius
	# there are only 2 types of activites:  
	#to-do: parse zipcode to city and state
	trail_data = get_Trail(activity, city, state, radius)
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
