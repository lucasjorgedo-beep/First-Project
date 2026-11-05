"""FinanceControl: simple expense tracker using only the Python standard library."""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

DEFAULT_FILE = Path(__file__).with_name("transactions.csv")
FIELDS = ["date", "description", "category", "amount"]


@dataclass(frozen=True)
class Transaction:
    date: str
    description: str
    category: str
    amount: Decimal


def parse_amount(value: str) -> Decimal:
    """Convert a user-entered amount into a positive Decimal."""
    normalized = value.strip().replace("R$", "").replace(" ", "")
    if "," in normalized:
        normalized = normalized.replace(".", "").replace(",", ".")
    try:
        amount = Decimal(normalized)
    except InvalidOperation as exc:
        raise ValueError("Informe um valor numérico válido.") from exc
    if not amount.is_finite() or amount <= 0:
        raise ValueError("O valor precisa ser maior que zero.")
    return amount.quantize(Decimal("0.01"))


def load_transactions(file_path: Path = DEFAULT_FILE) -> list[Transaction]:
    if not file_path.exists():
        return []
    with file_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != FIELDS:
            raise ValueError("Formato do CSV inválido. Esperadas colunas: " + ", ".join(FIELDS))
        transactions = []
        for row in reader:
            transactions.append(Transaction(
                date=row["date"],
                description=row["description"],
                category=row["category"],
                amount=Decimal(row["amount"]),
            ))
        return transactions


def add_transaction(transaction: Transaction, file_path: Path = DEFAULT_FILE) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not file_path.exists() or file_path.stat().st_size == 0
    with file_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if needs_header:
            writer.writeheader()
        writer.writerow({
            "date": transaction.date,
            "description": transaction.description,
            "category": transaction.category,
            "amount": f"{transaction.amount:.2f}",
        })


def format_brl(amount: Decimal) -> str:
    return "R$ " + f"{amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def print_summary(transactions: list[Transaction]) -> None:
    total = sum((item.amount for item in transactions), Decimal("0.00"))
    print(f"\nLançamentos: {len(transactions)}")
    print(f"Total de despesas: {format_brl(total)}")
    if transactions:
        print("\nPor categoria:")
        categories: dict[str, Decimal] = {}
        for item in transactions:
            categories[item.category] = categories.get(item.category, Decimal("0.00")) + item.amount
        for category, amount in sorted(categories.items()):
            print(f"- {category}: {format_brl(amount)}")


def run_cli(file_path: Path = DEFAULT_FILE) -> None:
    while True:
        print("\n=== FinanceControl ===")
        print("1. Registrar despesa")
        print("2. Listar despesas")
        print("3. Ver resumo")
        print("0. Sair")
        option = input("Escolha: ").strip()

        if option == "1":
            description = input("Descrição: ").strip()
            category = input("Categoria: ").strip()
            raw_amount = input("Valor (ex.: 35,90): ")
            if not description or not category:
                print("Descrição e categoria são obrigatórias.")
                continue
            try:
                amount = parse_amount(raw_amount)
            except ValueError as error:
                print(error)
                continue
            add_transaction(Transaction(date.today().isoformat(), description, category, amount), file_path)
            print("Despesa registrada.")
        elif option == "2":
            items = load_transactions(file_path)
            if not items:
                print("Nenhuma despesa cadastrada.")
            for item in items:
                print(f"{item.date} | {item.description} | {item.category} | {format_brl(item.amount)}")
        elif option == "3":
            print_summary(load_transactions(file_path))
        elif option == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Controle simples de despesas pessoais.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="Caminho do arquivo CSV.")
    args = parser.parse_args()
    run_cli(args.file)


if __name__ == "__main__":
    main()
