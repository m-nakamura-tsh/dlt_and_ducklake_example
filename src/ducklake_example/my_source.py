import dlt
import pandas as pd
import re
from pathlib import Path
import gzip


# Apache Common Log Format 用の正規表現
pattern = re.compile(
    r"(?P<host>\S+) "  # host
    r"\S+ \S+ "  # ident, authuser（今回は無視）
    r"\[(?P<time>.*?)\] "  # time
    r'"(?P<method>\S+) '  # HTTP method
    r"(?P<path>\S+) "  # path
    r'(?P<protocol>[^"]+)" '  # protocol
    r"(?P<status>\d+) "  # status code
    r"(?P<size>\d+)"  # response size
)


@dlt.source
def webaccess_data(
    source_data_path: Path = Path("./source_data/NASA_access_log_Jul95.gz"),
):
    @dlt.resource(name="kennedy_space_center", write_disposition="merge", merge_key=['access_date'])
    def kennedy_space_center_access():
        records = []
        # for line in StringIO(log_text):
        with gzip.open(
            source_data_path, "rt", encoding="utf_8", errors="replace"
        ) as log_file:
            for line in log_file:
                match = pattern.search(line)
                if match:
                    records.append(match.groupdict())

        df = pd.DataFrame(records)
        # 型変換
        df["status"] = df["status"].astype(int)
        df["size"] = df["size"].astype(int)
        df["time"] = pd.to_datetime(df["time"], format="%d/%b/%Y:%H:%M:%S %z")
        df["access_date"] = df["time"].dt.normalize()

        print(f"{df.columns=}")
        # ['host', 'time', 'method', 'path', 'protocol', 'status', 'size',
        # 'access_date']
        print(f"{df.shape=}")

        return df.to_dict(orient="records")

    return kennedy_space_center_access


if __name__ == "__main__":
    source = webaccess_data(Path("./source_data/NASA_access_log_Jul95.gz"))
    print(source.resources.keys())
    # breakpoint()
    resource = source.resources["kennedy_space_center"]
    for i, log in enumerate(resource):
        print(log)
        if i > 100:
            break
