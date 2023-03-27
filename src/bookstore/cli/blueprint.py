import click
from flask import Blueprint

from bookstore.cli.kafka_load_tester import KafkaLoadTester
from bookstore.cli.report_generator import ReportGenerator
from bookstore.infrastructure.event_buses import KafkaEventBusProducerFactory
from bookstore.infrastructure.event_buses.transactional_outbox.message_relay import (
    MessageRelay,
)
from bookstore.infrastructure.event_buses.transactional_outbox.sqlalchemy_transactional_outbox_repository_with_autocommit import (
    SqlalchemyTransactionalOutboxRepositoryWithAutocommit,
)
from bookstore.settings import logger, db

cli_commands = Blueprint(name="cli", import_name="cli")


@cli_commands.cli.command("load-test")
def load_test():
    KafkaLoadTester().execute()


@cli_commands.cli.command("generate-report")
def generate_report():
    ReportGenerator().generate_report()


@cli_commands.cli.command("launch_kafka_publications")
@click.argument("iterations")
def launch_kafka_publications(iterations):
    for i in range(iterations):
        KafkaLoadTester().execute()
        transactional_outbox_worker()
        ReportGenerator().generate_report()

    logger.info(f"Experiments completed: {iterations}")


@cli_commands.cli.command("transactional-outbox-worker")
def transactional_outbox_worker():
    logger.info("Starting transactional outbox worker")
    while True:
        try:
            MessageRelay(
                logger=logger,
                outbox_repository=SqlalchemyTransactionalOutboxRepositoryWithAutocommit(
                    db_session=db.session
                ),
                event_bus_producer=KafkaEventBusProducerFactory().build(),
            ).start()
        except Exception as e:
            logger.exception(f"MessageRelay suffered an error: {e}")
            logger.info("Resetting the execution of the MessageRelay")
