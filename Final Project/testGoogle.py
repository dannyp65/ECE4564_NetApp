#!/usr/bin/env python3
import socket
import sys
import time
import requests
import zipcode
import json

def get_Google():
    full_api_url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=CnRtAAAATLZNl354RwP_9UKbQ_5Psy40texXePv4oAlgP4qNEkdIrkyse7rPXYGd9D_Uj1rVsQdWT4oRz4QrYAJNpFX7rzqqMlZw2h2E2y5IKMUZ7ouD_SlcHxYq1yL4KbKUv3qtWgTK0A6QbGh87GB3sscrHRIQiG2RrmU_jF4tENr9wGS_YxoUSSDrYjWmrNfeEHSGSc3FyhNLlBU&key=AIzaSyCXSbe5xRL_aa-Op0AVNwJ-RsZgcCmvPSY'
    response = requests.get(full_api_url)
    return response

def main():
    final_result = get_Google()
    print (final_result)

if __name__ == "__main__":
    photoref = "CmRYAAAAcgHBFh51PP5mv4-BZy_l5FVVb4FNst1ZrNFnj3LtnglnlfVQT06foFBzRvqSBKoFFHj5NJ6g4c_mDocwVPyVGSVXMb5o8sY3jjuuSEKXjjqabAMoseai11XbZkJNinrSEhCT2zPrAVtZg-xHis8mSAEzGhRkzIRgFwfuMeQl4s3PxWmvifmSAQ"
    photorul = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=' + photoref + '&key=AIzaSyCXSbe5xRL_aa-Op0AVNwJ-RsZgcCmvPSY'
    print(photorul)
   
