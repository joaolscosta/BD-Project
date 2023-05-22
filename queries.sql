/* A PARTIR DAQUI É TUDO INVENTADO */

/* Exercicio 1 */
SELECT DISTINCT
  c.name
FROM 
  Customer c
INNER JOIN
  Order o ON c.cust_no = o.cust_no
INNER JOIN
  contains cs ON o.order_no = cs.order_no
INNER JOIN
  Product p ON cs.sku = p.sku
WHERE
  p.price > 50;

/* Exercicio 3 */
SELECT DISTINCT
  p.name
FROM
  Product p
INNER JOIN
  contains cs ON p.sku = cs.sku
INNER JOIN
  Sales s ON s.order_no = cs.order_no
WHERE 
  cs.quantity = (
    SELECT
      MAX(cs.quantity)
    FROM
      contains cs
);