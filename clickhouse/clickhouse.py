import clickhouse_connect
from clickhouse_connect.driver.exceptions import (
    DataError,
    DatabaseError,
    ClickHouseError,
    ProgrammingError,
    InternalError,
)
from .models import ClickhouseConfig, ClickhouseTable
from .exceptions import ServiceException
from .exceptions import MESSAGES as ERROR_CONSTANTS
from .decorator import LoggingDecorators
from typing import Any


class ClickhouseService:
    def __init__(self, connection_details: ClickhouseConfig = ClickhouseConfig()):
        self.connection_details = connection_details
        self.client = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
        try:
            self.client = clickhouse_connect.get_client(
                host=self.connection_details.HOST,
                port=self.connection_details.PORT,
                user=self.connection_details.USERNAME,
                password=self.connection_details.PASSWORD,
                secure=self.connection_details.SSL
            )
        except Exception as e:
            raise ServiceException(
                "ClickHouseService",
                ERROR_CONSTANTS.SERVICES.CLICKHOUSE.CONNECTION_ERROR,
                e,
            )
        self.check_connection()

    def disconnect(self):
        if self.client:
            self.client.close()

    def check_connection(self):
        try:
            self.execute_command("SELECT 1")
        except ServiceException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                "ClickHouseService",
                ERROR_CONSTANTS.SERVICES.CLICKHOUSE.CONNECTION_ERROR,
                e,
            )

    @LoggingDecorators.functional
    def list_databases(self) -> list[str]:
        try:
            query = "SHOW DATABASES;"
            result = self.execute_command(query)
            result = result.split("\n")
            return result
        except ServiceException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                "ClickHouseService", ERROR_CONSTANTS.SERVICES.CLICKHOUSE.QUERY_ERROR, e
            )

    ## TODO: Create table in clickhouse
    def create_table(self, table_details: ClickhouseTable):
        pass

    def list_tables(self, database: str) -> list[str]:
        try:
            query = f"SHOW TABLES FROM {database}"
            result = self.execute_command(query)
            result = result.split("\n")
            return result
        except ServiceException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                "ClickHouseService", ERROR_CONSTANTS.SERVICES.CLICKHOUSE.QUERY_ERROR, e
            )
    
    def query_values(self, data: Any):
        if isinstance(data, dict):
            return str(data)
        elif isinstance(data, list):
            return str(data)
        else:
            return f"'{str(data)}'"
    
    def insert_values(self, database: str, table_name: str, data: dict[str, Any]):
        column_keys = f"({', '.join([key for key in data])})"
        column_values = f"({', '.join([self.query_values(data[key]) for key in data])})"
        query = f"INSERT INTO {database}.{table_name} {column_keys} VALUES {column_values};"
        self.execute_command(query)

    def get_data_by_fields(self, database: str, table_name: str, data: dict[str, Any]):
        
        query = f"SELECT * FROM {database}.{table_name} WHERE "

        condition_list = []
        for key in data:
            value  = data[key]
            if isinstance(value, str):  
                formatted_value = f"'{value}'" 
            else:
                formatted_value = str(value)  
            condition_list.append(f"{key} = {formatted_value}")

        query += " AND ".join(condition_list) + ";"

        # Use SQLAlchemy to fetch results
        return self.execute_command(query)

    # @LoggingDecorators.functional
    def execute_command(self, script: str):
        try:
            return self.client.command(script)

        except DataError as ex:
            raise ServiceException(
                "ClickHouseService",
                ERROR_CONSTANTS.SERVICES.CLICKHOUSE.DATA_ERROR,
                ex,
            )
        except ProgrammingError as ex:
            raise ServiceException(
                "ClickHouseService",
                ERROR_CONSTANTS.SERVICES.CLICKHOUSE.PROGRAMMING_ERROR,
                ex,
            )
        except InternalError as ex:
            raise ServiceException(
                "ClickHouseService",
                ERROR_CONSTANTS.SERVICES.CLICKHOUSE.DATABASE_ERROR,
                ex,
            )
        except DatabaseError as ex:
            raise ServiceException(
                "ClickHouseService",
                ERROR_CONSTANTS.SERVICES.CLICKHOUSE.DATABASE_ERROR,
                ex,
            )
        except ClickHouseError as ex:
            raise ServiceException(
                "ClickHouseService",
                ERROR_CONSTANTS.SERVICES.CLICKHOUSE.CLICKHOUSE_ERROR,
                ex,
            )
        except Exception as ex:
            raise ServiceException(
                "ClickHouseService",
                ERROR_CONSTANTS.SERVICES.CLICKHOUSE.QUERY_ERROR,
                ex,
            )
