#!/usr/bin/python3
import os
from logging.config import dictConfig

import psycopg
from flask import flash
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool

import re


# postgres://{user}:{password}@{hostname}:{port}/{database-name}
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://db:db@postgres/db")

pool = ConnectionPool(conninfo=DATABASE_URL)
# the pool starts connecting immediately.

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
log = app.logger

@app.route("/", methods=("GET",))
def index():

    return render_template("index.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    
    if request.method == "POST":
        name = request.form.get("name")
        cust_no = request.form.get("cust_no")
        
        with pool.connection() as conn:
            with conn.cursor() as cur:
                # Check if the username exists in the Customer table
                cur.execute(
                    """
                    SELECT COUNT(*) FROM customer WHERE name = %s AND cust_no = %s;
                    """,
                    (name, cust_no),
                )
                count = cur.fetchone()[0]
                if count == 1:
                    
                    # Perform the login, as the username exists
                    # You can set some session variables or perform other actions to authenticate the user
                    return redirect(url_for("orders_index_private", cust_no=cust_no))
        
        # If the username is not found, you can display an error message
        error_message = "Invalid name or cust_no"
        return render_template("login_page.html", error_message=error_message)
    
    # Render the login page template for the initial GET request
    return render_template("login_page.html")



@app.route("/order_customer.html", methods=("GET",))
def order_customer_page():
    global order_no_count
    page_order_main = request.args.get("page", 1, type=int)
    per_page_order_main = 9
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            count_order_main = cur.execute(
                """
                SELECT COUNT(*) as count
                FROM customer
                WHERE cust_no >= 0;
                """
            ).fetchone()

            total_pages_order_main = math.ceil(count_order_main[0] / per_page_order_main)
            offset_order_main = (page_order_main - 1) * per_page_order_main
            cur.execute(
                """
                SELECT cust_no, name, email, phone
                FROM customer
                ORDER BY cust_no DESC
                LIMIT %s OFFSET %s;
                """,
                (per_page_order_main, offset_order_main),
            )
            customers = cur.fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    if order_no_count < count_order_main[-1]:
        order_no_count = count_order_main[-1]

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(customers)

    return render_template(
        "orders/order_customer.html",
        customers=customers,
        current_page=page_order_main,
        total_pages=total_pages_order_main,
    )


@app.route("/orders/<cust_no>", methods=("GET",))
def orders_index(cust_no):
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            count = cur.execute(
                """
                SELECT COUNT(*) as count
                FROM orders;
                """
            ).fetchone()
            
            orders = cur.execute(
                """
                SELECT DISTINCT order_no
                FROM orders JOIN contains USING (order_no)
                WHERE cust_no = %(cust_no)s
                AND NOT EXISTS (
                    SELECT 1
                    FROM pay
                    WHERE pay.order_no = orders.order_no
                )
                ORDER BY order_no;
                """,
                {"cust_no": cust_no},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

            contains = cur.execute(
                """
                SELECT order_no, sku, qty
                FROM orders JOIN contains USING (order_no)
                WHERE cust_no = %(cust_no)s
                AND NOT EXISTS (
                    SELECT 1
                    FROM pay
                    WHERE pay.order_no = orders.order_no
                )
                ORDER BY order_no;
                """,
                {"cust_no": cust_no},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

            pay = cur.execute(
                """
                SELECT order_no, cust_no
                FROM pay
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

            customer = cur.execute(
                """
                SELECT *
                FROM customer
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            ).fetchone()

            log.debug("Found 1 row.")

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(orders)
    return render_template("orders/orders_index.html", increment_counter=increment_counter,orders=orders, pay=pay, customer=customer,contains=contains)

@app.route("/orders/<cust_no>/private", methods=("GET",))
def orders_index_private(cust_no):


    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            
            
            orders = cur.execute(
                """
                SELECT DISTINCT order_no
                FROM orders JOIN contains USING (order_no)
                WHERE cust_no = %(cust_no)s
                AND NOT EXISTS (
                    SELECT 1
                    FROM pay
                    WHERE pay.order_no = orders.order_no
                )
                ORDER BY order_no;
                """,
                {"cust_no": cust_no},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

            contains = cur.execute(
                """
                SELECT order_no, sku, qty
                FROM orders JOIN contains USING (order_no)
                WHERE cust_no = %(cust_no)s
                AND NOT EXISTS (
                    SELECT 1
                    FROM pay
                    WHERE pay.order_no = orders.order_no
                )
                ORDER BY order_no;
                """,
                {"cust_no": cust_no},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

            pay = cur.execute(
                """
                SELECT order_no, cust_no
                FROM pay
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

            customer = cur.execute(
                """
                SELECT *
                FROM customer
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            ).fetchone()

            log.debug("Found 1 row.")




    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(orders)
    return render_template("orders/orders_index_private.html", increment_counter=increment_counter,orders=orders, pay=pay, customer=customer,contains=contains)


@app.route("/orders/<order_no>/", methods=("GET",))
def order_detail(order_no):
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            contains = cur.execute(
                """
                SELECT *
                FROM contains
                WHERE order_no = %(order_no)s;
                """,
                {"order_no": order_no},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

            qty_list = [contain[2] for contain in contains]
            

            order = cur.execute(
                """
                SELECT *
                FROM orders
                WHERE order_no = %(order_no)s;
                """,
                {"order_no": order_no},
            ).fetchone()

            log.debug(f"Found {cur.rowcount} rows.")

            products = cur.execute(
                """
                SELECT *
                FROM product JOIN contains USING (sku)
                WHERE order_no = %(order_no)s
                """,
                {"order_no": order_no},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

            price_list = [product[3] for  product in products]
            result_list = [qty * price for qty, price in zip(qty_list, price_list)]
            result_sum = sum(result_list)

    
    return render_template("orders/order_payment.html", qty_list=qty_list, price_list=price_list, order=order, products=products, result_sum=result_sum)

@app.route("/orders/add/<cust_no>", methods=("GET", "POST"))
def add_order(cust_no):
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            customer = cur.execute(
                """
                SELECT *
                FROM customer
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            ).fetchone()

            log.debug("Found 1 row.")

            products = cur.execute(
                """
                SELECT *
                FROM product
                WHERE NOT sku = '-1';
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return render_template("orders/add_order.html", customer=customer, products=products)


@app.route("/employee_index.html", methods=("GET",))
def employee_index():
    """Show all the accounts, most recent first."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            employees = cur.execute(
                """
                SELECT cust_no, name, email
                FROM customer
                ORDER BY cust_no DESC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(employees)

    return render_template("employee/employee_index.html", employees=employees)

@app.route("/products_index.html", methods=("GET",))
def products_page():
    page = request.args.get("page", 1, type=int)
    per_page = 12
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            
            count = cur.execute(
                """
                SELECT COUNT(*) as count
                FROM product
                WHERE NOT SKU = '-1';
                """
            ).fetchone()    
            
            total_pages = math.ceil(count[0] / per_page)
            offset = (page - 1) * per_page
            
            products = cur.execute(
                """
                SELECT SKU, name, price, description
                FROM product
                WHERE NOT SKU = '-1'
                ORDER BY SKU DESC
                LIMIT {0} OFFSET {1};
                """.format(per_page, offset),
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(products)

    return render_template("products/products_index.html", products=products,
        current_page=page,
        total_pages=total_pages)


@app.route("/products/<sku>/", methods=("GET",))
def product_detail(sku):
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            product = cur.execute(
                """
                SELECT *
                FROM product
                WHERE SKU = %(SKU)s;
                """,
                {"SKU": sku},
            ).fetchone()
            log.debug(f"Found {cur.rowcount} rows.")
    
    return render_template("products/product.html", product=product)

@app.route("/products/create", methods=("GET", "POST"))
def create_product():
    if request.method == "GET":
        return render_template("products/create_product.html", error=False)

    sku= request.form["sku"]
    name= request.form["name"]
    price= request.form["price"]
    description= request.form["description"]
    ean= request.form["ean"]

    if re.search("^(([a-zA-Z])|([0-9])){25}$", sku) is None:
        return render_template("products/create_product.html", error="SKU must be 25 alphanumeric characters.")

    elif len(name) > 200:
        return render_template("products/create_product.html", error="Name must be less than 200 characters.")

    elif re.search("^([0-9]){1,8}[.][0-9]{2}$", price) is None:
        return render_template("products/create_product.html", error="Price must be a decimal number with 2 decimal places. It must have 10 digits at most.")
    
    elif len(description) > 200:
        return render_template("products/create_product.html", error="Description must be less than 200 characters.")
    
    elif re.search("^([0-9]){1,13}$", ean) is None:
        return render_template("products/create_product.html", error="EAN must be 13 digits.")

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
                cur.execute(
                    """
                    START TRANSACTION;
                    """,
                    {},
                    )
    
                cur.execute(
                    """
                    INSERT INTO product (SKU, name, price, description, ean)
                    VALUES (%(SKU)s, %(name)s, %(price)s, %(description)s, %(ean)s);
                    """,
                    {
                        "SKU": sku,
                        "name": name,
                        "price": price,
                        "description": description,
                        "ean": ean,
                    },
                )
                log.debug(f"Inserted into product.")
    
                cur.execute(
                    """
                    COMMIT;
                    """,
                    {},
                    )
    
    return redirect(url_for("products_page"))

order_no_count = 0;
@app.route("/orders/create/<cust_no>", methods=("POST",))
def create_order(cust_no):
    global order_no_count
    
    selected_products = request.form.getlist('selected_products[]')
    quantities = request.form.getlist('quantities[]')

    for quantity in quantities:
        if int(quantity) < 0:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    customer = cur.execute(
                        """
                        SELECT *
                        FROM customer
                        WHERE cust_no = %(cust_no)s;
                        """,
                        {"cust_no": cust_no},
                    ).fetchone()

                    log.debug("Found 1 row.")

                    products = cur.execute(
                        """
                        SELECT *
                        FROM product
                        WHERE NOT sku = '-1';
                        """,
                        {},
                    ).fetchall()
                    log.debug(f"Found {cur.rowcount} rows.")

            return render_template("orders/add_order.html", error="Quantity must not be negative.", customer=customer, products=products)

    if re.search("^\d{4}-\d{2}-\d{2}$", request.form['date']) is None:
        return render_template("orders/add_order.html", error="Date must be in the format YYYY-MM-DD.")

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
                cur.execute(
                    """
                    START TRANSACTION;
                    """,
                    {},
                    )
                
                count_order = cur.execute(
                    """
                    SELECT COUNT(*) as count
                    FROM orders;
                    """
                ).fetchone()

                if order_no_count < count_order[-1]:
                    order_no_count = count_order[-1]

                cur.execute(
                    
                    """
                    INSERT INTO orders (order_no, cust_no, date)
                    VALUES (%(order_no)s, %(cust_no)s, %(date)s);
                    """,
                    {
                        "order_no": order_no_count + 1,
                        "cust_no": request.form["cust_no"],
                        "date": request.form["date"],
                    },
                )
                log.debug(f"Inserted into orders.")

                for product, quantity in zip(selected_products, quantities):
                    cur.execute(
                        """
                        INSERT INTO contains (order_no, SKU, qty)
                        VALUES (%(order_no)s, %(SKU)s, %(qty)s);
                        """,
                        {
                            "order_no": order_no_count + 1,
                            "SKU": product,
                            "qty": quantity,
                        },
                    )
                    log.debug(f"Inserted into contains.")

    
                cur.execute(
                    """
                    COMMIT;
                    """,
                    {},
                    )
    order_no_count+=1;
    return redirect(url_for("orders_index_private", cust_no=request.form["cust_no"]))


@app.route("/products/<sku>/update", methods=("GET", "POST"))
def update_product(sku):
    if request.method == "GET":
        with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                    product = cur.execute(
                        """
                        SELECT * from product WHERE SKU = %(SKU)s;
                        """,
                        {"SKU": sku},
                    ).fetchone()
                    log.debug(f"Found {cur.rowcount} rows.")

        return render_template("products/update_product.html", product=product)

    new_description = request.form["description"]
    new_price = request.form["price"]

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
                cur.execute(
                    """
                    UPDATE product
                    SET description = %(description)s,
                        price = %(price)s
                    WHERE SKU = %(SKU)s;
                    """,
                    {
                        "SKU": sku,
                        "description": new_description,
                        "price": new_price,
                    },
                )
                log.debug(f"Updated product.")
    
    return redirect(url_for("products_page"))

@app.route("/products/<sku>/delete", methods=("POST",))
def delete_product(sku):
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:

            cur.execute(
                """
                START TRANSACTION;
                """,
                {},
                )

            cur.execute(
                """
                UPDATE contains
                SET SKU = -1
                WHERE SKU = %(SKU)s;
                """,
                {"SKU": sku},
            )
            log.debug(f"Deleted from contains.")

            cur.execute(
                """
                DELETE FROM delivery
                WHERE TIN IN (
                    SELECT TIN FROM supplier WHERE SKU = %(SKU)s
                );
                """,
                {"SKU": sku},
            )
            log.debug(f"Deleted from delivery.")

            cur.execute(
                """
                DELETE FROM supplier
                WHERE SKU = %(SKU)s;
                """,
                {"SKU": sku},
            )
            log.debug(f"Deleted from supplier.")


            cur.execute(
                """
                DELETE FROM product
                WHERE SKU = %(SKU)s;
                """,
                {"SKU": sku},
            )
            log.debug(f"Deleted from product.")

            cur.execute(
                """
                COMMIT;
                """,
                {},
                )


    
    return redirect(url_for("products_page"))

@app.route("/supplier.html", methods=("GET",))
def suppliers():
    page_supplier = request.args.get("page", 1, type=int)
    per_page_supplier = 9
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            
            count_supplier = cur.execute(
                """
                SELECT COUNT(*) as count
                FROM supplier;
                """
            ).fetchone()
            
            total_pages_supplier = math.ceil(count_supplier[0] / per_page_supplier)
            offset_supplier = (page_supplier - 1) * per_page_supplier
            
            suppliers = cur.execute(
                """
                SELECT s.name, s.tin, s.address, s.date, p.name as product_name
                FROM supplier s
                JOIN product p USING (SKU)
                ORDER BY TIN ASC
                LIMIT {0} OFFSET {1};
                """.format(per_page_supplier, offset_supplier),
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")


    return render_template("supplier/index.html", suppliers=suppliers, current_page=page_supplier,
        total_pages=total_pages_supplier)

@app.route("/supplier/new", methods=("GET", "POST"))
def create_supplier():
    error = False
    if request.method == "POST":
        name = request.form["name"]
        tin = request.form["tin"]
        address = request.form["address"]
        date = request.form["date"]
        sku = request.form["sku"]

        if len(tin) > 20:
            error = "TIN must be less than 20 characters."
        
        if len(name) > 200:
            error="Name must be less than 200 characters."

        if len(address) > 255:
            error="Address must be less than 255 characters."
        
        if re.search("^\d{4}-\d{2}-\d{2}$", date) is None:
            error="Date must be in YYYY-MM-DD format."
        

        if error is False:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        INSERT INTO supplier (name, tin, address, date, SKU)
                        VALUES (%(name)s, %(tin)s, %(address)s, %(date)s, %(sku)s);
                        """,
                        {
                            "name": name,
                            "tin": tin,
                            "address": address,
                            "date": date,
                            "sku": sku,
                        },
                    )
                    log.debug(f"Inserted into supplier.")
            
            return redirect(url_for("suppliers"))

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
                products = cur.execute(
                    """
                    SELECT name, SKU from product
                    WHERE NOT SKU = '-1';
                    """,
                    {},
                ).fetchall()
                log.debug(f"Found {cur.rowcount} rows.")
        
    return render_template("supplier/create_supplier.html", products=products, error=error)

@app.route("/supplier/<tin>/delete", methods=("POST",))
def supplier_delete(tin):
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                START TRANSACTION;
                """,
                {},
                )

            cur.execute(
                """
                DELETE FROM delivery
                WHERE tin = %(tin)s;
                """,
                {"tin": tin},
            )
            log.debug(f"Deleted {cur.rowcount} from delivery.")

            cur.execute(
                """
                DELETE FROM supplier 
                WHERE tin = %(tin)s;
                """,
                {"tin": tin},
            )
            log.debug(f"Deleted {cur.rowcount} from supplier.")

            cur.execute(
                """
                COMMIT;
                """,
                {},
                )

    return redirect(url_for("suppliers"))

@app.route("/orders/pay", methods=("POST",))
def pay_order():
    order_no = request.form["order_no"]
    cust_no = request.form["cust_no"]
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                START TRANSACTION;
                """,
                {},
                )

            cur.execute(
                """
                INSERT INTO pay (order_no, cust_no)
                VALUES (%(order_no)s, %(cust_no)s);
                """,
                {"order_no": order_no, "cust_no": cust_no },
            )
            log.debug(f"Inserted {cur.rowcount} into pay.")


            cur.execute(
                """
                COMMIT;
                """,
                {},
                )

    return redirect(url_for("orders_index_private", cust_no=cust_no))

app.route("/employee_index.html", methods=("GET",))
def employees_page():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            employees = cur.execute(
                """
                SELECT ssn, TIN, bdate, name
                FROM employee
                ORDER BY ssn DESC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(employees)

    return render_template("employee/employee_index.html", employees=employees)

import math

@app.route("/customer_index.html", methods=("GET",))
def customer_index():
    """Show all the accounts, most recent first."""

    global cust_no_count
    
    page = request.args.get("page", 1, type=int)
    per_page = 9

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:

            count = cur.execute(
                """
                SELECT COUNT(*) as count
                FROM customer 
                WHERE cust_no >= 0;
                """
            ).fetchone()

            total_pages = math.ceil(count[0] / per_page)
            offset = (page - 1) * per_page

            customers = cur.execute(
                """
                SELECT cust_no, name, email, phone, address
                FROM customer
                WHERE cust_no >= 0
                ORDER BY cust_no DESC
                LIMIT {0} OFFSET {1};
                """.format(per_page, offset),
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    if cust_no_count < count[0]:
        cust_no_count = count[0]
        
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(customers)

    return render_template(
        "customer/customer_index.html",
        customers=customers,
        current_page=page,
        total_pages=total_pages,
    )

cust_no_count = 0;
@app.route("/customer/add", methods=("GET", "POST"))
def add_customer():
    global cust_no_count
    if request.method == "GET":
        return render_template("customer/add_customer.html", error=False)

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    address = request.form["address"]

    if len(name) > 80:
        return render_template("customer/add_customer.html", error="Name is too long.")
    
    if len(email) > 254:
        return render_template("customer/add_customer.html", error="Email is too long.")

    if len(phone) > 15:
        return render_template("customer/add_customer.html", error="Phone is too long.")

    if len(address) > 255:
        return render_template("customer/add_customer.html", error="Address is too long.")
    
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
                
                cur.execute(
                    """
                    START TRANSACTION;
                    """,
                    {},
                    )
    
                cur.execute(
                    """
                    INSERT INTO customer (cust_no, name, email, phone, address)
                    VALUES (%(cust_no)s, %(name)s, %(email)s, %(phone)s, %(address)s);
                    """,
                    {
                        "cust_no": cust_no_count + 1,
                        "name": request.form["name"],
                        "email": request.form["email"],
                        "phone": request.form["phone"],
                        "address": request.form["address"],
                    },
                )
                log.debug(f"Inserted new customer.")
    
                cur.execute(
                    """
                    COMMIT;
                    """,
                    {},
                    )
    cust_no_count+=1;
    return redirect(url_for("customer_index"))

@app.route("/customer/<cust_no>/delete", methods=("POST",))
def customer_delete(cust_no):
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                START TRANSACTION;
                """,
                {},
                )

            cur.execute(
                """
                UPDATE orders 
                SET cust_no = -1
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            )
            log.debug(f"Deleted {cur.rowcount}")
            
            cur.execute(
                """
                UPDATE pay 
                SET cust_no = -1
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            )
            log.debug(f"Deleted {cur.rowcount}")

            cur.execute(
                """
                DELETE FROM customer
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            )
            log.debug(f"Deleted {cur.rowcount}")

            cur.execute(
                """
                COMMIT;
                """,
                {},
                )

    return redirect(url_for("customer_index"))



def increment_counter(order, contains):
    counter = 0
    for product in contains:
        if order[0] == product[0] and product[2] > 0:
            counter += 1
    return counter




@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()