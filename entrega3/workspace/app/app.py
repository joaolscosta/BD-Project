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

@app.route("/workplaces.html", methods=("GET",))
def workplaces():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            offices = cur.execute(
                """
                SELECT *
                FROM workplace
                JOIN office USING (address)
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

            warehouses = cur.execute(
                """
                SELECT *
                FROM Workplace
                JOIN Warehouse USING (address)
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    workplaces = []

    for office in offices:
        workplaces.append({'place': office, 'type': 'office'})
            
    for warehouse in warehouses:
        workplaces.append({'place': warehouse, 'type': 'warehouse'})

    return render_template("workplaces/index.html", workplaces=sorted(workplaces, key=lambda workplace: workplace['place'].address))

@app.route("/workplaces/<address>/delete", methods=("POST",))
def workplace_delete(address):
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                DELETE FROM workplace 
                WHERE address = %(address)s;
                """,
                {"address": address},
            )
            log.debug(f"Deleted {cur.rowcount} rows.")

    return redirect(url_for("workplaces"))

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
