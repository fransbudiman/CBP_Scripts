# Setting Up Local Instance

To set up a local instance of cBioPortal, you will need to have Docker and Docker Compose installed on your machine. Then follow the steps.

```bash
git clone https://github.com/cBioPortal/cbioportal-docker-compose.git

./init.sh
docker compose up
```
If you are using an older version of docker compose use `docker-compose up` instead.

After this cBioPortal should be running in http://localhost:8080. Do not close the terminal.

<br><br>
# Validating Dataset

After creating your cBioPortal project with all the necessary files and correct structure, you can validate the dataset using the validation tools provided in the `datahub-study-curation-tools` repository.

```bash
git clone https://github.com/cBioPortal/datahub-study-curation-tools.git

python3 datahub-study-curation-tools/validation/validator/validateStudies.py \
  -d /root/directory/path/ \
  -l <list of projects to validate> \
  -html /directory/path/for/reports
```
- -d: Root folder containing all studies
- -l: Whitespace-separated list of study folders to validate (e.g., study_1 study_2)
- -html: Path to save the HTML report(s)
- -h: Show help message

<br><br>
# Importing Project to Local Instance of cBioPortal
To import your project into the local instance of cBioPortal, you can use the `metaImport.py` script found in the docker image. Then the script has to be executed within the container environment. Ensure that your cBioPortal instance is running before executing the import command.

```bash
# First, go to the cbioportal-docker-compose directory
cd cbioportal-docker-compose

# Then, run the metaImport.py script with the appropriate parameters
docker-compose run cbioportal metaImport.py -u http://cbioportal:8080 -s /path/to/study --html /path/to/report.html -v -o
```
- -u: URL of the cBioPortal instance
- -s: Path to the study directory to import
- -html: Path to save the HTML report
- -v: Verbose output
- -o: Override warnings
- -h: Show help message

After this refresh your cBioPortal instance in the browser. You should see your project listed there.

<br><br>
# Converting VCF to MAF
If your mutation data is in VCF format, you can convert it to MAF format using the `vcf2maf` tool.

## Install conda and VEP
```bash
curl -sL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh
bash miniconda.sh -bup $HOME/miniconda3 && rm -f miniconda.sh
export PATH="$HOME/miniconda3/bin:$PATH"
conda init
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
conda update -y -n base -c defaults conda
conda config --set solver libmamba
conda create -y -n vep && conda activate vep
conda install -y -c conda-forge -c bioconda -c defaults ensembl-vep==112.0 htslib==1.20 bcftools==1.20 samtools==1.20 ucsc-liftover==447
```
## Download offline cache for GRch38 and reference FASTA
```bash
mkdir -p $HOME/.vep/homo_sapiens/112_GRCh38/
rsync -avr --progress rsync://ftp.ensembl.org/ensembl/pub/release-112/variation/indexed_vep_cache/homo_sapiens_vep_112_GRCh38.tar.gz $HOME/.vep/
tar -zxf $HOME/.vep/homo_sapiens_vep_112_GRCh38.tar.gz -C $HOME/.vep/
rsync -avr --progress rsync://ftp.ensembl.org/ensembl/pub/release-112/fasta/homo_sapiens/dna_index/ $HOME/.vep/homo_sapiens/112_GRCh38/
rsync -avz --progress rsync://ftp.ensembl.org/ensembl/pub/release-112/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.toplevel.fa.gz $HOME/.vep/homo_sapiens/112_GRCh38/
gzip -d $HOME/.vep/homo_sapiens/112_GRCh38/Homo_sapiens.GRCh38.dna.toplevel.fa.gz
bgzip $HOME/.vep/homo_sapiens/112_GRCh38/Homo_sapiens.GRCh38.dna.toplevel.fa
samtools faidx $HOME/.vep/homo_sapiens/112_GRCh38/Homo_sapiens.GRCh38.dna.toplevel.fa.gz
```
## Common Issues
Missing Perl module:
```bash
conda install -y -c conda-forge perl-app-cpanminus
cpanm List::MoreUtils
```
Setting Locale failed:
```bash
export LANG=C
export LC_ALL=C
```
# Run VCF to MAF
First, we need to download the VCF2MAF tool:
```bash
export VCF2MAF_URL=`curl -sL https://api.github.com/repos/mskcc/vcf2maf/releases | grep -m1 tarball_url | cut -d\" -f4`
curl -L -o mskcc-vcf2maf.tar.gz $VCF2MAF_URL; tar -zxf mskcc-vcf2maf.tar.gz; cd mskcc-vcf2maf-*
```
Now converting:
```bash
perl vcf2maf.pl --input-vcf path/to/VCFfile.vcf --output-maf path/to/result/MAFfile.vep.maf --ref-fasta $HOME/.vep/homo_sapiens/112_GRCh38/Homo_sapiens.GRCh38.dna.toplevel.fa.gz --vep-path "$(dirname "$(which vep)")" --vep-data "$HOME/.vep" --ncbi-build GRCh38 --tumor-id TUMOR --normal-id NORMAL
```