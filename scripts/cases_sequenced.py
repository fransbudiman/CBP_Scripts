import pandas as pd
import argparse
import os

# Take project directory, make case_lists directory and the cases_sequenced.txt file
parser = argparse.ArgumentParser(description='Generate cases sequenced file for CBioPortal.')
parser.add_argument('--project-dir', required=True, help='Path to the project directory')
args = parser.parse_args()
project_dir = args.project_dir

num_samples = 0
case_list_ids = []

with open(os.path.join(project_dir, "meta_study.txt"), 'r') as meta_file:
    for line in meta_file:
        if line.startswith("cancer_study_identifier:"):
            study_id = line.split(":")[1].strip()
            break
stable_id = study_id + "_" + "sequenced"

df = pd.read_csv(os.path.join(project_dir, "data_mutations_extended.txt"), sep="\t", comment='#')
case_list_ids = df["Tumor_Sample_Barcode"].drop_duplicates().tolist()
num_samples = len(case_list_ids)

print(f"Study ID: {study_id}")
print(f"Stable ID: {stable_id}")
print(f"Number of Samples: {num_samples}")
print(f"Case List IDs: {case_list_ids}")

os.makedirs(os.path.join(project_dir, "case_lists"), exist_ok=True)
with open(os.path.join(project_dir, "case_lists", "cases_sequenced.txt"), "w") as f:
    f.write(f"cancer_study_identifier: {study_id}\n")
    f.write(f"stable_id: {stable_id}\n")
    f.write(f"case_list_name: Sequenced samples\n")
    f.write(f"case_list_description: Sequenced samples ({num_samples} sample)\n")
    f.write(f"case_list_category: all_cases_with_mutation_data\n")
    f.write(f"case_list_ids: {'\t'.join(case_list_ids)}\n")

print(f"Cases sequenced file created at: {os.path.join(project_dir, 'case_lists', 'cases_sequenced.txt')}")