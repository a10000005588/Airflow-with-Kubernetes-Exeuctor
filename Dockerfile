FROM apache/airflow:2.1.0 AS base

USER root
# install linux pakcages.
RUN apt-get update && apt-get install -y \
  sudo \
  git \
  procps \
  vim \
  gettext-base

# install google sdk
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz
RUN sudo mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh
RUN source /usr/local/gcloud/google-cloud-sdk/completion.bash.inc
RUN source /usr/local/gcloud/google-cloud-sdk/path.bash.inc
ENV PATH="/usr/local/gcloud/google-cloud-sdk/bin/:${PATH}"
RUN gcloud components update -q
RUN chmod -R 777 /opt

USER airflow
# add dependencies for http basic auth
RUN pip install --user --upgrade apache-airflow[password]
RUN pip install --upgrade google-cloud-bigquery
RUN pip install Flask-Bcrypt

# install airflow packages
RUN pip install apache-airflow[google]
RUN pip install "apache-airflow[async,postgres,google,kubernetes]"

# update airflow default configruation
COPY ./configs/airflow.cfg /opt/airflow
# add worker config files into image
COPY ./worker/ /opt/airflow/worker/
## add your custom dags in current docker build folder
COPY ./dags/ /opt/airflow/dags/