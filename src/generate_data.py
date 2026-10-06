from pathlib import Path
import csv
import json
import random
from faker import Faker


fake = Faker()
Faker.seed(42)
random.seed(42)


OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)


CUSTOMER_COUNT = 1000
ACCOUNT_COUNT = 2000
MERCHANT_COUNT = 100
TRANSACTION_COUNT = 100000


def generate_customers():
    customers = []

    for customer_id in range(1, CUSTOMER_COUNT + 1):
        customers.append({
            "customer_id": customer_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "created_at": fake.date_time_between(
                start_date="-5y",
                end_date="now"
            )
        })

    return customers


def generate_accounts():
    accounts = []

    for account_id in range(1, ACCOUNT_COUNT + 1):
        accounts.append({
            "account_id": account_id,
            "customer_id": random.randint(1, CUSTOMER_COUNT),
            "account_type": random.choice([
                "Checking",
                "Savings",
                "Credit"
            ]),
            "status": random.choice([
                "Active",
                "Active",
                "Active",
                "Closed"
            ]),
            "opened_date": fake.date_between(
                start_date="-10y",
                end_date="today"
            )
        })

    return accounts


def generate_merchants():
    merchants = []

    categories = [
        "Groceries",
        "Dining",
        "Gas",
        "Utilities",
        "Shopping",
        "Entertainment",
        "Travel"
    ]

    for merchant_id in range(1, MERCHANT_COUNT + 1):
        merchants.append({
            "merchant_id": merchant_id,
            "merchant_name": fake.company(),
            "merchant_category": random.choice(categories)
        })

    return merchants


def generate_transactions():
    transactions = []

    transaction_types = [
        "Purchase",
        "Deposit",
        "Withdrawal",
        "Payment"
    ]

    channels = [
        "Online",
        "Mobile",
        "Branch"
    ]

    for transaction_id in range(1, TRANSACTION_COUNT + 1):
        transaction_type = random.choice(transaction_types)

        if transaction_type == "Deposit":
            amount = round(random.uniform(100, 5000), 2)
        else:
            amount = round(random.uniform(-500, -1), 2)

        metadata = {
            "channel": random.choice(channels),
            "fraud_review": random.random() < 0.05
        }

        transactions.append({
            "transaction_id": transaction_id,
            "account_id": random.randint(1, ACCOUNT_COUNT),
            "merchant_id": random.randint(1, MERCHANT_COUNT),
            "transaction_date": fake.date_time_between(
                start_date="-2y",
                end_date="now"
            ),
            "amount": amount,
            "transaction_type": transaction_type,
            "description": fake.sentence(nb_words=4),
            "metadata": json.dumps(metadata)
        })

    return transactions


def write_csv(filename, rows):
    if not rows:
        return

    file_path = OUTPUT_DIR / filename

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)


customers = generate_customers()
accounts = generate_accounts()
merchants = generate_merchants()
transactions = generate_transactions()

write_csv("customers.csv", customers)
write_csv("accounts.csv", accounts)
write_csv("merchants.csv", merchants)
write_csv("transactions.csv", transactions)

print("Data generation complete.")