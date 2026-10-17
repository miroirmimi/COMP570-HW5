import argparse
import csv
from datetime import datetime

# Create the command-line argument parser
parser = argparse.ArgumentParser(
    description="Count complaint types by borough within a date range."
)

# Define command-line arguments
parser.add_argument("-i", required=True, help="Input CSV file")
parser.add_argument("-s", required=True, help="Start date (YYYY-MM-DD)")
parser.add_argument("-e", required=True, help="End date (YYYY-MM-DD)")
parser.add_argument("-o", required=False, help="Output CSV file")

args = parser.parse_args()

# Convert user input dates
start_date = datetime.strptime(args.s, "%Y-%m-%d").date()
end_date = datetime.strptime(args.e, "%Y-%m-%d").date()

# Dictionary for counting complaints
counts = {}

# Read the CSV file
with open(args.i, "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        # Convert complaint creation date
        created_date = datetime.strptime(
            row["Created Date"], "%m/%d/%Y %I:%M:%S %p"
        ).date()

        # Check whether the date is within the specified range
        if start_date <= created_date <= end_date:
            borough = row["Borough"]
            complaint_type = row["Complaint Type"]

            # Use borough and complaint type as dictionary key
            key = (borough, complaint_type)

            # Increase the count by 1
            counts[key] = counts.get(key, 0) + 1
import sys

# Decide where to write the results
if args.o:
    output = open(args.o, "w", encoding="utf-8", newline="")
else:
    output = sys.stdout

# Write results in CSV format
writer = csv.writer(output)
writer.writerow(["complaint type", "borough", "count"])

for (borough, complaint_type), count in sorted(counts.items()):
    writer.writerow([complaint_type, borough, count])

# Close the output file if one was created
if args.o:
    output.close()
