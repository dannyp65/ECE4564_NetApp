#!/usr/bin/env python3
import socket
import sys
import time
import requests
import zipcode
import json

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


def get_Trail(activity, city, state, radius):
    full_api_url = 'https://trailapi-trailapi.p.mashape.com/?lon=-&q[activities_activity_type_name_eq]=' + activity + '&q[city_cont]=' + city + '&q[country_cont]=United+State&q[state_cont]=' + state + '&radius=' + radius
    # api_url = 'https://trailapi-trailapi.p.mashape.com/?lat=' + lat + '&lon=' + long + '&q[activities_activity_type_name_eq]=' + activity +' &radius=' + radius
    response = requests.get(full_api_url,
                            headers={"X-Mashape-Key": "kopJS5O41PmshhVPxUeXCkLj8rOQp14geTqjsnSiGdq8SoUTWR",
                                     "Accept": "tapplication/json"})
    return json.loads(response.text)


def main():
    host = ''
    port = 50003
    backlog = 5
    size = 1024
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
    print('Server Connected')
    while 1:
        wclient, address = s.accept()  # accept request from a client
        pickled_data = wclient.recv(size)  # received data

        # example of using trail API with activity, city, state, and radius
        # there are only 2 types of activites:
        # to-do: parse zipcode to city and state
        places = []
        trail_data = get_Trail(activity, city, state, radius)
        # stores location's name, picture, rating, length, activity type, and directions from JSON dictionary in list
        for loc in trail_data["places"]:
            places.append([loc["name"], loc["activities"][0]["thumbnail"], loc["activities"][0]["rating"],
                           loc["activities"][0]["length"], loc["activities"][0]["activity_type_name"],
                           loc["directions"]])
        # if nothing is found add a message to the list
        if len(places) == 0:
            places.append("No " + activity + " locations found.")
            ###TESTING: print each location's details
        c = 1
        print("Found %d places:" % (len(places)))
        for x in places:
            print("%d." % (c), x, "\n")
            c += 1
            ###---
        weather = get_OWM(city, state)
        weather_stats = [weather["main"]["temp"], weather["main"]["temp_min"], weather["main"]["temp_max"],
                         weather["wind"]["speed"], weather["clouds"]["all"]]
        print(
            "-----\nTemp(Min, Current, Max): {0}{5}F, {1}{5}F, {2}{5}F \nWind Speed: {3} \nClouds: {4}\n-----\n".format(
                weather_stats[1], weather_stats[0], weather_stats[2], weather_stats[3], weather_stats[4], chr(176)))


        wclient.close()


if __name__ == "__main__":
    main()
