#!/usr/bin/env python3
import re
import logging

PII_FIELDS = ("ssn", "password", "ip")
def filter_datum(fields: list, redaction: str, message: str, separator: str)-> str:
    """filter values in incoming log records
    """
    pattern = rf"({'|'.join(fields)})=.*?(?={separator}|$)"
    redaction = rf"\1={redaction}"
    redacted_message = re.sub(pattern, redaction, message)
    return redacted_message


def get_logger()-> str:
    """logger function
    """
    custom_logger = logging.getLogger("user_data")
    custom_logger.setLevel(logging.INFO)
    custom_logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter)
    custom_logger.addHandler(handler)



class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields
        

    def format(self, record: logging.LogRecord) -> str:
        logging.basicConfig(format=self.FORMAT, level=logging.INFO)
        logger = logging.getLogger(record.name)
        msg = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return logger.info(msg)




message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
formatter = RedactingFormatter(fields=("email", "ssn", "password"))
print(formatter.format(log_record))