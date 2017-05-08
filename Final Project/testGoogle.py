#!/usr/bin/env python3
import socket
import sys
import time
import requests
import zipcode
import json

def get_Google(activity, zipcode, radius):
    full_api_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='+activity+zipcode+'&radius='+radius+'&key=AIzaSyCXSbe5xRL_aa-Op0AVNwJ-RsZgcCmvPSY'
    response = requests.get(full_api_url)
    return json.loads(response.text)

def main():
    activity = "hiking"
    zipcode = "24060"
    radius = "5"
    final_result = get_Google(activity, zipcode, radius)
    print (final_result)

if __name__ == "__main__":
    main()
    
