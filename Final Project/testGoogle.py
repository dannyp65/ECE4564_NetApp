#!/usr/bin/env python3
import socket
import sys
import time
import requests
import zipcode
import json

def get_Google(current, destination):
    full_api_url = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + current + '&destination=' + destination + '&key=AIzaSyDe7n7-K-vkA8lbHRWgUpy36X5PJRxBQvQ'
    response = requests.get(full_api_url)
    return json.loads(response.text)

def main():
    current = "517 Green St, Blacksburg, VA, 24060"
    destination = "304 Broce Dr, Blacksburg, VA, 24060"
    final_result = get_Google(current, destination)
    print (final_result)

if __name__ == "__main__":
    main()
   
