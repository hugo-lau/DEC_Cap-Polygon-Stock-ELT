from dagster import Definitions
from Orchestration.assets.dbt.dbt import dbt_warehouse, dbt_warehouse_resource

defs = Definitions(
    assets=[dbt_warehouse],
    resources={
        "dbt_warehouse_resource": dbt_warehouse_resource
    },
)