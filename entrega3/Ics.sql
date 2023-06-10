--R1:
CREATE OR REPLACE FUNCTION ValidAge() RETURNS TRIGGER AS
$$
  BEGIN
    IF ((CURRENT_DATE - 6570) < NEW.bdate ) THEN
      RAISE EXCEPTION 'Employees must be 18 years old';
    END IF;
    RETURN NEW;
  END
$$ LANGUAGE plpgsql;

CREATE TRIGGER CheckValidAge
BEFORE INSERT OR UPDATE ON employee
FOR EACH ROW EXECUTE PROCEDURE ValidAge();

--Nao tenho a certeza, by : nunes



-- R2:
CREATE OR REPLACE FUNCTION CheckValidWorkplace() RETURNS TRIGGER AS
$$
  BEGIN
    IF (NEW.address NOT IN (SELECT address FROM Office) AND
        NEW.address NOT IN (SELECT address FROM Warehouse)) 
      OR
       ( NEW.address IN (SELECT address FROM Office) AND
         NEW.address IN (SELECT address FROM Warehouse))  
      THEN
      RAISE EXCEPTION 'Workplace must be either an Office or a Warehouse and not Both!';
    END IF;
    RETURN NEW;
  END
$$ LANGUAGE plpgsql;

CREATE TRIGGER CheckValidWorkplace
BEFORE INSERT OR UPDATE ON Workplace
FOR EACH ROW EXECUTE FUNCTION CheckValidWorkplace();

-- R3:
CREATE OR REPLACE FUNCTION CheckValidOrder() RETURNS TRIGGER AS
$$
  BEGIN
    IF (NEW.order_no NOT IN (SELECT order_no FROM contains)) THEN
      RAISE EXCEPTION 'Orders must have at least one product!';
    END IF;
    RETURN NEW;
  END
$$ LANGUAGE plpgsql;

CREATE TRIGGER CheckValidOrder
BEFORE INSERT OR UPDATE ON orders
FOR EACH ROW EXECUTE PROCEDURE CheckValidOrder();

