import dlt
from dlt.destinations.impl.ducklake.configuration import DuckLakeCredentials
from pathlib import Path
from ducklake_example.my_source import webaccess_data

credentials = DuckLakeCredentials(
    "weblog_raw",
    catalog="sqlite:///data/catalog.ducklake.sqlite3",
    # storage=str(Path("./data/storage/").resolve()),
    storage=str(Path("./data/storage/")),
)
destination = dlt.destinations.ducklake(credentials=credentials)
pipeline = dlt.pipeline(
    pipeline_name="weblog_sample_pipeline",
    destination=destination,
    dataset_name="my_lake_dataset",
    # dev_mode=True,
)


if __name__ == "__main__":
    load_info = pipeline.run(
        data=webaccess_data, destination=destination, refresh="drop_sources"
    )
