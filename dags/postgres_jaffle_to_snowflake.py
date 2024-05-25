from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor
import pendulum

from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.operators import DbtRunOperationOperator
from cosmos.profiles import PostgresUserPasswordProfileMapping
from airflow.datasets import Dataset
from datetime import datetime

AIRBYTE_CONNECTION_ID = '24f75469-58e5-46ec-b42d-a8b387a0a4d0'
#RAW_PRODUCTS_FILE = '/tmp/airbyte_local/json_from_faker/_airbyte_ra_products.jsonl'
#COPY_OF_RAW_PRODUCTS = '/tmp/airbyte_local/json_from_faker/moved_raw_products.jsonl'


with DAG(dag_id='postgres_jaffle_to_snowflake',
        default_args={'owner': 'airflow'},
        schedule='@daily',
        start_date=pendulum.today('UTC').add(days=-1)
   ) as dag:

   trigger_airbyte_sync = AirbyteTriggerSyncOperator(
       task_id='airbyte_trigger_sync',
       airbyte_conn_id='airbyte_conn',
       connection_id=AIRBYTE_CONNECTION_ID,
       asynchronous=True
   )

   wait_for_sync_completion = AirbyteJobSensor(
       task_id='airbyte_check_sync',
       airbyte_conn_id='airbyte_conn',
       airbyte_job_id=trigger_airbyte_sync.output
   )

   run_this_last = EmptyOperator(
       task_id="job_sync_completed",
   )

   my_dbt_dag = TriggerDagRunOperator(
       task_id='trigger_dbt_jaffle',
       trigger_dag_id='run_dbt_jaffle',
       trigger_rule=TriggerRule.ALL_SUCCESS,
       dag=dag
   )

   my_snow_gx_dag = TriggerDagRunOperator(
       task_id='trigger_snow_gx_validation',
       trigger_dag_id='validate_datamart_prod_core',
       trigger_rule=TriggerRule.ALL_SUCCESS,
       dag=dag
   )

   trigger_airbyte_sync >> wait_for_sync_completion >>  run_this_last  >> my_dbt_dag >> my_snow_gx_dag