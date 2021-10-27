import logging
import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from kubernetes.client import models as k8s

logger = logging.getLogger("airflow.task")

dag = DAG(
    "example",
    schedule_interval="0 1 * * *",
    catchup=False,
    default_args={
        "owner": "Test",
        "start_date": datetime(2020, 8, 7),
        "retries": 2,
        "retry_delay": timedelta(seconds=30),
    },
)

# Jobs
task1 =  KubernetesPodOperator(
    namespace='default',
    image="python:2.7",
    cmds=["python","-c"],
    arguments=["for r in range(3): print('running script by ptyhon 2.7')"],
    name="task1",
    task_id="task1",
    get_logs=True,
    dag=dag
)
# Jobs
task2 =  KubernetesPodOperator(
    namespace='default',
    image="python:3.6",
    cmds=["python","-c"],
    arguments=["for r in range(3): print('running script by python 3.6')"],
    name="task2",
    task_id="task2",
    get_logs=True,
    dag=dag
)


task1 >> task2