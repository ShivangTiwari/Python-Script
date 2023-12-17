Cluster Configuration Data Extractor
Overview
This Bash script is designed to extract configuration data from YAML files in a specific directory structure and format the output as a CSV file. The extracted data includes information about the environment, cluster, application, and relevant properties such as POOL_SIZE and MAX_IDLE.

Prerequisites
Bash Shell: Ensure that you have a Bash-compatible shell.
Usage
Clone the Repository: ```bash git clone git@bitbucket.org:zetaengg/hdfc-sre-programs.git cd hdfc-sre-programs

Set Root Directory:

Open the script (zdd_extractor.sh) in a text editor.
Update the root_directory variable with the path to your target directory.
Execute the Script:

Open a terminal.
Navigate to the directory containing the script.
Run the script: ```bash chmod +x zdd_extractor.sh ./zdd_extractor.sh
Review Output:

The script generates an output.csv file with the extracted data.
Open the output.csv file to review the data.
Customization
Environment Names:

The script abbreviates environment names as "PCI" for directories containing "pcidss" and "Non-PCI" otherwise. You can customize this logic based on your directory naming conventions.
Excluded Keywords:

The script excludes lines containing "HTTP" or "http" from the output. Adjust the exclusion criteria as needed.
Notes
Descriptor Files:

The script ignores files named "descriptor.yaml" in the directory structure.
Output Format:

The output CSV file has columns: ZONE, CLUSTER, APPLICATION, ENV PROPERTY.
Run Frequency:

Depending on your requirements, you can manually run the script or set up scheduled runs using cron jobs or other scheduling mechanisms.
