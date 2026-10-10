from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "jorge",
    "depends_on_past": False,
}


with DAG(
    dag_id="meetup_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 10, 1),
    schedule="*/15 * * * *",
    catchup=False,
    tags=["meetup", "snowflake", "aws"],
) as dag:

    generate_synthetic_data = BashOperator(
        task_id="generate_synthetic_data",
        bash_command="""
        cd /opt/airflow/project
        python -m pipelines.run_synthetic_generation
        """
    )

    load_bronze = BashOperator(
        task_id="load_bronze",
        bash_command="""
        cd /opt/airflow/project
        python -m pipelines.run_bronze_load
        """
    )

    load_silver = BashOperator(
        task_id="load_silver",
        bash_command="""
        cd /opt/airflow/project
        python -m pipelines.run_silver_load
        """
    )

    load_gold = BashOperator(
        task_id="load_gold",
        bash_command="""
        cd /opt/airflow/project
        python -m pipelines.run_gold_load
        """
    )

    export_gold = BashOperator(
        task_id="export_gold",
        bash_command="""
        cd /opt/airflow/project
        python -m pipelines.run_export_gold
        """
    )

    (
        generate_synthetic_data
        >> load_bronze
        >> load_silver
        >> load_gold
        >> export_gold
    )