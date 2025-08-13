# Main script to run all the entire process

set -x

while getopts "i:p:v:" opt; do
  case $opt in
    i) input_csv="$OPTARG";;
    p) project_dir="$OPTARG";;
    v) vcf_dir="$OPTARG";;
    \?) echo "Invalid option -$OPTARG" >&2;;
  esac
done
# input_csv: contains clinical data and their additional information
# project_dir: Is the directory where the final project files will be stored
# vcf_dir: Is the directory where the VCF files are located

# Check if files and directories exist
if [ ! -f "$input_csv" ]; then
  echo "Input CSV file not found: $input_csv" >&2
  exit 1
fi

if [ ! -d "$project_dir" ]; then
  echo "Project directory not found, making one . . ."
  mkdir -p "$project_dir"
fi

if [ ! -d "$vcf_dir" ]; then
  echo "VCF directory not found: $vcf_dir" >&2
  exit 1
fi

# Get the absolute path to the CBP_Scripts directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_DIR="$(dirname "$SCRIPT_DIR")"
TEMP_DIR="$(dirname "$project_dir")/temp_cbioportal"
mkdir -p "$TEMP_DIR/maf_files"

# run process_vcf.py on vcf_dir
PROCESSED_DIR="$(realpath "$TEMP_DIR/processed")"
for vcf_file in "$vcf_dir"/*.vcf; do
    python "$SCRIPT_DIR/process_vcf.py" --input-vcf "$vcf_file" --output-dir "$PROCESSED_DIR"
done

# The processed vcf right now is in hg19 format we need to change the chrom naming convention to GRCh37 to match our reference
module load gcc/8.3.0 bcftools/1.8
GRCH37_DIR="$(realpath "$TEMP_DIR/GRCh37_format")"
mkdir -p "$GRCH37_DIR"
for vcf_file in "$PROCESSED_DIR"/*.vcf; do
    bcftools annotate --rename-chrs "$MAIN_DIR/chr_map.txt" -o "$GRCH37_DIR/$(basename "$vcf_file" .vcf).GRCh37.vcf" "$vcf_file"
done

# run vcf2maf.pl container on all file in PROCESSED_DIR
# build apptainer
DEF_FILE="$MAIN_DIR/niagara_apptainer.def"
SIF_FILE="$MAIN_DIR/niagara_apptainer.sif"

if [ ! -f "$SIF_FILE" ]; then
  apptainer --verbose build "$SIF_FILE" "$DEF_FILE"
fi

SCRATCH_ABS="$(realpath "$SCRATCH")"
TEMP_DIR_ABS="$(realpath "$TEMP_DIR")"
# loop through directory
for vcf_file in "$GRCH37_DIR"/*.vcf; do
    vcf_file_container="/mount${vcf_file#$SCRATCH_ABS}"
    maf_file_container="${TEMP_DIR_ABS/#$SCRATCH_ABS/\/mount}/maf_files/$(basename "$vcf_file" .hard-filtered.vcf).maf"
    apptainer run --bind "$SCRATCH_ABS:/mount/" "$SIF_FILE" "$vcf_file_container" "$maf_file_container"
done

# Merge the MAF files
conda install pandas numpy
python "$SCRIPT_DIR/merge_maf.py" --input-dir "$TEMP_DIR/maf_files" --output-file "$TEMP_DIR/data_mutation_extended.txt"


# Need to tell user the naming conventions
echo "The naming structure of the project Name is <ACRONYM: Top-level-OncoTree - Concept (PI, Centre)>"
echo "1. ACRONYM <- if your study has an acronym for it"
echo "2. Top-level-OncoTree <- the Cancer Type Detailed Name"
echo "3. Concept <- Xenograft? Cell line? Clinical Trial? Landscape of cohorts? etc"
echo "4. PI <- Main Principal Investigator of the project"
echo "5. Centre <- which centre generated this data"

# Make metadata file
echo "Enter study identifier:"
read study_id
echo "Enter study name:"
read study_name

python "$SCRIPT_DIR/metadata_maker.py" --study-identifier "$study_id" --name "$study_name" --project-dir "$project_dir" --sample-csv "$input_csv"

# Make clinical sample data file
python "$SCRIPT_DIR/clinicaldata_maker.py" --input-csv "$input_csv" --project-dir "$project_dir"
