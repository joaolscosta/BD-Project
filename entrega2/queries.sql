/* A PARTIR DAQUI É TUDO INVENTADO */

/* Exercicio 1 */
SELECT DISTINCT
  c.name
FROM 
  Customer c
INNER JOIN
  "order" o ON c.cust_no = o.cust_no
INNER JOIN
  contains cs ON o.order_no = cs.order_no
INNER JOIN
  Product p ON cs.sku = p.sku
WHERE
  p.price > 50
AND
  o.date > '2022-12-31'
AND
  o.date < '2024-01-01';

/* Exercicio 2 */

WITH EJAN2023 AS
  (
    SELECT DISTINCT
      e.name
    From
      Employee e
    INNER JOIN
      process p ON e.ssn = p.ssn
    INNER JOIN
      "order" o ON p.order_no = o.order_no
    WHERE
      o.date > '2022-12-31'
    and
      o.date < '2023-02-01'
  ),

EWHA AS 
  (
    SELECT DISTINCT 
      e.name
    FROM 
      Employee e
    WHERE e.ssn IN (
      SELECT 
        w.ssn
      FROM 
        works w
      JOIN Warehouse wh ON w.address = wh.address
    )
    AND e.ssn NOT IN (
      SELECT 
        w.ssn
      FROM 
        works w
      JOIN Office o ON w.address = o.address
    )
  )

SELECT DISTINCT
  name
FROM
  EJAN2023
INTERSECT
  SELECT DISTINCT
    name
  FROM
    EWHA;

/* Exercicio 3 */

with sold as (
  SELECT
    *
  FROM
    contains cs
  INNER JOIN
    sale s ON cs.order_no = s.order_no
),
bestseller as (
  SELECT
    s.sku
  FROM
    sold s
  GROUP BY
    s.sku
  HAVING 
    SUM(s.quantity) >= ALL (
      SELECT
        SUM(s.quantity)
      FROM
        sold s
      GROUP BY
        s.sku
  )
)
SELECT DISTINCT
  p.name
FROM
  bestseller bs
INNER JOIN
  Product p ON bs.sku = p.sku;

/* Exercicio 4 */

SELECT 
  query.order_no, SUM(query.total)
FROM
  (
    SELECT 
      s.order_no, ct.quantity*p.price as total
    FROM
      Product p
    INNER JOIN
      contains ct ON p.sku = ct.sku
    INNER JOIN
      sale s ON s.order_no = ct.order_no
  ) as query
GROUP BY
  query.order_no;

