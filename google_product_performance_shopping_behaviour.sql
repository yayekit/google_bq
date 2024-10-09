WITH product_actions AS (
  SELECT
    product.v2ProductName AS product_name,
    fullVisitorId,
    visitId,
    SUM(CASE WHEN hits.eCommerceAction.action_type = '2' THEN 1 ELSE 0 END) AS product_views,
    SUM(CASE WHEN hits.eCommerceAction.action_type = '3' THEN 1 ELSE 0 END) AS add_to_cart,
    SUM(CASE WHEN hits.eCommerceAction.action_type = '6' THEN 1 ELSE 0 END) AS purchases
  FROM
    `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits,
    UNNEST(hits.product) AS product
  WHERE
    _TABLE_SUFFIX BETWEEN '20170701' AND '20170731'
    AND product.v2ProductName IS NOT NULL
  GROUP BY
    product_name, fullVisitorId, visitId
)

SELECT
  product_name,
  SUM(product_views) AS total_product_views,
  SUM(add_to_cart) AS total_add_to_cart,
  SUM(purchases) AS total_purchases,
  COUNT(DISTINCT CONCAT(fullVisitorId, CAST(visitId AS STRING))) AS sessions,
  COUNT(DISTINCT fullVisitorId) AS users
FROM
  product_actions
GROUP BY
  product_name
ORDER BY
  total_purchases DESC
LIMIT 100