#!/usr/bin/env python3

import nipyapi
import requests
import time
import logging

""" Logging """
log = logging.getLogger("Nifi-Deployer")
log.setLevel(logging.INFO)
logging.getLogger('nipyapi.versioning').setLevel(logging.INFO)
logging.getLogger('nipyapi.utils').setLevel(logging.INFO)

""" Suffixes """
api_suffix = "-api"
nifi_suffix = "/nifi"
registry_suffix = "/nifi-registry"

"""NiFi Endpoints"""
nifi_producer_base_url = "http://nifi-file-reader:8080"
nifi_consumer_base_url = "http://nifi-kafka-consumer:8080"

nifi_producer_ui_url = nifi_producer_base_url + nifi_suffix
nifi_consumer_ui_url = nifi_consumer_base_url + nifi_suffix

nifi_producer_api = nifi_producer_ui_url + api_suffix
nifi_consumer_api = nifi_consumer_ui_url + api_suffix
all_nifi_apis = [nifi_producer_api, nifi_consumer_api]

"""NiFi-Registry properties"""
registry_base_url = "http://nifi-registry:18080"
registry_ui_url = registry_base_url + registry_suffix
registry_api = registry_ui_url + api_suffix
registry_name = "Nifi Registry"
registry_description = registry_name

"""DEPLOY"""

def wait_nifis_up():
    for instance in all_nifi_apis + [registry_api]:
        log.info("Waiting for " + instance + " to be ready")
        nipyapi.utils.set_endpoint(instance)
        nipyapi.utils.wait_to_complete(
            test_function=nipyapi.utils.is_endpoint_up,
            endpoint_url=instance.replace("-api", ""),
            nipyapi_delay=nipyapi.config.long_retry_delay,
            nipyapi_max_wait=nipyapi.config.long_max_wait
        )
        log.info(instance + " is ready")

def get_nifis_without_registry():
    result = []
    for endpoint in all_nifi_apis:
       nipyapi.config.nifi_config.host = endpoint
       clients = nipyapi.versioning.list_registry_clients()
       if not clients.registries: 
           result.append(endpoint)
           log.info(endpoint + " added to the list of endpoints still without Registry.")
    return result

def attach_nifis_to_registry(endpoints):
    for endpoint in endpoints:
        nipyapi.utils.set_endpoint(endpoint)
        nipyapi.versioning.create_registry_client(
            name=registry_name,
            uri=registry_base_url,
            description=registry_description
        )
        log.info("NiFi-Registry has been added to: " + endpoint + " successfully.")

def main():
    """wait_for_nifis()"""
    wait_nifis_up()
    nifis_to_setup = get_nifis_without_registry()
    attach_nifis_to_registry(nifis_to_setup)
    log.info("All NiFi instances have now a Registry configured.")

if __name__ == "__main__":
    main()
