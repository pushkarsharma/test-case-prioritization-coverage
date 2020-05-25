#!/usr/bin/python3

import os
import csv
import random


class Selector:
    def __init__(self):
        self.test_cases = []
        self.all_stmts = set()
        self.all_branches = set()
        # self.total_stmt = 0
        # self.total_branches = 0

    def reset(self):
        self.__init__()

    def random(self):
        """[Random Prioritization]

        Returns:
            [list] -- [random ordered test cases]
        """
        temp_test_cases = list(self.test_cases)
        random.shuffle(temp_test_cases)
        return temp_test_cases

    def total_coverage(self, stmt):
        """[Total Coverage Prioritization]

        Arguments:
            stmt {[bool]} -- [Boolean for criteria]

        Returns:
            [list] -- [Sorted test cases based on criteria]
        """
        if stmt:
            return sorted(self.test_cases, reverse=True, key=lambda x: len(x[1]))
        else:
            return sorted(self.test_cases, reverse=True, key=lambda x: len(x[2]))

    def select_max_test_case(self, leftover, test_cases, stmt):
        """[Select maximum test case]

        Arguments:
            leftover {[set]} -- [Leftover statements/branches]
            test_cases {[list]} -- [applicable test cases]
            stmt {[bool]} -- [Boolean for criteria]

        Returns:
            [list] -- [Test case]
        """
        max_tc_pos = 0
        max_intersection = 0
        for pos, tc in enumerate(test_cases):
            if stmt:
                if len(leftover.intersection(tc[1])) > max_intersection:
                    max_tc_pos = pos
                    max_intersection = len(leftover.intersection(tc[1]))
            else:
                if len(leftover.intersection(tc[2])) > max_intersection:
                    max_tc_pos = pos
                    max_intersection = len(leftover.intersection(tc[2]))
        return test_cases.pop(max_tc_pos)

    def additional_selector(self, stmt):
        """[Additional Selector Prioritization]

        Arguments:
            stmt {[bool]} -- [Boolean for criteria]

        Returns:
            [list] -- [Selected test cases]
        """
        selected_test = []
        if stmt:
            leftover_stmts = set(self.all_stmts)
            intersecting_test_cases = list(self.test_cases)
            while leftover_stmts:
                max_test_case = self.select_max_test_case(
                    leftover_stmts, intersecting_test_cases, stmt)
                selected_test.append(max_test_case[0])
                leftover_stmts = leftover_stmts.difference(max_test_case[1])
                intersecting_test_cases = [
                    t for t in intersecting_test_cases if leftover_stmts.intersection(t[1])]
        else:
            left_branches = set(self.all_branches)
            intersecting_test_cases = list(self.test_cases)
            while left_branches:
                max_test_case = self.select_max_test_case(
                    left_branches, intersecting_test_cases, stmt)
                selected_test.append(max_test_case[0])
                left_branches = left_branches.difference(max_test_case[2])
                intersecting_test_cases = [
                    t for t in intersecting_test_cases if left_branches.intersection(t[2])]
        return selected_test

    def retrieve_tests(self, benchmark):
        """[Fetch all the test cases from the CSV file]

        Arguments:
            benchmark {[string]} -- [Benchmark name]
        """
        with open('_PROJECT_DIR_/output/' + benchmark + '/' + benchmark + '.csv',
                  'r') as benchmark_file:
            csv_reader = csv.reader(benchmark_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    test_case = []
                    test_case.append(int(row[0]))  # Test_ID
                    # Executed Statements
                    test_case.append(set([int(i) for i in row[2].split()]))
                    # Taken Branches
                    test_case.append(set([int(i) for i in row[4].split()]))
                    self.all_stmts = self.all_stmts.union(
                        set([int(i) for i in row[2].split()]))
                    self.all_branches = self.all_branches.union(
                        set([int(i) for i in row[4].split()]))
                    self.test_cases.append(test_case)
                line_count += 1

    def selector(self, t_cases, stmt):
        """[Selector for random, total prioritizations]

        Arguments:
            t_cases {[list]} -- [All test cases in required order]
            stmt {[bool]} -- [Boolean for criteria]

        Returns:
            [list] -- [Selected test case IDs]
        """
        selected_set = set()
        selected_test = []
        for test_case in t_cases:
            if stmt and len(self.all_stmts.difference(selected_set)):
                if len(selected_set.union(test_case[1])) > len(selected_set):
                    selected_set = selected_set.union(test_case[1])
                    selected_test.append(test_case[0])
            elif not stmt and len(self.all_branches.difference(selected_set)):
                if len(selected_set.union(test_case[2])) > len(selected_set):
                    selected_set = selected_set.union(test_case[2])
                    selected_test.append(test_case[0])
            else:
                break
        return selected_test

    def test_suite_generator(self, stmt, priority, tests):
        """[Generate test suites with selected test case IDs]

        Arguments:
            stmt {[bool]} -- [Boolean for criteria]
            priority {[string]} -- [Prioritization]
            tests {[list]} -- [Selected test case IDs]
        """
        try:
            os.mkdir(
                "_PROJECT_DIR_/output/"+benchmark+"/test-suite/")
        except FileExistsError:
            print("Directory already exists!")
        if stmt_bool:
            test_suite_file = open("_PROJECT_DIR_/output/" +
                                   benchmark+"/test-suite/statement-"+priority+".txt", "w")
        else:
            test_suite_file = open("_PROJECT_DIR_/output/" +
                                   benchmark+"/test-suite/branch-"+priority+".txt", "w")
        universe_file = open(
            "_PROJECT_DIR_/benchmarks/"+benchmark+"/universe.txt", "r")
        for st in tests:
            universe_test = universe_file.readline()
            line_counter = 1
            while universe_test:
                if line_counter == st:
                    test_suite_file.write(universe_test)
                    break
                universe_test = universe_file.readline()
                line_counter += 1
            universe_file.seek(0)
        universe_file.close()
        test_suite_file.close()


if __name__ == '__main__':
    benchmarks = list(
        os.walk('_PROJECT_DIR_/output/'))[0][1]
    for benchmark in benchmarks:
        p = Selector()
        print('\n\n-------------------' + benchmark + '-------------------')
        p.retrieve_tests(benchmark)
        for stmt_bool in [True, False]:
            if stmt_bool:
                print('--------Statements--------')
            else:
                print('--------Branches--------')
            rand_test_cases = p.random()
            selected_test = p.selector(rand_test_cases, stmt_bool)
            print('Random: ' + str(selected_test))
            p.test_suite_generator(stmt_bool, 'random', selected_test)

            total_coverage_cases = p.total_coverage(stmt_bool)
            selected_test = p.selector(total_coverage_cases, stmt_bool)
            p.test_suite_generator(stmt_bool, 'total', selected_test)
            print('Total Coverage: ' + str(selected_test))

            additional_selected = p.additional_selector(stmt_bool)
            p.test_suite_generator(
                stmt_bool, 'additional', additional_selected)
            print('Additional Coverage: ' + str(additional_selected))
