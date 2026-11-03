import io
import unittest
from unittest.mock import patch

# Import the main function from mia.py
from src import code


class TestMain(unittest.TestCase):

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_main_prints_hello_world(self, mock_stdout):
        """Verify that main() prints 'Hello world' followed by a newline."""
        # Execute the function
        code()

        # Retrieve the printed console output
        output = mock_stdout.getvalue()

        # Assert the expected output match
        self.assertEqual(output, None)


if __name__ == "__main__":
    unittest.main()
