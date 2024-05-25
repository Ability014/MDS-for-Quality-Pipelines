from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor
from great_expectations_provider.operators.great_expectations import (
	GreatExpectationsOperator,
)
from airflow.sensors.filesystem import FileSensor
import pendulum

from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.operators import DbtRunOperationOperator
from cosmos.profiles import PostgresUserPasswordProfileMapping
from airflow.datasets import Dataset
from datetime import datetime

POSTGRES_CONNECTION_ID = 'postgres_docker'
POSTGRES_SCHEMA = 'public'
MY_GX_DATA_CONTEXT = '/opt/airflow/ge/gx'
#RAW_PRODUCTS_FILE = '/tmp/airbyte_local/json_from_faker/_airbyte_ra_products.jsonl'
#COPY_OF_RAW_PRODUCTS = '/tmp/airbyte_local/json_from_faker/moved_raw_products.jsonl'

with DAG(dag_id='validate_jaffle_fact_orders_dim_customers',
        default_args={'owner': 'airflow'},
        schedule=None,
        start_date=pendulum.today('UTC').add(days=-1)
   ) as dag:
   
   snow_gx_validate_fact_orders = GreatExpectationsOperator(
       task_id='run_gx_fact_orders_chkpoint',
       checkpoint_name='fact_orders_checkpoint',
       data_context_root_dir=MY_GX_DATA_CONTEXT,
       return_json_dict=True,
   )

   snow_gx_validate_dim_customers = GreatExpectationsOperator(
       task_id='run_gx_dim_customers_chkpoint',
       checkpoint_name='dim_customers_checkpoint',
       data_context_root_dir=MY_GX_DATA_CONTEXT,
       return_json_dict=True,
   )

   [snow_gx_validate_fact_orders, snow_gx_validate_dim_customers]