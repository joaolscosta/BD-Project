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
  p.price > 50;

/* Exercicio 2 */
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

INTERSECT 

SELECT DISTINCT
  e.name
From
  Employee e
INNER JOIN
  works wk ON e.ssn = wk.ssn
INNER JOIN
  (SELECT * 
  FROM
    Workplace wkp
  Where
    wkp.address NOT IN (
      SELECT
        o.address
      FROM
        Office o
    )
  ) wp ON wk.address = wp.address;

INNER JOIN
  Warehouse wa ON wp.address = wa.address

/* Exercicio 3 */
SELECT DISTINCT
  p.name
FROM
  Product p
INNER JOIN
  contains cs ON p.sku = cs.sku
INNER JOIN
  Sale s ON s.order_no = cs.order_no
WHERE 
  cs.quantity = (
    SELECT
      MAX(cs.quantity)
    FROM
      contains cs
);