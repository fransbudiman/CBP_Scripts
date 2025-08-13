# After generating multiple MAFs, this script will merge all MAF in a directory into a single study MAF.
# Feature: 
# 1. Check if columns are consistent across all MAF files
# 2. Check if tumor sample barcode is unique before merging. Fail if not.

import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(description='Merge MAF files.')
parser.add_argument('--input-dir', required=True, help='Path to the directory containing MAF files.')
parser.add_argument('--output-file', required=True, help='Path to the output merged MAF file.')

args = parser.parse_args()
input_dir = args.input_dir
output_file = args.output_file
output_dir = os.path.dirname(output_file)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

input_files = [f for f in os.listdir(input_dir) if f.endswith('.maf')]
first_file = input_files[0]

reader = open(os.path.join(input_dir, first_file), 'r')

metadata_lines = []

# Read and store the metadata for later
for line in reader:
    if line.startswith('#'):
        metadata_lines.append(line)
    else:
        break

reader.close()

# Set empty dataframe for merged data. Set the columns to the first file's columns
merged_df = pd.DataFrame()
first_df = pd.read_csv(os.path.join(input_dir, first_file), sep='\t', comment='#')
merged_df_columns = first_df.columns

for file in input_files:
    df = pd.read_csv(os.path.join(input_dir, file), sep='\t', comment='#')

    # Check if columns are consistent
    if not df.columns.equals(merged_df_columns):
        raise ValueError(f'Inconsistent columns in file: {file}')

    # Check if tumor sample barcode is unique
    elif df['Tumor_Sample_Barcode'].isin(merged_df['Tumor_Sample_Barcode'].values).any():
        raise ValueError(f'Tumor sample barcode is not unique in file: {file}')
    
    else:
        merged_df = pd.concat([merged_df, df], ignore_index=True)

# Write metadata to output file
with open(output_file, 'w') as f:
    f.writelines(metadata_lines)
    merged_df.to_csv(f, sep='\t', index=False)

