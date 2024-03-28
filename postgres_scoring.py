#!/usr/bin/env python3
import psycopg2


class PostgreSQLCheck:
    def __init__(self, host, port, dbname, username, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.username = username
        self.password = password
        self.result = Result()

    def check_db_read(self, cur):
        try:
            cur.execute("SELECT * FROM purchases;")
            cur.execute("SELECT * FROM receipts;")
            self.result.success(feedback="PostgreSQL scoring user can read data")
        except psycopg2.Error as e:
            self.result.warn(feedback="PostgreSQL scoring user cannot read data", details={
                "error": str(e)
            })

    def check_db_write(self, cur, conn):
        try:
            cur.execute("INSERT INTO receipts(username, date, total) VALUES (%s, NOW(), %s) RETURNING id",
                        ("testuser", "50.00"))
            receipt_id = cur.fetchone()[0]
            cur.execute("INSERT INTO purchases(receipt_id, item_id, quantity) VALUES (%s, %s, %s)",
                        (receipt_id, 1, 1))
            conn.commit()
            self.result.success(feedback="PostgreSQL scoring user can write data")
        except psycopg2.Error as e:
            self.result.warn(feedback="PostgreSQL scoring user cannot write data", details={
                "error": str(e)
            })

    def execute(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.username,
                password=self.password
            )
            cur = conn.cursor()
            self.result.success(feedback="PostgreSQL scoring user can connect and authenticate")

            self.check_db_read(cur)
            self.check_db_write(cur, conn)

            cur.close()
            conn.close()
        except psycopg2.OperationalError as e:
            if "password authentication failed" in str(e):
                self.result.warn(feedback="PostgreSQL scoring user authentication failed", details={
                    "error": str(e)
                })
            else:
                self.result.fail(feedback="PostgreSQL is inaccessible", details={
                    "error": str(e)
                })
        except psycopg2.Error as e:
            self.result.fail(feedback="An error occurred while connecting to PostgreSQL", details={
                "error": str(e)
            })


class Result:
    def __init__(self):
        self.status = "unknown"
        self.feedback = ""

    def fail(self, feedback, details=None):
        self.status = "fail"
        self.feedback = feedback
        print(f"FAIL: {feedback}")
        if details:
            print(f"Details: {details}")

    def warn(self, feedback, details=None):
        self.status = "warn"
        self.feedback = feedback
        print(f"WARN: {feedback}")
        if details:
            print(f"Details: {details}")

    def success(self, feedback):
        self.status = "success"
        self.feedback = feedback
        print(f"SUCCESS: {feedback}")


if __name__ == '__main__':
    postgresql_host = "192.168.1.7"
    postgresql_port = 5432
    postgresql_dbname = "db"
    postgresql_username = "postgres"
    postgresql_password = "S3cr3tDBP@ss!"

    check = PostgreSQLCheck(
        host=postgresql_host,
        port=postgresql_port,
        dbname=postgresql_dbname,
        username=postgresql_username,
        password=postgresql_password
    )
    check.execute()
