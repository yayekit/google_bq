WITH user_paths AS (
  SELECT
    fullVisitorId,
    visitId,
    channelGrouping,
    totals.transactions,
    DATE(PARSE_TIMESTAMP('%Y%m%d', date)) AS visit_date,
    ROW_NUMBER() OVER (PARTITION BY fullVisitorId ORDER BY DATE(PARSE_TIMESTAMP('%Y%m%d', date))) AS visit_sequence
  FROM
    `bigquery-public-data.google_analytics_sample.ga_sessions_*`
),
path_creation AS (
  SELECT
    fullVisitorId,
    STRING_AGG(channelGrouping, ' > ' ORDER BY visit_sequence) AS conversion_path,
    COUNT(DISTINCT visitId) AS sessions,
    SUM(transactions) AS transactions
  FROM
    user_paths
  GROUP BY
    fullVisitorId
)
SELECT
  conversion_path,
  COUNT(*) AS user_count,
  SUM(sessions) AS total_sessions,
  SUM(transactions) AS total_transactions,
  -- below are 2 additional metrics that may be avoided; were included for a potential use in stats
  SAFE_DIVIDE(SUM(transactions), COUNT(*)) AS transactions_per_user, 
  SAFE_DIVIDE(SUM(sessions), COUNT(*)) AS sessions_per_user
FROM
  path_creation
GROUP BY
  conversion_path
ORDER BY
  total_transactions DESC,
  total_sessions DESC
LIMIT 100