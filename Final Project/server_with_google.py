#!/usr/bin/env python3
import socket
import threading
import sys
import time
import requests
import zipcode
import json
import pickle
import hashlib


# this function generates a MD5 checksum value from string
def MD5_Encode(str):
    endata = str.encode('utf-8')
    m = hashlib.md5()
    m.update(endata)
    return m.hexdigest()


# this function receive a string and a checksum value
# it generate a new checksum value for the input string
# then checking it with the checksum to see if the transferred string is correct
def Check_Payload(str, checksum):
    compute_checksum = MD5_Encode(str)
    if checksum == compute_checksum:
        return True
    else:
        return False


def get_OWM(city, state):
    cloud_list = []
    user_token = '9738f6dd8889617a46ed1ab4109dffb6'
    full_api_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + state + '&units=imperial&APPID=' + user_token
    try:
        r = requests.get(full_api_url)
    except:
        print('Error: Weather API request error!')
        sys.exit()
    weather_data = json.loads(r.text)
    return weather_data


def get_Google(activity, city, state, radius):
    full_api_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='+ activity + '+' + city + '+' + state + '&types=campground|park|natural_feature&radius=' + radius + '&key=AIzaSyCXSbe5xRL_aa-Op0AVNwJ-RsZgcCmvPSY'
    response = requests.get(full_api_url)
    return json.loads(response.text)


def main():
    host = ''
    port = 1234
    backlog = 5
    size = 4096
    s = None

    # socket connection and information transition
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
    print('Server Socket Bound and Listening')
    while 1:
        print('\nWaiting to accept new connection...')
        wclient, address = s.accept()  # accept request from a client
        pickled_data = wclient.recv(size)  # received data
        recv_data = pickle.loads(pickled_data)

        params = recv_data[0]
        recv_checksum = recv_data[1]
        print('Payload Received\nChecking MD5 Checksum')

        if Check_Payload(params, recv_checksum):  # checking if the the checksum to see if the information is correct
            print('Checksum Verified')
            activity = params.split(',')[0]
            city = params.split(',')[1]
            state = params.split(',')[2]
            radius = params.split(',')[3]
            print("Parameters Received From Client:", activity, city, state, radius)
            # example of using trail API with activity, city, state, and radius
            # there are only 2 types of activites:
            places = []
            trail_data = get_Google(activity, city, state, radius)
            # stores location's information from JSON dictionary in list
            for loc in trail_data["results"]:
                if (loc.get("rating")):
                    places.append([loc["name"],loc["formatted_address"],loc["rating"]])
                else:
                    places.append([loc["name"],loc["formatted_address"]])
            # if nothing is found add a message to the list
            if len(places) == 0:
                places.append("No " + activity + " locations found.")

            weather = get_OWM(city, state)
            weather_stats = [weather["main"]["temp"], weather["main"]["temp_min"], weather["main"]["temp_max"],
                             weather["wind"]["speed"], weather["clouds"]["all"]]

            str_places = '[!]'.join(str(x) for x in places)
            str_weather = '[!]'.join(str(y) for y in weather_stats)
            str_send = str_places + '[?]' + str_weather
            #print(str_send)
            send_checksum = MD5_Encode(str_send)
            tuple_send = (str_send, send_checksum)
            pickle_send = pickle.dumps(tuple_send)
            print('Sending Requested Data Back to Client')
            wclient.send(pickle_send)
        else:  # if checksum not correct, send an error message to the client
            print('MD5 Checksum Not Verified')
            wclient.send(b'MD5 Verification Fail!')
        # close the connection with client
        wclient.close()


if __name__ == "__main__":
    main()
