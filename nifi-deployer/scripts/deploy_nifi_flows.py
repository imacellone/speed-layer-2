#!/usr/bin/env python3

import nipyapi
import requests
import logging
import os

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

producer_version = int(os.environ['NIFI_PRODUCER_FLOW_VERSION'])
consumer_version = int(os.environ['NIFI_CONSUMER_FLOW_VERSION'])
producer_process_group_name = os.environ['NIFI_PRODUCER_PG_NAME']
consumer_process_group_name = os.environ['NIFI_CONSUMER_PG_NAME']

def wait_nifis_up():
    log.info("WAITING UNTIL ALL NIFI INSTANCES ARE READY...")
    for instance in all_nifi_apis + [registry_api]:
        log.info("WAITING FOR " + instance + " TO BE READY")
        nipyapi.utils.set_endpoint(instance)
        nipyapi.utils.wait_to_complete(
            test_function=nipyapi.utils.is_endpoint_up,
            endpoint_url=instance.replace("-api", ""),
            nipyapi_delay=nipyapi.config.long_retry_delay,
            nipyapi_max_wait=nipyapi.config.long_max_wait
        )
        log.info(instance + "IS READY.")
    log.info("ALL NIFI INSTANCES ARE READY.")

def get_nifis_without_registry():
    result = []
    for endpoint in all_nifi_apis:
       nipyapi.config.nifi_config.host = endpoint
       clients = nipyapi.versioning.list_registry_clients()
       if not clients.registries: 
           result.append(endpoint)
           log.info(endpoint + " ADDED TO THE LIST OF ENDPOINTS STILL WITHOUT REGISTRY.")
    return result

def attach_nifis_to_registry(endpoints):
    for endpoint in endpoints:
        nipyapi.utils.set_endpoint(endpoint)
        nipyapi.versioning.create_registry_client(
            name=registry_name,
            uri=registry_base_url,
            description=registry_description
        )
        log.info("NIFI-REGISTRY HAS BEEN ADDED TO: " + endpoint + " SUCCESSFULLY.")

def deploy_flows():
    deploy_flow(nifi_producer_api, "message-producer", "message-producer", producer_version, producer_process_group_name)
    deploy_flow(nifi_consumer_api, "message-consumer", "write-to-mongo", consumer_version, consumer_process_group_name)

def deploy_flow(nifi_api, bucket_name, flow_name, version_number, process_group_name):
    nipyapi.utils.set_endpoint(nifi_api)
    nipyapi.utils.set_endpoint(registry_api)
    if nipyapi.canvas.get_process_group(process_group_name, greedy=False):
        log.info(process_group_name + " ALREADY DEPLOYED. SKIPPING...")
        return
    else:
        log.info("DEPLOYING PROCESS GROUP NAME: " + process_group_name)
    bucket = nipyapi.versioning.get_registry_bucket(bucket_name)
    flow = nipyapi.versioning.get_flow_in_bucket(
        bucket_id=bucket.identifier,
        identifier=flow_name
    )
    reg_client = nipyapi.versioning.get_registry_client(registry_name)
    nipyapi.versioning.deploy_flow_version(
        parent_id=nipyapi.canvas.get_root_pg_id(),
        location=(20, 20),
        bucket_id=bucket.identifier,
        flow_id=flow.identifier,
        reg_client_id=reg_client.id,
        version=version_number
    )
    """pg_id = nipyapi.canvas.get_process_group(process_group_name, greedy=False).component.id
    nipyapi.canvas.schedule_process_group(pg_id, True)

def start_flows():
    pass
"""

def main():
    wait_nifis_up()
    nifis_to_setup = get_nifis_without_registry()
    attach_nifis_to_registry(nifis_to_setup)
    deploy_flows()
    """start_flows()"""
    log.info("ALL NIFI INSTANCES HAVE BEEN SUCCESSFULLY DEPLOYED. ENJOY!")

if __name__ == "__main__":
    main()
