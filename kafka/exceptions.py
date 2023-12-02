import functools
import time
import asyncio
import inspect

from enum import Enum

from kafka3 import errors as KAFKA_ERROR

from clickhouse.exceptions import ServiceException
from clickhouse.exceptions import KAFKA as ERROR_CONSTANTS
from clickhouse.decorator import LoggingDecorators
import logging


class BackoffPolicy(Enum):
    LINEAR = "linear"
    EXPONENTIAL = "exponential"

class BackoffState():

    initial_timestamp: int
    last_attempt_timestamp: int
    backoff_policy: BackoffPolicy
    backoff_time: int
    max_retries: int
    max_time: int
    exponential_factor: float
    attempts: int = 0
    
    def __init__(self, backoff_policy: BackoffPolicy = BackoffPolicy.EXPONENTIAL,
                 max_retries: int = 10, max_time:int =  600, backoff_time: int = 5,
                 exponential_factor: float = 1.5) -> None:
        self.backoff_policy = backoff_policy
        self.max_retries = max_retries
        self.backoff_time = backoff_time
        self.exponential_factor = exponential_factor
        self.max_time = max_time
        self.attempts = 1
        self.initial_timestamp = time.time()
    
    async def retry(self, func: callable, *args, **kwargs):
        sleep_time = 0
        if self.backoff_policy == BackoffPolicy.LINEAR:
            sleep_time = self.backoff_time
        else:
            sleep_time = int(self.backoff_time * pow(self.exponential_factor, self.attempts))
        logging.warn(f"Caught exception. Since backoff is configured, retry after {sleep_time} seconds.")
        self.attempts += 1
        await asyncio.sleep(sleep_time)
        if inspect.iscoroutinefunction(func):
            return asyncio.run(func(*args, **kwargs))
        else:
            return func(*args, **kwargs)

    def can_retry(self) -> bool:
        if self.attempts < self.max_retries:
            return True
        if self.max_time > time.time() - self.initial_timestamp:
            return True
        return False

class KafkaHandler:
    @classmethod
    def catch(cls, func: callable):
        @LoggingDecorators.functional
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if inspect.iscoroutinefunction(func):
                    return asyncio.run(func(*args, **kwargs))
                else:
                    return func(*args, **kwargs)
            except (
                KAFKA_ERROR.AuthenticationMethodNotSupported,
                KAFKA_ERROR.AuthenticationFailedError,
            ) as e:
                raise ServiceException("KafkaService", ERROR_CONSTANTS.AUTH_FAILED, e)
            except KAFKA_ERROR.OffsetOutOfRangeError as e:
                raise ServiceException(
                    "KafkaService", ERROR_CONSTANTS.OFFSET_OUT_OF_RANGE, e
                )
            except KAFKA_ERROR.MessageSizeTooLargeError as e:
                raise ServiceException("KafkaService", ERROR_CONSTANTS.MSG_TOO_LARGE, e)
            except KAFKA_ERROR.KafkaError as e:
                if e.retriable:
                    backoff_state = BackoffState()
                    while backoff_state.can_retry():
                        try:
                            ret_val = asyncio.run(backoff_state.retry(func, *args, **kwargs))
                            return ret_val
                        except Exception as e:
                            pass
                    raise ServiceException(
                        "KafkaService", ERROR_CONSTANTS.BACKOFF_ERROR, e
                    )
                raise ServiceException("KafkaService", ERROR_CONSTANTS.GENERIC, e)
            except Exception as e:
                raise ServiceException("KafkaService", ERROR_CONSTANTS.GENERIC, e)

        return wrapper