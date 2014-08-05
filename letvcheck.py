#!/usr/bin/env python3
#coding:utf-8
# Author: Beining --<ACICFG>
# Purpose: Batch check whether the Letvcloud file's statues.
# Created: 08/02/2014

import urllib.request
import sys
import os
import json
import hashlib
import getopt


#----------------------------------------------------------------------
def check_upload(source_id):
    """"""
    line_to_write_this =''
    message = ''
    user_id = ''
    video_name = ''
    video_duration = ''
    add_time = ''
    type_avalable = ''
    user_unique = ''
    video_type_set = ''
    str2Hash = 'cfflashformatjsonran0.7214574650861323uu2d8c027396ver2.1vu' + source_id + 'bie^#@(%27eib58'
    sign = hashlib.md5(str2Hash.encode('utf-8')).hexdigest()
    request_info = urllib.request.Request('http://api.letvcloud.com/gpc.php?&sign='+sign+'&cf=flash&vu='+source_id+'&ver=2.1&ran=0.7214574650861323&qr=2&format=json&uu=2d8c027396')
    try:
        response = urllib.request.urlopen(request_info)
        data = response.read()
        info = json.loads(data.decode('utf-8'))
        #print(info['code'])
        if info['code'] == 0:
            message = info['message']
            user_id = info['data']['video_info']['user_id']
            video_name = info['data']['video_info']['video_name']
            video_duration = info['data']['video_info']['video_duration']
            add_time = info['data']['video_info']['add_time']
            user_unique = info['data']['user_info']['user_unique']
            video_type_set = info['data']['user_info']['video_type_set']
            for i in info['data']['video_info']['media']:
                type_avalable = type_avalable + info['data']['video_info']['media'][i]['video_type'] + ';'
        else:
            print(source_id + ','+info['message'])
            return str(source_id + ','+info['message'])
    except:
        print(source_id + ',ERROR: Cannot check!')
        return str(source_id + ',ERROR: Cannot check!')
    line_to_write_this = source_id + ',' + message + ',' + video_name + ',' + video_duration + ',' + add_time + ',' + user_id + ',' + type_avalable
    print(line_to_write_this)
    return line_to_write_this

#----------------------------------------------------------------------
def usage():
    """"""
    print('''Usage:
    python3 letvcheck.py (-h)(-s 1.csv) vu1 vu2
    -s: Save to CSV file.
    -h: Help.''')


if __name__=='__main__':
    argv_list = []
    argv_list = sys.argv[1:]
    file_csv = ''
    line_to_write = ''
    try:
        opts, args = getopt.getopt(argv_list, "hs:", ["help",'save'])
    except getopt.GetoptError:
        usage()
        exit()
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            exit()
        elif o in ('-s', '--save'):
            file_csv = a
            print('Saving your result to csv file '+a)
            try:
                argv_list.remove('-s')
            except:
                break
            argv_list.remove(a)
    #print(argv_list)
    if file_csv is not '':
        for vu in argv_list:
            line_to_write = line_to_write + str(check_upload(vu)) + '\n'
            line_to_write = line_to_write
            f = open(file_csv, "w")
            f.writelines(line_to_write)
            f.close()
    else:
        for vu in argv_list:
            check_upload(vu)