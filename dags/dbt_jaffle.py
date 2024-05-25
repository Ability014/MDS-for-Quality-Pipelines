from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping, SnowflakeUserPasswordProfileMapping
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.datasets import Dataset
from datetime import datetime

profile_config = ProfileConfig(
    profile_name="dbt_jaffle_shop",
    target_name="RAW",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake",
        profile_args={
            "database": "JAFFLE_SHOP",
            "schema": "CORE",
        },
    ),
)

my_dbt_dag = DbtDag(
    project_config=ProjectConfig(
        "/opt/airflow/dbt/dbt_jaffle_shop",
    ),
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path="/home/airflow/.local/bin/dbt",
    ),
    # normal dag parameters
    schedule_interval=None,
    start_date=datetime(2024, 5, 24),
    catchup=False,
    dag_id="run_dbt_jaffle",
    default_args={"retries": 2},
)

my_dbt_dag