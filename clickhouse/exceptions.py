class ServiceException(Exception):
    def __init__(self, service_name: str,error_code: int, error_message: str, e: Exception = None, *args:object):
        self.service_name = service_name
        self.error_message = error_message
        self.error_code = error_code
        super().__init__(e, *args)

    def __str__(self):
        return f"Service Failure: {self.service_name} Message: {self.error_message} Code: {self.error_code}"

class KAFKA:
    GENERIC = "Kafka operation failed"
    BACKOFF_ERROR = "Unable to communicate with service even after multiple retries"
    CONNECTION_ERROR = "Failed to connect to the Kafka cluster"
    CONNECTION_TIMEOUT = "Timeout error ,failed to connect to Kafka Cluster"
    TOPIC_ALREADY_EXISTS = "Failed as Topic Already Exists"
    DELETE_TOPIC_TIMEOUT = "Timeout Error , could not delete Topic "
    UNKNOWN_TOPIC_PARTITION = "Failed as topic or partition is not known"
    INVALID_TOPIC = "Failed as Topic is invalid"
    AUTH_FAILED = "Kafka server authentication failed"
    OFFSET_OUT_OF_RANGE = "Kafka offset out of range"
    MSG_TOO_LARGE = "Kafka message size too large"
    RETRY_BACKOFF = "Failed after retrying multiple times"


class AUTH:
    UNAUTHENTICATED = "Invalid authentication provided."
    FORBIDDEN = (
        "User does not have required permissions to access the requested resource."
    )
    INVALID_TOKEN = "Authentication provided is not invalid."


class CLICKHOUSE:
    CONNECTION_ERROR = "Failed to connect to the Clickhouse cluster"
    QUERY_ERROR = "Unable to fetch data for this query"
    CLICKHOUSE_ERROR = "Exception related to operation with ClickHouse"
    DATABASE_ERROR = "Exception raised for errors that are related to the database"
    DATA_ERROR = (
        "Exception raised for errors that are due to problems with the processed data"
    )
    PROGRAMMING_ERROR = "Exception raised for Sql Syntax or Programming"

class POSTGRES:
    CONNECTION_ERROR = "Failed to connect to the Postgres cluster"
    QUERY_ERROR = "Unable to fetch data for this query"

class REDIS:
    CONNECTION_ERROR = "Failed to connect to the Redis cluster"
    SET_ERROR = "Failed to set the key to Redis cluster"
    GET_ERROR = "Unable to fetch the data with specified key from Redis"
    DELETE_ERROR = "Failed to delete the key to Redis cluster"
    


class FLINK:
    CONNECTION_ERROR = "Failed to connect to the Flink cluster"


class BUGSNAG:
    CONFIGURE_ERROR = "Failed to configure Bugsnag"
    LOGGING_ERROR = "Failed to setup logging in Bugsnag"


class SERVICES:
    SERVICE_NOT_IMPLEMENTED = "This service is not yet available"
    KAFKA = KAFKA()
    CLICKHOUSE = CLICKHOUSE()
    BUGSNAG = BUGSNAG()
    AUTH = AUTH()
    FLINK= FLINK()
    REDIS= REDIS()
    POSTGRES= POSTGRES()

class INTERNAL:
    CODE = "Something went wrong,Please check your code"


class MESSAGES:
    SERVICES = SERVICES()
    AUTH = AUTH()