from picture_hunt import db
from picture_hunt.models import Task

import argparse
import csv


if '__main__' == __name__:
    
    # Get Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('src', type=str, help="File to load")

    args = parser.parse_args()
    
    with open(args.src, 'r') as f:
        csv_file = csv.DictReader(f)

        for i in csv_file:
            name = i.get('name', '').strip()
            note = i.get('note').strip()
            task = Task(name=name, note=note)
            db.session.add(task)
            print(name, note)
        db.session.commit()
