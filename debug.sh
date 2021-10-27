#!/bin/sh

# Before executed it, create the 'venv' pyvirtual environment

activate() {
    . ./venv/bin/activate
}

activate

AIRFLOW_VERSION=2.1.0
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip3 install "apache-airflow[async,postgres,kubernetes]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
