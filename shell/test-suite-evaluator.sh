#!/bin/bash

# Benchmarks Names
for path in _PROJECT_DIR_/benchmarks/*; do
  name="$(echo "$path" | cut -d'/' -f8)"
  echo "cd $path" >> shell/test-suite-evaluator-run.sh

  # Compiling original version
  if [[ $name = totinfo || $name = replace ]]; then
    echo "gcc -Wno-return-type -g -o $name $name.c -lm -fprofile-arcs -ftest-coverage" >> shell/test-suite-evaluator-run.sh
  else
    echo "gcc -Wno-return-type -g -o $name $name.c -fprofile-arcs -ftest-coverage" >> shell/test-suite-evaluator-run.sh
  fi

  # Running test-suites on original program
  for test_suite in _PROJECT_DIR_/output/$name/test-suite/*; do
    while IFS= read -r test_case
    do
      echo "mkdir -p _PROJECT_DIR_/output/$name/test-suite-outputs/original" >> shell/test-suite-evaluator-run.sh 
      echo "./$name $test_case >> _PROJECT_DIR_/output/$name/test-suite-outputs/original/$(echo "$test_suite" | cut -d'/' -f10)" >> shell/test-suite-evaluator-run.sh
      echo "rm "$name.gcda"" >> shell/test-suite-evaluator-run.sh
    done < $test_suite
    echo "rm $name.gcno" >> shell/test-suite-evaluator-run.sh
  done
  echo "rm $name" >> shell/test-suite-evaluator-run.sh

  # Running test-suites on faulty versions
  for version_path in _PROJECT_DIR_/benchmarks/$name/*; do
    version="$(echo "$version_path" | cut -d'/' -f9)"
    benchmark_path="_PROJECT_DIR_/benchmarks/$name"
    # Checking if the directory name is like v1 or v2
    if [[ $version =~ v[0-9]+ ]]; then
      echo "cd "$benchmark_path"/$(echo "$version_path" | cut -d'/' -f9)" >> shell/test-suite-evaluator-run.sh
      for v_id in _PROJECT_DIR_/benchmarks/$name/$version_path/*; do
        for inputs in _PROJECT_DIR_/benchmarks/$name/*; do
          if ! [[ $inputs =~ v[0-9]+ ]]; then
            if [[ -d $inputs ]]; then
              echo "cp -rn $inputs ." >> shell/test-suite-evaluator-run.sh
            fi
          fi
        done
        # Compiling the faulty versions
        if [[ $name = totinfo || $name = replace ]]; then
          echo "gcc -Wno-return-type -g -o $name $name.c -lm -fprofile-arcs -ftest-coverage" >> shell/test-suite-evaluator-run.sh
        else
          echo "gcc -Wno-return-type -g -o $name $name.c -fprofile-arcs -ftest-coverage" >> shell/test-suite-evaluator-run.sh
        fi
        echo "mkdir -p _PROJECT_DIR_/output/$name/test-suite-outputs" >> shell/test-suite-evaluator-run.sh
        # Executing test-suites on faulty versions
        for test_suite in _PROJECT_DIR_/output/$name/test-suite/*; do
          while IFS= read -r test_case
          do
            echo "mkdir -p _PROJECT_DIR_/output/$name/test-suite-outputs/"$version >> shell/test-suite-evaluator-run.sh 
            echo "./$name $test_case >> _PROJECT_DIR_/output/$name/test-suite-outputs/$version/$(echo "$test_suite" | cut -d'/' -f10)" >> shell/test-suite-evaluator-run.sh
            echo "rm "$name.gcda"" >> shell/test-suite-evaluator-run.sh
          done < $test_suite
        done
      done
      echo "rm $name $name.gcno" >> shell/test-suite-evaluator-run.sh
    fi
  done
done
chmod +x shell/test-suite-evaluator-run.sh
./shell/test-suite-evaluator-run.sh
rm shell/test-suite-evaluator-run.sh