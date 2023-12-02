from .config import ConfigBuilder
from pydantic import BaseModel
from enum import Enum


class ClickhouseConfig(ConfigBuilder):

    __slots__ = [
        "HOST",
        "PORT",
        "SSL",
        "USERNAME",
        "PASSWORD",
        "DATABASE"
    ]

    def __init__(self, prefix: str = "CLICKHOUSE", use_prefix: bool = True) -> None:
        super().__init__(prefix, use_prefix)
    
    def get_jdbc_url(self):
        """
        The function `get_jdbc_url` returns a JDBC URL based on the values of config properties.
        :return: a JDBC URL string.
        """
        proto = "jdbc:cd:"
        if ( self.SSL.lower() == "true"):
            proto += "https:"
        return f"{proto}//{self.HOST}:{self.PORT}"

class DATA_TYPES(Enum):
    INT_8 = "Int8"
    INT_16 = "Int16"
    INT_32 = "Int32"
    INT_64 = "Int64"
    UINT_8 = "UInt8"
    UINT_16 = "UInt16"
    UINT_32 = "UInt32"
    UINT_64 = "UInt64"
    FLOAT = "Float32"
    FLOAT_64 = "Float64"
    STRING = "String"
    DATE = "Date"
    DATE_32 = "Date32"
    DATE_TIME = "DateTime"
    DATE_TIME_64 = "DateTime64"
    JSON = "JSON"
    UUID = "UUID"

class ENGINE(Enum):
    MERGE_TREE = "MergeTree"
    REPLICATED_MERGE_TREE = "ReplicatedMergeTree"
    REPLACING_MERGE_TREE = "ReplacingMergeTree"
    REPLICATED_REPLACING_MERGE_TREE = "ReplicatedReplacingMergeTree"
    DISTRIBUTED = "Distributed"


class TableConfig(BaseModel):
    table_engine: ENGINE
    args: dict[str, str]

class ClickhouseTableColumn(BaseModel):
    name: str
    data_type: Enum
    array: bool
    nullable: bool
    primary_key: bool
    order_key: bool

class ClickhouseTable(BaseModel):
    database_name: str
    table_name: str
    table_config: TableConfig
    columns: list[ClickhouseTableColumn]