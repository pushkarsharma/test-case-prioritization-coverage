#!/usr/bin/python3

import os
import re
import csv


class Parser:
    def __init__(self):
        self.STMT_COUNT = re.compile(r"^\s+(#####|[0-9]+):\s+[0-9]+:.*")
        self.STMT_EXEC_COUNT = re.compile(r"^\s+[0-9]+:\s+[0-9]+:.*")
        self.BRANCH_COUNT = re.compile(r"^branch\s+[0-9]+.*")
        self.BRANCH_EXEC_COUNT = re.compile(r"^branch\s+[0-9]+\s+taken\s+[1-9][0-9]*.*")
        self.STMT_EXP = re.compile(r"^\s+[0-9]+:\s+([0-9]+):.*")

    def parsing(self, benchmark):
        """[Parser for .gcov file]

        Arguments:
            benchmark {[string]} -- [Benchmark name]
        """
        test_count = len(list(os.walk('_PROJECT_DIR_/output/'+benchmark))[0][1])
        with open('_PROJECT_DIR_/output/'+benchmark+'/'+benchmark+'.csv', mode='w') as benchmark_file:
            print('_PROJECT_DIR_/output/'+benchmark+'/'+benchmark+'.csv')
            benchmark_writer = csv.writer(benchmark_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            benchmark_writer.writerow(['Test ID', 'Total Statements', 'Statements Executed', 'Total Branches', 'Branches Taken'])
            for test_id in range(1, test_count+1):
                line_num = 1
                num_stmts = 0
                num_branches = 0
                statements = set()
                branches = set()
                f = open('_PROJECT_DIR_/output/'+benchmark+'/'+str(test_id)+'/'+benchmark+'.c.gcov', 'r')
                line = f.readline()
                while line:
                    if self.STMT_COUNT.match(line):
                        num_stmts+=1
                        if self.STMT_EXEC_COUNT.match(line):
                            code_line = int(self.STMT_EXP.match(line).group(1))
                            statements.add(code_line)
                    elif self.BRANCH_COUNT.match(line):
                        num_branches+=1
                        if self.BRANCH_EXEC_COUNT.match(line):
                            branches.add(line_num)
                    line_num+=1
                    line = f.readline()
                statements = list(statements)
                branches = list(branches)
                benchmark_writer.writerow([test_id, num_stmts, str(statements)[1:-1].replace(', ', ' '), num_branches, str(branches)[1:-1].replace(', ', ' ')])

if __name__=='__main__':
    p = Parser()
    benchmarks = list(os.walk('_PROJECT_DIR_/output/'))[0][1]
    for benchmark in benchmarks:
        p.parsing(benchmark)
