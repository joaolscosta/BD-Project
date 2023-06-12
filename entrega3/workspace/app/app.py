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


@app.route("/customer_index.html", methods=("GET",))
def customer_index():
    """Show all the accounts, most recent first."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            customers = cur.execute(
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
        return jsonify(customers)

    return render_template("customer/customer_index.html", customers=customers)

@app.route("/orders_index.html", methods=("GET",))
def orders_index():
    """Show all the accounts, most recent first."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            contains = cur.execute(
                """
                SELECT order_no, sku, qty
                FROM contains
                ORDER BY order_no ;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(contains)

    return render_template("orders/orders_index.html", contains=contains)

@app.route("/orders/<order_no>/<sku>/", methods=("GET",))
def order_detail(order_no, sku):
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            contain = cur.execute(
                """
                SELECT *
                FROM contains
                WHERE order_no = %(order_no)s;
                """,
                {"order_no": order_no},
            ).fetchone()
            log.debug(f"Found {cur.rowcount} rows.")

            order = cur.execute(
                """
                SELECT *
                FROM orders
                WHERE order_no = %(order_no)s;
                """,
                {"order_no": order_no},
            ).fetchone()

            log.debug(f"Found {cur.rowcount} rows.")

            product = cur.execute(
                """
                SELECT *
                FROM product
                WHERE SKU = %(SKU)s;
                """,
                {"SKU": sku},
            ).fetchone()
            log.debug(f"Found {cur.rowcount} rows.")
    
    return render_template("orders/order_payment.html", contain=contain, order=order, product=product)


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
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            products = cur.execute(
                """
                SELECT SKU, name, price, description
                FROM product
                ORDER BY SKU DESC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(products)

    return render_template("products/products_index.html", products=products)


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

@app.route("/products/<sku>/delete", methods=("POST",))
def delete_product(sku):
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            product = cur.execute(
                """
                DELETE FROM product
                WHERE SKU = %(SKU)s;
                """,
                {"SKU": sku},
            ).fetchone()
            log.debug(f"Deleted {cur.rowcount} rows.")
    
    return redirect(url_for("products_page"))

@app.route("/supplier.html", methods=("GET",))
def suppliers():

    
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            suppliers = cur.execute(
                """
                SELECT s.name, s.tin, s.address, s.date, p.name as product_name
                FROM supplier s
                JOIN product p USING (SKU)
                ORDER BY TIN ASC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")


    return render_template("supplier/index.html", suppliers=suppliers)

@app.route("/supplier/<tin>/delete", methods=("POST",))
def supplier_delete(tin):
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                DELETE FROM supplier 
                WHERE tin = %(tin)s;
                """,
                {"tin": tin},
            )
            log.debug(f"Deleted {cur.rowcount} rows.")

    return redirect(url_for("suppliers"))

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

app.route("/customer_index.html", methods=("GET",))
def customers_page():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            customers = cur.execute(
                """
                SELECT cust_no, name, email, phone, adress
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
        return jsonify(customers)

    return render_template("customer/customer_index.html", customers=customers)

@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()
