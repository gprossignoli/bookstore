from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock

from src.application import CommandExecutor
from src.application import CommandHandler


class TestCommandExecutor(TestCase):
	def setUp(self):
		self.command_executor = CommandExecutor()

	def test_execute(self):
		command = Mock()
		command.fqn.return_value = "command.example"
		command_handler = Mock(spec=CommandHandler)
		command_handler.execute = Mock()

		with patch.object(self.command_executor, "_CommandExecutor__mapper", new_callable=PropertyMock) as mapper_mock:
			mapper_mock.return_value = {"command.example", command_handler.execute}
			mapper_mock.get.return_value = command_handler.execute

			self.command_executor.execute(command)

		command_handler.execute.assert_called_with(command)
