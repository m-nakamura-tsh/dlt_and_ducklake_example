MODEL (
  name summary.kennedy_space_center_popular_contents,
  kind INCREMENTAL_BY_TIME_RANGE (
    time_column access_date,
    lookback 2,
  ),
  cron '@daily'
);

SELECT
    access_date,
    path,
    COUNT(*) AS request_count
FROM my_lakehouse.my_lake_dataset.kennedy_space_center
WHERE
  access_date BETWEEN @start_dt AND @end_dt
GROUP BY access_date, path
ORDER BY access_date, request_count DESC
LIMIT 20;

