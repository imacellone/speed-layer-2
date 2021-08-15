#!/usr/bin/env python3

import nipyapi
import requests
import time

"""NiFi Endpoints"""
nifi_message_producer_endpoint = "http://nifi-file-reader:8080/nifi-api" 
nifi_message_consumer_endpoint = "http://nifi-kafka-consumer:8080/nifi-api"
nifi_system_diagnostics_uri = "/system-diagnostics"
nifi_message_producer_health_check = nifi_message_producer_endpoint + nifi_system_diagnostics_uri
nifi_message_consumer_health_check = nifi_message_consumer_endpoint + nifi_system_diagnostics_uri 

"""NiFi-Registry properties"""
nifi_registry_name = "Nifi Registry"
nifi_registry_url = "http://nifi-registry:18080"
nifi_registry_description = nifi_registry_name

"""CHECK IF IT IS ALREADY IMPORTED"""

"""DEPLOY"""

def wait_for_nifis():
    nifi_health_check_urls = [nifi_message_consumer_health_check, nifi_message_producer_health_check]
    for url in nifi_health_check_urls:
        wait_status_ok(url)

def wait_status_ok(url):
    wait_time = 10
    status_code = 404
    while status_code != requests.codes.ok:
        try:
            status_code = requests.get(url).status_code 
        except:
            time.sleep(wait_time)

def get_nifis_without_registry():
    endpoints = [nifi_message_producer_endpoint, nifi_message_consumer_endpoint]
    result = []
    for endpoint in endpoints:
       nipyapi.config.nifi_config.host = endpoint
       clients = nipyapi.versioning.list_registry_clients()
       if not clients.registries: 
           result.append(endpoint)
           print(endpoint + " added to the list of endpoints without Registry")
    return result

def attach_nifis_to_registry(endpoints):
    for endpoint in endpoints:
        attach_nifi_to_registry(
            endpoint,
            nifi_registry_name,
            nifi_registry_url,
            nifi_registry_description
        )
        print(endpoint + " has been added a Registry")

def attach_nifi_to_registry(nifi_endpoint, registry_name, registry_url, registry_description):
    nipyapi.utils.set_endpoint(nifi_endpoint)
    nipyapi.versioning.create_registry_client(
        name=registry_name,
        uri=registry_url,
        description=registry_description
    )

def main():
    wait_for_nifis()
    nifis_to_setup = get_nifis_without_registry()
    attach_nifis_to_registry(nifis_to_setup)
    print("Both NiFi instances are now connected to NiFi-Registry!")

if __name__ == "__main__":
    main()
