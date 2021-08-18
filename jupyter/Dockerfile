FROM continuumio/anaconda3
EXPOSE 8888
RUN ["/bin/bash", "-c", "conda install jupyter -y --quiet && \
                conda install -c anaconda pymongo -y && \
                conda install -c conda-forge mongoengine -y && \
                mkdir -p /opt/notebooks"]
ENTRYPOINT ["/bin/bash", "-c", "jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --NotebookApp.token='' --NotebookApp.password='' --no-browser --allow-root"]