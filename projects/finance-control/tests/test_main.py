import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from main import (
    Transaction,
    add_transaction,
    format_brl,
    load_transactions,
    parse_amount,
    print_summary,
)


class FinanceControlTests(unittest.TestCase):
    def test_parse_brazilian_amount(self):
        self.assertEqual(parse_amount("1.234,56"), Decimal("1234.56"))

    def test_reject_zero_and_invalid_amount(self):
        for value in ("0", "-5", "abc"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_amount(value)

    def test_save_and_load_transaction(self):
        with tempfile.TemporaryDirectory() as folder:
            csv_path = Path(folder) / "data.csv"
            item = Transaction("2026-11-05", "Mercado", "Alimentação", Decimal("42.90"))
            add_transaction(item, csv_path)
            self.assertEqual(load_transactions(csv_path), [item])

    def test_brl_format(self):
        self.assertEqual(format_brl(Decimal("1234.5")), "R$ 1.234,50")


if __name__ == "__main__":
    unittest.main()
