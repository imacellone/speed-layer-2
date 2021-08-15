FROM python:slim-buster

RUN ["/bin/bash", "-c", "pip install nipyapi && pip install requests"]

ENTRYPOINT ["/bin/bash", "-c", "chmod +x /scripts/* && python3 /scripts/deploy_nifi_flows.py"]