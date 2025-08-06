# CBP_Scripts
Scripts for cBioPortal project

# General Flow
1. Assume we have a directory full of VCF files, this signifies a study.
2. We first merge the VCF files into a single VCF file.
3. Since the VCF uses TM tumor naming convention and we want to use the SGT naming, we need to rename the column in the merged VCF file and create a SGT/TM mapping file for future use.
4. We then run vcf2maf to convert the VCF file into MAF format.
5. Then we will find the oncotree code for the cancer type of the whole study. If study has multiple cancer types, we will use the most common one. **unsure how to handle this yet**.
6. Then we will make the metadata text file for the study.
7. Then using the SGT/TM mapping file and the provided csv file containing more information about the samples, we will create the data_clinical_sample.txt file.
8. Then we will make the case directory and files.
9. Finally we run metaimport script to validate the study directory and upload the data to cBioPortal (local?).

## Installation_SOP.md
This markdown file provides a step-by-step guide to run vcf2maf, validate your study directory and upload your data to cBioPortal.

## vcf_merger.sh
This script uses bcftools to merge multiple VCF files into a single VCF file. It also renames the tumor sample column to SGT naming convention and creates a mapping file for future reference.

## vcf2maf.sh
This script runs the vcf2maf tool to convert the merged VCF file into MAF format.

## oncotree_code_finder.py
This Python script finds the oncotree code for the cancer type of the study. It uses a predefined mapping of cancer types to oncotree codes. Might need to use API. Might need to have a get majority function to handle multiple cancer types.

## metadata_maker.py
This Python script generates the meta_study.txt and meta_clinical_sample.txt files based on the provided sample information (in csv format) and the SGT/TM mapping file.

## case_directory_maker.py
This Python script handle the case directory creation.

## metaimport.py
This Python script validates the study directory and uploads the data to cBioPortal. It uses the metaimport tool provided by cBioPortal.

## main.py
This Python script orchestrates the entire process by calling the other scripts in the correct order. It handles the flow of data from merging VCF files to uploading the study to cBioPortal.

## Test
This is a test directory to test the entire flow of the scripts. It contains sample VCF files and a sample csv file with sample information. 

