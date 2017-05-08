#!/usr/bin/env python3
import socket
import sys
import time
import requests
import zipcode
import json

def get_Google(activity, zipcode, radius):
    full_api_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='+activity+zipcode+'&radius='+radius+'&key=AlzaSyCeje-BewlHbBDwXp5sL18nE81puhBNMHo'
    # api_url = 'https://trailapi-trailapi.p.mashape.com/?lat=' + lat + '&lon=' + long + '&q[activities_activity_type_name_eq]=' + activity +' &radius=' + radius
    response = requests.get(full_api_url)
    return json.loads(response.text)

def main():
    activity = "hiking"
    zipcode = "24060"
    radius = "50000"
    print(get_Goolge(activity, zipcode, radius))
    
