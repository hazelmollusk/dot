import logging

class ColorFormatter(logging.Formatter):

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    indigo = "\x1b[34;20m"
    green = "\x1b[1;32;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_base = "%(asctime)s - %(levelname)s - %(message)s"
    format_suffix = " (%(filename)s:%(lineno)d)"

    msg_data = format_base + reset + grey + format_suffix + reset
    FORMATS = {
        logging.DEBUG: indigo + msg_data,
        logging.INFO: green + msg_data,
        logging.WARNING: yellow + msg_data,
        logging.ERROR: red + msg_data,
        logging.CRITICAL: bold_red + msg_data
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
