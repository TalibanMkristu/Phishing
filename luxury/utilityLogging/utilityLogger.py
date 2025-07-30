import os, logging
from datetime import datetime


def setupLogger(log_level=logging.DEBUG, log_file=None):
    """Creating logger"""
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    
    if logger.handlers:
        """Prevents returning handlers multiple times"""
        return logger
    """Desired log formatting"""
    formatter = logging.Formatter(
        "[ [%(asctime)s] [%(name)s] %(levelname)s >> %(message)s ]",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    """Creating console handler"""
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    """File handler if specified in log_file else defaulting to None"""
    if log_file:
        """Create a directory if None for logs"""
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def main():
    logger =setupLogger()
    logger.info("Started running logger")
if __name__  == '__main__':
    main()
    