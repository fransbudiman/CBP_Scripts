import argparse
import os

# This script will do all the preprocessing for the VCF file before being converted to MAF format.
# Steps:
# 1. Change the sample name from TM to SGT convention.

parser = argparse.ArgumentParser(description='Process VCF file for MAF conversion.')
parser.add_argument('--input-vcf', required=True, help='Path to the input VCF file.')
parser.add_argument('--output-dir', required=True, help='Path to the directory where processed VCF will be saved.')

args = parser.parse_args()
input_vcf = args.input_vcf
input_dir = os.path.dirname(input_vcf)
output_dir = args.output_dir

os.makedirs(output_dir, exist_ok=True)

sample_name = input_vcf.split('/')[-1].replace('.hard-filtered.vcf', '')
output_vcf = os.path.join(output_dir, f"{sample_name}.processed.vcf")
print("Sample name:", sample_name)

file_in = open(input_vcf, 'r')
file_out = open(output_vcf, 'w')

for line in file_in:
    if line.startswith('#CHROM'):
        column = line.strip().split('\t')
        column[9] = sample_name
        line = '\t'.join(column) + '\n'
    file_out.write(line)

file_in.close()
file_out.close()
