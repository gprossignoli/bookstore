from flask import Blueprint

from bookstore.cli.kafka_load_tester import KafkaLoadTester
from bookstore.cli.report_generator import ReportGenerator

cli_commands = Blueprint(name="cli", import_name="cli")


@cli_commands.cli.command("load-test")
def load_test():
    KafkaLoadTester().execute()


@cli_commands.cli.command("generate-report")
def generate_report():
    ReportGenerator().generate_report()
