#!/usr/bin/env python3

from Connection import Connection
import requests
from geoip import Geoip
from IP import IP
from datetime import datetime
import argparse
import pathlib
import os

THIS_PATH = pathlib.Path(__file__).parent.resolve()

OUTPUT_DIR = os.path.join(THIS_PATH, "out")
if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    
parser = argparse.ArgumentParser(prog="Tarpit Analyzer", description="Analyze tarpit logs and show who attacks your server!")
parser.add_argument("file", metavar="file", type=str, help="Tarpit Logfile")

args = parser.parse_args()
analytics_file = args.file
#analytics_file = "analytics-2022-11-08.log"



def get_value(sample:str) -> str:
    return sample.split("=")[1]

def crush_date(sample:str):
    date, time = sample.split('T')
    time, _ = time.split('.')
    return date, time

def get_open_connections(connections:dict) -> list:
    return [v for _,v in connections.items() if v.status == 'accepted']

def sort_dict_by_value(dictionary:dict, reverse:bool=False) -> dict:
    return {k: v for k,v in sorted(dictionary.items(), key=lambda v: v[1], reverse=reverse)}

def get_location(ip):
    response = requests.get(f"https://ipapi.co/{ip}/json").json()
    return response


def main():
    ip_count = {}
    country_count = {}
    connections = {}
    count_accept = 0
    count_closed = 0
    
    gi = Geoip()
    
    with open(analytics_file, 'r') as f:
        while line:=f.readline():
            if "host" in line:
                _, __, timesample, status, host, port, *rest = line.split()
                
                date, time = crush_date(timesample)
                host = get_value(host).split(':')[-1]
                port = get_value(port)
                if host and port:
                    print(f"{host} :: {port}")
                    
                    if status == 'ACCEPT':
                        connection = Connection(host)
                        connection.time_start = f"{date}_{time}"
                        
                        connections[f"{host}:{port}"] = connection
                        
                        count_accept += 1
                        if host in ip_count:
                            ip_count[host].count()
                        else:
                            try:
                                ip = IP(host)
                                location = gi.search(str(host))
                                ip.country = location["country"]
                                ip.country_code = location["code"]
                                ip_count[host] = ip
                            except Exception as e:
                                print(e)
                                print(host)
                                exit()
                            
                            
                    elif status == 'CLOSE':
                        if f"{host}:{port}" in connections:
                            connection = connections[f"{host}:{port}"]
                            connection.close()
                        else:
                            connection = Connection(host)
                            connection.close()
                            connections[f"{host}:{port}"] = connection
                            
                        connection.time_close = f"{date}_{time}"
                        connection.time_delta = rest[1]
                                            
                        count_closed += 1
                        
                    else:
                        pass
       
    print()        
    print('STATS')
    print(f"accepted: {count_accept}\nclosed: {count_closed}")
    print(f"open: {count_accept - count_closed}")
    
    # get open connections
    l = get_open_connections(connections)
    print(len(l))
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    print()
    print("IPs")
    print(f"unique ips: {len(ip_count)}")
    ip_count = sort_dict_by_value(ip_count, True)
    by_ip_file = os.path.join(OUTPUT_DIR, f"{timestamp}_by_ip.txt")
    with open(by_ip_file, 'w') as fp:
        for _, ip in ip_count.items():
            print(ip.ip, ip.frequency, ip.country_code, ip.country)
            fp.write(f"{ip.ip} {ip.frequency} {ip.country_code} {ip.country}\n")
            
            # count countrys
            if ip.country_code in country_count:
                country_count[ip.country_code] += ip.frequency
            
            else:
                country_count[ip.country_code] = 1
    
    
    print()
    print("COUNTRYs")
    countrys = sort_dict_by_value(country_count, True)
    by_country_file = os.path.join(OUTPUT_DIR, f"{timestamp}_by_country.txt")
    with open(by_country_file, 'w') as fp:
        for code, val in countrys.items():
            print(code, val)
            fp.write(f"{code} {val}\n")
        
    
    
    
if __name__ == '__main__':
    main()    
    
    
    
    
    
            
    
