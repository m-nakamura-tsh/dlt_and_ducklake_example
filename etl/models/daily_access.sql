MODEL (
  name summary.kennedy_space_center,
  kind INCREMENTAL_BY_TIME_RANGE (
    time_column access_date,
    lookback 2,
  ),
  cron '@daily'
);

SELECT 
  access_date,
  host,
  time,
  method, 
  path,
  protocol,
  status,
  size
FROM my_lakehouse.my_lake_dataset.kennedy_space_center
WHERE
  access_date BETWEEN @start_dt AND @end_dt


