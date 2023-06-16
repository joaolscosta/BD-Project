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
        return render_template("index.html", error_message=error_message)
    
    # Render the login page template for the initial GET request
    return render_template("index.html")



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
                FROM orders;
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


    page_order = request.args.get("page", 1, type=int)
    per_page_order = 9
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            
            count_order = cur.execute(
                """
                SELECT COUNT(*) as count
                FROM orders;
                """
            ).fetchone()
            
            total_pages_order = math.ceil(count_order[0] / per_page_order)
            offset_order= (page_order - 1) * per_page_order
            
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
                ORDER BY order_no
                LIMIT {0} OFFSET {1};
                """.format(per_page_order, offset_order),
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
                ORDER BY order_no
                LIMIT {0} OFFSET {1};
                """.format(per_page_order, offset_order),
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
    return render_template("orders/orders_index_private.html", increment_counter=increment_counter,orders=orders, pay=pay, customer=customer,contains=contains,current_page=page_order, total_pages=total_pages_order)


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

    
    return render_template("orders/order_payment.html", qty_list=qty_list, order=order, products=products)

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
                FROM product;
                """
            ).fetchone()    
            
            total_pages = math.ceil(count[0] / per_page)
            offset = (page - 1) * per_page
            
            products = cur.execute(
                """
                SELECT SKU, name, price, description
                FROM product
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
        return render_template("products/create_product.html")

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
                        "SKU": request.form["sku"],
                        "name": request.form["name"],
                        "price": request.form["price"],
                        "description": request.form["description"],
                        "ean": request.form["ean"],
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
@app.route("/orders/create", methods=("GET", "POST"))
def create_order():
    global order_no_count
    if request.method == "GET":
        return render_template("orders/create_order.html")
    

    
    selected_products = request.form.getlist('selected_products[]')
    quantities = request.form.getlist('quantities[]')

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
                DELETE FROM process
                WHERE order_no IN (
                    SELECT order_no FROM contains WHERE SKU = %(SKU)s
                );
                """,
                {"SKU": sku},
            )
            log.debug(f"Deleted from orders.")

            cur.execute(
                """
                DELETE FROM pay
                WHERE order_no IN (
                    SELECT order_no FROM contains WHERE SKU = %(SKU)s
                );
                """,
                {"SKU": sku},
            )
            log.debug(f"Deleted from orders.")

            cur.execute(
                """
                DELETE FROM contains
                WHERE SKU = %(SKU)s;
                """,
                {"SKU": sku},
            )
            log.debug(f"Deleted from contains.")

            cur.execute(
                """
                DELETE FROM orders
                WHERE order_no IN (
                    SELECT order_no FROM contains WHERE SKU = %(SKU)s
                );
                """,
                {"SKU": sku},
            )
            log.debug(f"Deleted from orders.")

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
    if request.method == "GET":
        with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                    products = cur.execute(
                        """
                        SELECT name, SKU from product;
                        """,
                        {},
                    ).fetchall()
                    log.debug(f"Found {cur.rowcount} rows.")
        
        return render_template("supplier/create_supplier.html", products=products)
    
    else:
        with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                cur.execute(
                    """
                    INSERT INTO supplier (name, tin, address, date, SKU)
                    VALUES (%(name)s, %(tin)s, %(address)s, %(date)s, %(sku)s);
                    """,
                    {
                        "name": request.form["name"],
                        "tin": request.form["tin"],
                        "address": request.form["address"],
                        "date": request.form["date"],
                        "sku": request.form["sku"],
                    },
                )
                log.debug(f"Inserted into supplier.")
        
        return redirect(url_for("suppliers"))
                

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

# @app.route("/accounts/<account_number>/update", methods=("GET", "POST"))
# def account_update(account_number):
#     """Update the account balance."""

#     with pool.connection() as conn:
#         with conn.cursor(row_factory=namedtuple_row) as cur:
#             account = cur.execute(
#                 """
#                 SELECT account_number, branch_name, balance
#                 FROM account
#                 WHERE account_number = %(account_number)s;
#                 """,
#                 {"account_number": account_number},
#             ).fetchone()
#             log.debug(f"Found {cur.rowcount} rows.")

#     if request.method == "POST":
#         balance = request.form["balance"]

#         error = None

#         if not balance:
#             error = "Balance is required."
#             if not balance.isnumeric():
#                 error = "Balance is required to be numeric."

#         if error is not None:
#             flash(error)
#         else:
#             with pool.connection() as conn:
#                 with conn.cursor(row_factory=namedtuple_row) as cur:
#                     cur.execute(
#                         """
#                         UPDATE account
#                         SET balance = %(balance)s
#                         WHERE account_number = %(account_number)s;
#                         """,
#                         {"account_number": account_number, "balance": balance},
#                     )
#                 conn.commit()
#             return redirect(url_for("account_index"))

#     return render_template("account/update.html", account=account)


# @app.route("/accounts/<account_number>/delete", methods=("POST",))
# def account_delete(account_number):
#     """Delete the account."""

#     with pool.connection() as conn:
#         with conn.cursor(row_factory=namedtuple_row) as cur:
#             cur.execute(
#                 """
#                 DELETE FROM account
#                 WHERE account_number = %(account_number)s;
#                 """,
#                 {"account_number": account_number},
#             )
#         conn.commit()
#     return redirect(url_for("account_index"))

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
                FROM customer;
                """
            ).fetchone()

            total_pages = math.ceil(count[0] / per_page)
            offset = (page - 1) * per_page

            customers = cur.execute(
                """
                SELECT cust_no, name, email, phone, address
                FROM customer
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
        return render_template("customer/add_customer.html")
    
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
                DELETE FROM customer
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            )
            log.debug(f"Deleted {cur.rowcount}")

            cur.execute(
                """
                DELETE FROM orders 
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            )
            log.debug(f"Deleted {cur.rowcount}")
            
            cur.execute(
                """
                DELETE FROM pay 
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