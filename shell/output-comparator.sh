#!/bin/bash

printf '%s\n' 'Benchmark' 'Criteria' 'Prioritization' 'Faults' | paste -sd ',' >> _PROJECT_DIR_/output/fault-counts.csv
# Benchmark Names
for path in _PROJECT_DIR_/output/*; do
  if [[ -d $path ]]; then
    name="$(echo "$path" | cut -d'/' -f8)"
    # Finding all combinations of criteria and priotizations
    for criteria in statement branch
    do
      for priority in random total additional
      do
        mismatch_count=0
        for output_folder in _PROJECT_DIR_/output/$name/test-suite-outputs/*; do
          version="$(echo "$output_folder" | cut -d'/' -f10)"
          if [[ $version =~ v[0-9]+ ]]; then
              if [[ $test_file_name="$criteria-$priority.txt" ]]; then
                # Comparing the faulty version outputs with the original program output
                cmp --silent $output_folder/$criteria-$priority".txt" _PROJECT_DIR_/output/$name/test-suite-outputs/original/$criteria-$priority".txt" || let mismatch_count++
              fi
          fi
        done
        # Output to the CSV file
        printf '%s\n' $name $criteria $priority $mismatch_count | paste -sd ',' >> _PROJECT_DIR_/output/fault-counts.csv
      done
    done
  fi
done