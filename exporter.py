import csv
from datetime import date

def save_to_file(properties):
    today = date.today()
    file = open(f"export/{today}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["Image", "Suburb", "Address", "Price", "Size", "Type", "Link", "Image Link"])

    for property in properties:
        writer.writerow(list(property.values()))

    return