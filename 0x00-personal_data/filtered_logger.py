#!/usr/bin/env python3
"""data filtered logger modules
"""

from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ filter values in incoming log records
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filter incoming log record with the filter_datum """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """ return logger object """
    custom_logger = logging.getLogger("user_data")
    custom_logger.setLevel(logging.INFO)
    custom_logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    custom_logger.addHandler(handler)
    return custom_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to the database """
    PERSONAL_DATA_DB_USERNAME = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    PERSONAL_DATA_DB_PASSWORD = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    PERSONAL_DATA_DB_HOST = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    PERSONAL_DATA_DB_NAME = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connection.MySQLConnection(
            host=PERSONAL_DATA_DB_HOST,
            user=PERSONAL_DATA_DB_USERNAME,
            password=PERSONAL_DATA_DB_PASSWORD,
            database=PERSONAL_DATA_DB_NAME
            )
    return connection


def main() -> None:
    """ main function with the implementation
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    field_names = [i[0] for i in cursor.description]

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
