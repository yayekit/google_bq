SELECT
  p.v2ProductName AS product_name,
  COUNTIF(h.eCommerceAction.action_type = 2) AS total_product_views,
  COUNTIF(h.eCommerceAction.action_type = 3) AS total_add_to_cart,
  COUNTIF(h.eCommerceAction.action_type = 6) AS total_purchases,
  COUNT(DISTINCT STRUCT(s.fullVisitorId, s.visitId)) AS sessions,
  COUNT(DISTINCT s.fullVisitorId) AS users
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_*` AS s
  CROSS JOIN UNNEST(s.hits) AS h
  CROSS JOIN UNNEST(h.product) AS p
WHERE
  _TABLE_SUFFIX BETWEEN '20170701' AND '20170731'
  AND p.v2ProductName IS NOT NULL
GROUP BY
  product_name
ORDER BY
  total_purchases DESC
LIMIT 100;
