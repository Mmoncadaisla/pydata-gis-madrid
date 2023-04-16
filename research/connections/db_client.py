import os

import geopandas as gpd
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine

from ..utils.utils import init_logger


class DBClient:
    NO_CURSOR_RESULTS_PATTERN = ["no", "results", "to", "fetch"]

    def __init__(self, host=None, database=None, user=None, password=None):
        self._logger = init_logger()
        self.host = host or os.environ.get("DB_HOST")
        self.database = database or os.environ.get("DB_DATABASE")
        self.user = user or os.environ.get("DB_USER")
        self.password = password or os.environ.get("DB_PASSWORD")

    @property
    def connection(self):
        conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        return conn

    @property
    def engine(self):
        return create_engine(
            "postgresql+psycopg2://"
            f"{self.user}:{self.password}@"
            f"{self.host}/{self.database}"
        )

    def _get_cursor(self):
        connection = self.connection
        return connection.cursor(cursor_factory=RealDictCursor), connection

    def run_in_transaction(self, query):
        """
        Runs a SQL query within a PosgtreSQL transaction
                Args:
                    query (str): SQL query to be executed.
                Example:
                    >>> db_client.run_in_transaction(
                        "UPDATE table_name SET column_1 = 'value'"
                        )
        """
        cursor, connection = self._get_cursor()
        cursor.execute(query)
        try:
            results = cursor.fetchall()
        except Exception as e:
            results = None
            if not all(
                msg in str(e) for msg in self.NO_CURSOR_RESULTS_PATTERN
            ):
                self._logger.warning(
                    f"Could not fetch results from cursor: {e}"
                )
        connection.commit()
        cursor.close()
        connection.close()
        return results

    @staticmethod
    def _sql_format(value):
        if isinstance(value, str):
            return "'{}'".format(value)
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        return str(value)

    def _row_values_format(self, row_values):
        return "({})".format(
            ",".join([self._sql_format(value) for value in row_values])
        )

    def read_sql(
        self, query, geom_col=None, crs="EPSG:4326", parse_dates=None
    ) -> gpd.GeoDataFrame:
        """
        Reads the output from a SQL query and returns a Geopandas GeoDataFrame
            Args:
                query (str): SQL query to be executed.
                geom_col (string): Geometry column from the output table.
                                    If None, a standard DataFrame is returned.
                                    Default: None.
                crs (string): Coordinate Reference System to use
                              for the GeoDataFrame (optional).
                              Used in combination with 'geom_col'
                              Default: 'EPSG:4326'
                parse_dates (list or dict): List of date column names.
                                Default None
            Example:
                >>> db_client.read_sql('SELECT * FROM my_table')
        """
        if geom_col:
            return gpd.GeoDataFrame.from_postgis(
                sql=query,
                con=self.engine,
                geom_col=geom_col,
                crs=crs,
                parse_dates=None
            )
        else:
            return gpd.GeoDataFrame(
                pd.read_sql(
                    sql=query,
                    con=self.engine,
                    parse_dates=parse_dates
                )
            )
