# 2018-09-03 23:30:12
# author: Caton ZHONG Zixuan
# updated at: 2018-09-03

import cv2
import numpy as np
import json
import time
import os
import commands
import re
import send_email
import requests
import socket
import urllib2



def internet_on():
    try:
        urllib2.urlopen('https://www.google.com.hk', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False  


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com.hk', 0))
    return s.getsockname()[0]

def device_init(ip_):
    url = 'https://ust.one/api/initiate-device'
    payload = {'ip': ip_,"Content-Type": "application/json"}
    headers = {'Content-Type': 'application/jsons'}
    response = requests.post(url, data=json.dumps(payload),headers=headers)
    if (response.status_code != 200):
        print("response wrong")
        
if(internet_on()): 
    # get ip
    ip = get_ip()
    conf = '/home/ustone/conf.json'
    with open(conf, 'r') as json_file:
        json_data=json_file.read().replace('\n', '')
    conf_json = json.loads(json_data)
    machine_id = conf_json['id']
    if(machine_id==0):
        device_init(ip)
        

    




