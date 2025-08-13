# This script takes in a csv file with that contains the data from each clinical sample.
# The minimum required columns are: PATIENT_ID, SAMPLE_ID, CANCER_TYPE, CANCER_TYPE_DETAILED, ONCOTREE_CODE

import argparse
import os
import pandas as pd

parser = argparse.ArgumentParser(description='Generate clinical data files for CBioPortal.')
parser.add_argument('--input-csv', required=True, help='Path to the input CSV file')
parser.add_argument('--project-dir', required=True, help='Path to the project directory')

args = parser.parse_args()
input_csv = args.input_csv
project_dir = args.project_dir

output_file_path = os.path.join(project_dir, "data_clinical_sample.txt")
df = pd.read_csv(input_csv, sep="\t")

# Write required header to output file
with open(output_file_path, "w") as f:
    f.write("#Patient Identifier\tSample Identifier\tCancer Type\tCancer Type Detailed\tOncotree Code\n")
    f.write("#Identifier to uniquely specify a patient.\tA unique sample identifier.\tCancer type.\tCancer type detailed.\tOncotree code.\n")
    f.write("#STRING\tSTRING\tSTRING\tSTRING\tSTRING\n")
    f.write("#1\t1\t1\t1\t1\n")


# Check if all required columns are present
required_columns = ["PATIENT_ID", "SAMPLE_ID", "CANCER_TYPE", "CANCER_TYPE_DETAILED", "ONCOTREE_CODE"]
if not all(col in df.columns for col in required_columns):
    print(df.columns)
    raise ValueError(f"Input CSV must contain the following columns: {required_columns}")
    
# Write the output file
df.to_csv(output_file_path, sep="\t", index=False)
print(f"Clinical data file created at: {output_file_path}")

