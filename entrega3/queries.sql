-- 1

SELECT c.cust_no, name
FROM customer c
JOIN Pay p ON c.cust_no = p.cust_no
HAVING num > ALL
    (
      SELECT COUNT(*)
      FROM Pay
      GROUP BY cust_no
      ) as num
