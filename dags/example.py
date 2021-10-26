import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

logger = logging.getLogger("airflow.task")

dag = DAG(
    "example",
    schedule_interval="0 1 * * *",
    catchup=False,
    default_args={
        "owner": "Test",
        "depends_on_past": False,
        "start_date": datetime(2020, 8, 7),
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 2,
        "retry_delay": timedelta(seconds=30),
        "sla": timedelta(hours=23),
    },
)

# Jobs
passing1 = KubernetesPodOperator(
    namespace='rbs',
    image="python:3.6",
    cmds=["python","-c"],
    arguments=["for r in range(10): print('helloworld')"],
    labels={"foo": "bar"},
    name="passing-test",
    task_id="passing-task1",
    get_logs=True,
    dag=dag
)

# Jobs
passing2 = KubernetesPodOperator(
    namespace='rbs',
    image="python:3.6",
    cmds=["python","-c"],
    arguments=["for r in range(20): print('helloworld')"],
    labels={"foo": "bar"},
    name="passing-test",
    task_id="passing-task2",
    get_logs=True,
    dag=dag
)

passing1 >> passing2