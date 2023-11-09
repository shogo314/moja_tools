"""convert to zip"""

import os
import glob
import json
import shutil


def read_PROBLEM(PROBLEM_path):
    if not os.path.isfile(PROBLEM_path):
        print(PROBLEM_path, "が見つかりません。")
        return None

    read_title = None
    read_reference_solution = None

    def atcoder_config(task_id=None):
        pass

    def problem(
        time_limit=2.0,
        id="X",
        title="X: Your Problem Name",
        wiki_name="Your pukiwiki page name",
        assignees=[],
        need_custom_judge=True,
        reference_solution="",
    ):
        global read_title,read_reference_solution
        read_title = title
        read_reference_solution = reference_solution

    with open(PROBLEM_path, "r") as f:
        exec(f.read())

    if read_title is None or read_reference_solution is None:
        print("PROBLEMの中にproblem関数が見つかりません。")
        return None

    return read_title, read_reference_solution


def search_TESTSET_and_SOLUTION(problem_directory_path, reference_solution):
    directory_list = glob.glob(problem_directory_path)
    TESTSET_directory = None
    SOLUTION_directory = None
    for d in directory_list:
        if os.path.isfile(os.path.join(d, "TESTSET")):
            if TESTSET_directory is not None:
                print("There are two or more TESTSET directories.")
                return None
            TESTSET_directory = d.split(os.path.pathsep)[-1]
        if os.path.isfile(os.path.join(d, "SOLUTION")):
            if d.split(os.path.pathsep)[-1] == reference_solution:
                SOLUTION_directory = d.split(os.path.pathsep)[-1]
    if TESTSET_directory is None:
        print("TESTSET", "が見つかりません。")
        return None
    if SOLUTION_directory is None:
        print("SOLUTION", "が見つかりません。")
        return None

    return TESTSET_directory, SOLUTION_directory


def write_problem_json(problem_directory_path, moja_out_directory_path, read_title):
    problem_json_path = os.path.join(problem_directory_path, "problem.json")
    if ":" in read_title:
        title = read_title.split(":")[1].strip()
    else:
        title = read_title
    problem_json_flag = False
    if os.path.exists(problem_json_path):
        try:
            with open(problem_json_path, "r") as f:
                json_load = json.load(f)
                title = json_load["title"]
                problem_json_flag = True
        except:
            pass

    if problem_json_flag:
        shutil.copy(
            problem_json_path, os.path.join(moja_out_directory_path, "problem.json")
        )
    else:
        with open(os.path.join(moja_out_directory_path, "problem.json")) as f:
            f.write(json.dump({"title", title}, indent=4))


def write_testcases(rime_out_testset, rime_out_solution, moja_out_in, moja_out_out):
    for rime_out_in in glob.glob(rime_out_testset):
        file_in = os.path.basename(rime_out_in)
        if not file_in.endswith(".in"):
            continue
        file_stem = file_in.removesuffix(".in")
        file_out = file_stem + ".out"
        rime_out_out = os.path.join(rime_out_solution, file_out)
        if not os.path.isfile(rime_out_out):
            continue
        moja_in_case = os.path.join(moja_out_in, file_in)
        moja_out_case = os.path.join(moja_out_out, file_out)
        shutil.copy(rime_out_in, moja_in_case)
        shutil.copy(rime_out_out, moja_out_case)


def main(argv):
    if len(argv) != 1:
        print("mjtools", "rime_to_zip", "<problem_path>")
        print("の形式で書いてください。")
        return 0
    problem_directory_path = os.path.abspath(argv[0])
    PROBLEM_path = os.path.join(problem_directory_path, "PROBLEM")

    tmp = read_PROBLEM(PROBLEM_path)
    if tmp is None:
        return 1
    read_title, read_reference_solution = tmp

    README_path = os.path.join(problem_directory_path, "README.md")

    if not os.path.isfile(README_path):
        print(README_path, "が見つかりません。")
        return 1

    EDITORIAL_path = os.path.join(problem_directory_path, "EDITORIAL.md")
    if not os.path.isfile(EDITORIAL_path):
        EDITORIAL_path = None

    tmp = search_TESTSET_and_SOLUTION(problem_directory_path, read_reference_solution)
    if tmp is None:
        return 1
    TESTSET_directory, SOLUTION_directory = tmp

    rime_out_directory_path = os.path.join(problem_directory_path, "rime-out")
    if not os.path.isdir(rime_out_directory_path):
        print(rime_out_directory_path, "が見つかりません。")
        return 1
    rime_out_testset = os.path.join(rime_out_directory_path, TESTSET_directory)
    if not os.path.isdir(rime_out_testset):
        print(rime_out_testset, "が見つかりません。")
        return 1
    rime_out_solution = os.path.join(rime_out_directory_path, SOLUTION_directory)
    if not os.path.isdir(rime_out_solution):
        print(rime_out_solution, "が見つかりません。")
        return 1

    moja_out_directory_path = os.path.join(problem_directory_path, "moja-out")
    if os.path.exists(moja_out_directory_path):
        shutil.rmtree(moja_out_directory_path)
    os.mkdir(moja_out_directory_path)

    write_problem_json(problem_directory_path, moja_out_directory_path, read_title)

    shutil.copy(README_path, os.path.join(moja_out_directory_path, "README.md"))

    if EDITORIAL_path is not None:
        shutil.copy(
            EDITORIAL_path, os.path.join(moja_out_directory_path, "EDITORIAL.md")
        )

    os.mkdir(os.path.join(moja_out_directory_path, "testcases"))
    moja_out_in = os.path.join(moja_out_directory_path, "testcases", "in")
    moja_out_out = os.path.join(moja_out_directory_path, "testcases", "out")
    os.mkdir(moja_out_in)
    os.mkdir(moja_out_out)

    write_testcases(rime_out_testset, rime_out_solution, moja_out_in, moja_out_out)

    return 0
