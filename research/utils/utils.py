import logging
from functools import wraps


def init_logger() -> logging.RootLogger:
    """Initialize logger object.

    Returns:
        logging.RootLogger: Logger object
    """
    logging.basicConfig(
        level="INFO",
        format=" %(asctime)s - %(levelname)s - %(message)s",
        datefmt="%I:%M:%S %p",
    )
    logger = logging.getLogger()
    return logger


def safe_run(func):
    """Decorator to catch exceptions and log them.

    Args:
        func (function): Function to be wrapped

    Returns:
        function: Wrapped function
    """
    @wraps(func)
    def new_func(self, *args, **kwargs):
        logger = init_logger()
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            logger.error(f"Some error occurred running {func.__name__}: {e}")

    return new_func


def wrap_materialize_table_sql(
    table_name: str,
    sql_query: str,
    replace: bool = True
) -> str:
    drop_sql = f'DROP TABLE IF EXISTS {table_name};' if replace is True else ''
    create_sql = f"""
            {drop_sql}
            CREATE TABLE {table_name} AS
            ({sql_query})
        """
    return create_sql
