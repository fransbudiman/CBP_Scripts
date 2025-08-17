import argparse
import os

parser = argparse.ArgumentParser(description='Process VCF file for MAF conversion.')
parser.add_argument('--project-dir', required=True, help='Path to the project directory')
parser.add_argument('--sample-csv', required=True, help='Path to the sample CSV file')
parser.add_argument('--study-identifier', required=True, help='Study identifier')
parser.add_argument('--name', required=True, help='Name of the study')
parser.add_argument('--description', required=True, help='Description of the study')

args = parser.parse_args()
project_dir = args.project_dir
sample_csv = args.sample_csv
study_identifier = args.study_identifier
name = args.name
description = args.description

if not os.path.exists(project_dir):
    os.makedirs(project_dir)

# first create the meta_study.txt file
meta_study_file = os.path.join(project_dir, "meta_study.txt")
with open(meta_study_file, "w") as f:
    f.write("type_of_cancer: mixed\n")
    f.write(f"cancer_study_identifier: {study_identifier}\n")
    f.write(f"name: {name}\n")
    f.write("reference_genome: hg38\n")
    f.write("add_global_case_list: true\n")
    f.write(f"description: {description}\n")

print("meta_study.txt is complete")
# meta_study.txt is complete

# Next create meta_clinical_sample.txt

meta_clinical_sample_file = os.path.join(project_dir, "meta_clinical_sample.txt")
with open(meta_clinical_sample_file, "w") as f:
    f.write(f"cancer_study_identifier: {study_identifier}\n")
    f.write("genetic_alteration_type: CLINICAL\n")
    f.write("datatype: SAMPLE_ATTRIBUTES\n")
    f.write("data_filename: data_clinical_sample.txt\n")

print("meta_clinical_sample.txt is complete")
