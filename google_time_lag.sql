WITH first_visits AS (
  SELECT 
    fullVisitorId, 
    MIN(DATE(TIMESTAMP_SECONDS(visitStartTime))) AS first_visit_date -- getting the first date for each customer visit
  FROM 
    `bigquery-public-data.google_analytics_sample.ga_sessions_*`
  GROUP BY 
    fullVisitorId
),

first_purchases AS (
  SELECT 
    fullVisitorId, 
    MIN(DATE(TIMESTAMP_SECONDS(visitStartTime))) AS first_purchase_date
  FROM 
    `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
  WHERE 
    hits.transaction.transactionId IS NOT NULL
  GROUP BY 
    fullVisitorId
),

time_lags AS (
  SELECT 
    fullVisitorId,
    DATE_DIFF(first_purchase_date, first_visit_date, DAY) AS time_lag
  FROM 
    first_visits
  JOIN 
    first_purchases
  USING (fullVisitorId)
)

SELECT 
  CASE 
    WHEN time_lag BETWEEN 0 AND 11 THEN CAST(time_lag AS STRING)
    WHEN time_lag BETWEEN 12 AND 30 THEN '12-30'
    ELSE '30+'
  END AS time_lag_bucket,
  COUNT(*) AS conversions,
  0.00 AS conversion_value,  -- Placeholder as we don't have actual conversion values
  ROUND(COUNT(*) / (SELECT COUNT(*) FROM time_lags) * 100, 2) AS percentage_of_total
FROM 
  time_lags
GROUP BY 
  time_lag_bucket
ORDER BY 
  CASE 
    WHEN time_lag_bucket = '12-30' THEN 12
    WHEN time_lag_bucket = '30+' THEN 31
    ELSE CAST(time_lag_bucket AS INT64)
  END