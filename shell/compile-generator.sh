#!/bin/bash

# Benchmarks Names
for path in _PROJECT_DIR_/benchmarks/*; do
  name="$(echo "$path" | cut -d'/' -f8)"
  echo "cd $path" >> shell/compile-run.sh
  output="_PROJECT_DIR_/output/$name"
  # Compiling the program file
  if [[ $name = totinfo || $name = replace ]]; then
    echo "gcc -Wno-return-type -g -o $name $name.c -lm -fprofile-arcs -ftest-coverage" >> shell/compile-run.sh
  else
    echo "gcc -Wno-return-type -g -o $name $name.c -fprofile-arcs -ftest-coverage" >> shell/compile-run.sh
  fi
  # Running all test cases from universe.txt on original program
  test_num=1
  while IFS= read -r test_case
  do
    echo "./$name $test_case" >> shell/compile-run.sh
    echo "gcov -b -c $name" >> shell/compile-run.sh
    test_num_dir="$output/$test_num"
    echo "mkdir -p $test_num_dir" >> shell/compile-run.sh
    echo "mv "$name.c.gcov" $test_num_dir" >> shell/compile-run.sh
    echo "rm "$name.gcda"" >> shell/compile-run.sh
    let test_num++
  done < "$path/universe.txt"
  echo "rm $name $name.gcno" >> shell/compile-run.sh
done
chmod +x shell/compile-run.sh
./shell/compile-run.sh
rm shell/compile-run.sh
