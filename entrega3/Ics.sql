--R1:



-- R2:
CREATE TRIGGER CheckValidWorkplace
BEFORE INSERT OR UPDATE ON Workplace
FOR EACH ROW
BEGIN
  IF (NEW.address NOT IN (SELECT address FROM Office) AND
      NEW.address NOT IN (SELECT address FROM Warehouse)) 
    OR
     ( NEW.address IN (SELECT address FROM Office) AND
       NEW.address IN (SELECT address FROM Warehouse))  
    THEN
    RAISE EXCEPTION 'Workplace must be either an Office or a Warehouse and not Both!';
  END IF;
END

-- R3:
CREATE TRIGGER CheckValidOrder
BEFORE INSERT OR UPDATE ON 'order'
FOR EACH ROW
BEGIN
  IF (NEW.order_no NOT IN (SELECT order_no FROM contains)) THEN
    RAISE EXCEPTION 'Orders must have at least one product!';
  END IF;
END