from kafka3 import KafkaConsumer, KafkaProducer, TopicPartition
import json

from .exceptions import (
    KafkaHandler as KAFKA_HANDLER,
)
from clickhouse.config import ConfigBuilder


class KafkaConfig(ConfigBuilder):
    """
    The `KafkaConfig` class is a subclass of `ConfigBuilder` that defines slots for various configuration
    parameters related to a Kafka application.
    """

    __slots__ = [
        "BOOTSTRAP_SERVERS",
        "CONSUMER_GROUP",
        "CLIENT_ID",
        "USERNAME",
        "PASSWORD",
    ]

    def __init__(self, prefix: str = "KAFKA") -> None:
        super().__init__(prefix, use_prefix=True)


class KafkaService:
    def __init__(self, config: KafkaConfig = None):
        if config is None:
            config = KafkaConfig()
        self.config = config
        self.consumer = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    @KAFKA_HANDLER.catch
    def check_connection(self):
        self.list_all_topics()

    @KAFKA_HANDLER.catch
    def connect(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers=self.config.BOOTSTRAP_SERVERS,
            value_deserializer=lambda x: x.decode("utf-8"),
            group_id=self.config.CONSUMER_GROUP,
            client_id=self.config.CLIENT_ID,
            security_protocol="PLAINTEXT",
        )

    @KAFKA_HANDLER.catch
    def disconnect(self):
        self.consumer.close()

    @KAFKA_HANDLER.catch
    def list_all_topics(self) -> list[str]:
        topics = self.consumer.topics()
        topic_list = list(topics)
        for topic in topic_list:
            print(f"Topic: {topic}")
        return list(topics)

    @KAFKA_HANDLER.catch
    def send_message_to_topic(self, topic_name, message):
        producer = KafkaProducer(
            bootstrap_servers=self.config.BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        producer.send(topic_name, message)
        producer.flush()
        producer.close()

    @KAFKA_HANDLER.catch
    def assign_topics(self, topics: list):
        topic_partitions = [
            TopicPartition(topic=topic, partition=0) for topic in topics
        ]
        self.consumer.assign(topic_partitions)

    @KAFKA_HANDLER.catch
    def consume_data(self):
        for msg in self.consumer:
            print("Topic Name=%s,Message=%s" % (msg.topic, msg.value))
            yield msg
