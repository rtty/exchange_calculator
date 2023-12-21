import argparse
import csv
import logging
from datetime import datetime

from sqlalchemy.orm import Session
from tqdm import tqdm

from config import SessionLocal, engine
from db import models
from db.models import Rate, Currency
from services.currencies_service import get_currency_by_code, create_currency


def get_or_create_currency(code: str, db: Session) -> Currency:
    return get_currency_by_code(code, db) or create_currency(code, db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', required=True, help='The input file')
    args = parser.parse_args()
    logging.disable(logging.INFO)

    try:
        print(f'Populate initial data from {args.input_file}')
        # create tables
        models.Base.metadata.create_all(bind=engine)

        with SessionLocal() as db, open(args.input_file) as f:
            reader = csv.reader(f)

            header = True
            batch_rates = []
            for row in tqdm(reader):
                if header:
                    header = False
                    # load all currency pairs
                    pairs = [[code for code in pair.split('/')] for pair in row[1:]]
                    continue

                # parse date and rates
                date, *rates = row
                date = datetime.strptime(date, '%Y-%m-%d').date()
                rates = [float(x) for x in rates]

                for i, currency in enumerate(rates):
                    # check if base currency exists
                    currency_base = get_or_create_currency(pairs[i][0], db)
                    # check if target currency exists
                    currency_target = get_or_create_currency(pairs[i][1], db)
                    # store rate
                    batch_rates.append(
                        Rate(
                            date=date,
                            currency_base_id=currency_base.id,
                            currency_target_id=currency_target.id,
                            rate=rates[i],
                        )
                    )

            db.add_all(batch_rates)
            db.commit()
    except Exception as e:
        print(f'An error occurred: {e}')
