import os
import warnings
import time
from formalgeo.tools import load_json, save_json, get_theorem_dag
from formalgeo.solver import Interactor
from formalgeo.parse import parse_theorem_seqs
from fgdat.problems import get_cleaned_theorem_seqs


def check_expanded(path_datasets, start_pid=1, clean_theorem=False, clean_acc=False):
    """Run method and load problem from problem_GDL."""
    solver = Interactor(load_json(os.path.join(path_datasets, "gdl/predicate_GDL.json")),
                        load_json(os.path.join(path_datasets, "gdl/theorem_GDL.json")))
    warnings.filterwarnings("ignore")
    error_problems = []
    problem_number = load_json(os.path.join(path_datasets, "info.json"))["problem_number"]
    if start_pid == 1:
        pid_count = problem_number + 1
    else:
        pid_count = int(list(load_json(os.path.join(path_datasets, "expanded/{}.json".format(start_pid - 1))))[-1]) + 1

    print("raw_pid\tsolved\ttiming(s)")
    for raw_pid in range(start_pid, problem_number + 1):
        expanded_problems = load_json(os.path.join(path_datasets, "expanded/{}.json".format(raw_pid)))
        solved_problems = {}
        timing = time.time()

        for pid in expanded_problems:
            try:
                problem_CDL = load_json(os.path.join(path_datasets, "problems", "{}.json".format(raw_pid)))
                problem_CDL["problem_id"] += expanded_problems[pid]["problem_id"]
                problem_CDL["text_cdl"] += expanded_problems[pid]["added_cdl"]
                problem_CDL["goal_cdl"] = expanded_problems[pid]["goal_cdl"]
                problem_CDL["problem_answer"] = expanded_problems[pid]["problem_answer"]
                problem_CDL["theorem_seqs"] = expanded_problems[pid]["theorem_seqs"]

                solver.load_problem(problem_CDL)
                for t_name, t_branch, t_para in parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                    solver.apply_theorem(t_name, t_branch, t_para)
                solver.problem.check_goal()

                if not solver.problem.goal.solved:
                    continue

                if clean_theorem:
                    theorem_seqs, theorem_seqs_dag = get_cleaned_theorem_seqs(solver, problem_CDL, clean_acc)
                    if len(theorem_seqs) == 0:
                        continue
                    theorem_seqs_dag = get_theorem_dag(solver.problem)
                    cleaned = {
                        "problem_id": pid_count,
                        "added_cdl": expanded_problems[pid]["added_cdl"],
                        "goal_cdl": expanded_problems[pid]["goal_cdl"],
                        "problem_answer": expanded_problems[pid]["problem_answer"],
                        "theorem_seqs": theorem_seqs,
                        "theorem_seqs_dag": theorem_seqs_dag
                    }
                    solved_problems[pid_count] = cleaned
                    pid_count += 1
                else:
                    solved_problems[pid] = pid
            except BaseException as e:
                error_problems.append((raw_pid, raw_pid, repr(e)))

        if clean_theorem:
            save_json(solved_problems, os.path.join(path_datasets, "expanded/{}.json".format(raw_pid)))
        print("{}\t{}/{}\t{}".format(raw_pid, len(solved_problems), len(expanded_problems), time.time() - timing))

    print("\nraw_pid\tpid\te_msg")
    for raw_pid, pid, e_msg in error_problems:  # show unsolved
        print("{}\t{}\t{}".format(raw_pid, pid, e_msg))


if __name__ == '__main__':
    # check_expanded("../../../projects/formalgeo7k", start_pid=1, clean_theorem=True, clean_acc=False)
    check_expanded("../../../projects/formalgeo-imo", start_pid=8, clean_theorem=True, clean_acc=False)
