#!/usr/bin/env python3

import nipyapi
import requests
import logging
import os

log = logging.getLogger("Nifi-Deployer")
log.setLevel(logging.INFO)

api_suffix = "/nifi-api"
registry_api_suffix = "/nifi-registry-api"

registry_deployment = {
    "api": os.environ["REGISTRY_URL"] + ":" + os.environ["REGISTRY_INTERNAL_PORT"] + registry_api_suffix,
    "url": os.environ["REGISTRY_URL"] + ":" + os.environ["REGISTRY_INTERNAL_PORT"],
    "name": os.environ["REGISTRY_NAME"],
    "description": os.environ["REGISTRY_DESCRIPTION"]
}

producer_deployment = {
   "api": os.environ["NIFI_PRODUCER_URL"] + ":" + os.environ["NIFI_PRODUCER_INTERNAL_PORT"] + api_suffix,
   "bucket_name": os.environ["NIFI_PRODUCER_BUCKET_NAME"],
   "flow_name": os.environ["NIFI_PRODUCER_FLOW_NAME"],
   "version_number": int(os.environ['NIFI_PRODUCER_FLOW_VERSION']),
   "process_group_name": os.environ['NIFI_PRODUCER_PG_NAME'] 
}

consumer_deployment = {
   "api": os.environ["NIFI_CONSUMER_URL"] + ":" + os.environ["NIFI_CONSUMER_INTERNAL_PORT"] + api_suffix,
   "bucket_name": os.environ["NIFI_CONSUMER_BUCKET_NAME"],
   "flow_name": os.environ["NIFI_CONSUMER_FLOW_NAME"],
   "version_number": int(os.environ['NIFI_CONSUMER_FLOW_VERSION']),
   "process_group_name": os.environ['NIFI_CONSUMER_PG_NAME']
}

deployments = [consumer_deployment, producer_deployment]

def wait_nifis_up():
    log.info("WAITING UNTIL ALL NIFI INSTANCES ARE READY...")
    for deployment in [registry_deployment] + deployments:
        log.info("WAITING FOR " + deployment['api'] + " TO BE READY")
        nipyapi.utils.set_endpoint(deployment['api'])
        nipyapi.utils.wait_to_complete(
            test_function=nipyapi.utils.is_endpoint_up,
            endpoint_url=deployment['api'].replace("-api", ""),
            nipyapi_delay=nipyapi.config.long_retry_delay,
            nipyapi_max_wait=nipyapi.config.long_max_wait
        )
        log.info(deployment['api'] + " IS READY.")
    log.info("ALL NIFI INSTANCES ARE READY.")

def get_nifis_without_registry():
    result = []
    for deployment in deployments:
       nipyapi.config.nifi_config.host = deployment['api']
       clients = nipyapi.versioning.list_registry_clients()
       if not clients.registries: 
           result.append(deployment)
           log.info(deployment['bucket_name'] + " ADDED TO THE LIST OF ENDPOINTS STILL WITHOUT REGISTRY.")
    return result

def attach_nifis_to_registry(deployments_missing):
    for deployment in deployments_missing:
        nipyapi.utils.set_endpoint(deployment['api'])
        nipyapi.versioning.create_registry_client(
            name=registry_deployment['name'],
            uri=registry_deployment['url'],
            description=registry_deployment['description']
        )
        log.info("NIFI-REGISTRY HAS BEEN ADDED TO: " + deployment['api'] + " SUCCESSFULLY.")

def deploy_flows():
    for deploy in deployments:
        nipyapi.utils.set_endpoint(deploy['api'])
        nipyapi.utils.set_endpoint(registry_deployment['api'])
        process_group_name = deploy["process_group_name"]
        if nipyapi.canvas.get_process_group(process_group_name, greedy=False):
            log.info(process_group_name + " ALREADY DEPLOYED. SKIPPING...")
            continue
        else:
            log.info("DEPLOYING PROCESS GROUP NAME: " + process_group_name)
        bucket = nipyapi.versioning.get_registry_bucket(deploy["bucket_name"])
        flow = nipyapi.versioning.get_flow_in_bucket(
            bucket_id=bucket.identifier,
            identifier=deploy["flow_name"]
        )
        reg_client = nipyapi.versioning.get_registry_client(registry_deployment['name'])
        nipyapi.versioning.deploy_flow_version(
            parent_id=nipyapi.canvas.get_root_pg_id(),
            location=(50, 50),
            bucket_id=bucket.identifier,
            flow_id=flow.identifier,
            reg_client_id=reg_client.id,
            version=deploy["version_number"]
        )
    log.info("ALL NIFI INSTANCES ARE CONFIGURED.")

def start_flows():
    log.info("STARTING PROCESS GROUPS...")
    for deployment in deployments:
        api = deployment['api']
        nipyapi.utils.set_endpoint(api)
        process_group_name = deployment['process_group_name']
        stopped_before = nipyapi.canvas.get_process_group_status(detail='all').stopped_count
        if stopped_before == 0:
            log.info("PROCESS GROUP: " + process_group_name + " ON " + api + " IS ALREADY RUNNING. SKIPPING...")
            continue
        pg_id = nipyapi.canvas.get_process_group(process_group_name, greedy=False).component.id 
        nipyapi.canvas.schedule_process_group(pg_id, True)
        total_running_processors = stopped_before - nipyapi.canvas.get_process_group_status(detail='all').stopped_count
        log.info("STARTED " + str(total_running_processors) + " PROCESSORS IN THE PROCESS GROUP " + process_group_name + ".")
    log.info("ALL PROCESS GROUPS ARE RUNNING.")

def main():
    wait_nifis_up()
    nifis_to_setup = get_nifis_without_registry()
    attach_nifis_to_registry(nifis_to_setup)
    deploy_flows()
    start_flows()

if __name__ == "__main__":
    main()
