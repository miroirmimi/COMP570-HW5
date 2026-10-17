import csv
from datetime import datetime
from collections import defaultdict

input_file = "311_2024.csv"
output_file = "monthly_response.csv"

# Store total response hours and complaint counts
stats = defaultdict(lambda: [0.0, 0])

date_format = "%m/%d/%Y %I:%M:%S %p"

with open(input_file, "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        zipcode = row["Incident Zip"].strip()
        created = row["Created Date"].strip()
        closed = row["Closed Date"].strip()

        # Skip missing values
        if not zipcode or not created or not closed:
            continue

        try:
            created_date = datetime.strptime(created, date_format)
            closed_date = datetime.strptime(closed, date_format)
        except ValueError:
            continue

        # Only include incidents created in 2024
        if created_date.year != 2024:
            continue

        # Calculate response time in hours
        response_hours = (
            closed_date - created_date
        ).total_seconds() / 3600

        # Remove negative response times
        if response_hours < 0:
            continue

        # Use the closing month
        month = closed_date.strftime("%Y-%m")

        # Record ZIP code statistics
        stats[(zipcode, month)][0] += response_hours
        stats[(zipcode, month)][1] += 1

        # Record citywide statistics
        stats[("ALL", month)][0] += response_hours
        stats[("ALL", month)][1] += 1

# Save monthly averages
with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["zipcode", "month", "average_hours"])

    for (zipcode, month), (total_hours, count) in sorted(stats.items()):
        average = total_hours / count
        writer.writerow([zipcode, month, round(average, 2)])

print(f"Finished! Created {output_file}")
