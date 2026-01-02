from pathlib import Path
from sqlmesh.core.config import (
    Config,
    GatewayConfig,
    DuckDBConnectionConfig,
    ModelDefaultsConfig,
    LinterConfig,
)
from sqlmesh.core.config.connection import DuckDBAttachOptions

config = Config(
    gateways={
        "duckdb": GatewayConfig(
            connection=DuckDBConnectionConfig(
                catalogs={
                    # persistent catalog
                    "persistent": "../data/local_data_mart.duckdb",
                    # ducklake catalog
                    "my_lakehouse": DuckDBAttachOptions(
                        type="ducklake",
                        path="../data/catalog.ducklake.sqlite3",
                        data_path=str(Path("../data/storage").resolve()),
                    ),
                },
                extensions=["ducklake"],
            ),
            state_connection=DuckDBConnectionConfig(
                database="../data/sqlmesh_state.duckdb",
            ),
        )
    },
    default_gateway="duckdb",
    model_defaults=ModelDefaultsConfig(
        dialect="duckdb",
        start="1995-01-01",
        cron="@daily",
    ),
    linter=LinterConfig(
        enabled=True,
        rules={
            "ambiguousorinvalidcolumn",
            "invalidselectstarexpansion",
            "noambiguousprojections",
        },
    ),
)
