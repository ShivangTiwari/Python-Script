#!/bin/bash

# Loop through each line in data.csv
while IFS=',' read -r namespace the_hpa_name m_down m_up; do
    if [ "$1" = "up" ]; then
        patch_data="{\"spec\":{\"minReplicas\": $m_down , \"maxReplicas\": $m_up  }}"
    elif [ "$1" = "down" ]; then
        patch_data="{\"spec\":{\"minReplicas\": 2 , \"maxReplicas\": 2 }}"
    fi
    existing_min=$(kubectl get hpa -n "$namespace" "$the_hpa_name" -o=jsonpath='{.spec.minReplicas}')
    existing_max=$(kubectl get hpa -n "$namespace" "$the_hpa_name" -o=jsonpath='{.spec.maxReplicas}')

    echo "The existing min and max values of $the_hpa_name in $namespace cluster are $existing_min , $existing_max"

    # patch_data_min_max="{\"spec\":{\"minReplicas\": $m_down,\"maxReplicas\": $m_up }}"
    kubectl patch hpa "$the_hpa_name" -p "$patch_data" -n "$namespace"

    if [ $? -eq 0 ]; then
        echo "Successfully changed $patch_data for $the_hpa_name in $namespace cluster"
    else
        echo "Failed to apply for $the_hpa_name in $namespace cluster"
    fi
done < pci-zc.csv
