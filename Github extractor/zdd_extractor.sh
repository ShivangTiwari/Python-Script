#!/bin/bash

# Set the root directory
root_directory=

# Set the output file
output_file="output.csv"

# Add column names to the output file
echo "ZONE,CLUSTER,APPLICATION,ENV PROPERTY" > "$output_file"

# Loop over PCI and NONPCI directories
for environment in ""; do

    # Set the full path for the current environment
    environment_path="$root_directory/$environment"

    # Determine the abbreviated environment name for the output file
    abbreviated_env=""
    if [[ $environment == *"pcidss"* ]]; then
        abbreviated_env="PCI"
    else
        abbreviated_env="Non-PCI"
    fi

    # Use find to get a list of YAML files in the current environment and loop over them
    find "$environment_path" -type f -name "*.yaml" ! -name "descriptor.yaml" -print | while read -r file_path; do
        # Extract the immediate parent directory as the cluster name
        cluster_name=$(basename "$(dirname "$(dirname "$file_path")")")

        # Use awk to search for POOL_SIZE and MAX_IDLE and print respective lines
        awk -v zone="$abbreviated_env" -v cluster="$cluster_name" -v OFS=',' '
            /^[a-zA-Z0-9_-]+:/ {
                if (application) {
                    print zone, cluster, application, property
                }
                application=$1
                gsub(/:$/, "", application)  # Remove colon from the end of the line
                property=""
            }
            /POOL_SIZE|pool_size|MAX_IDLE|max_idle/ && !/HTTP|http/ {
                property=sprintf("%s %s", property, $0)
            }
            END {
                if (application) {
                    print zone, cluster, application, property
                }
            }' "$file_path" >> "$output_file"
    done

done
