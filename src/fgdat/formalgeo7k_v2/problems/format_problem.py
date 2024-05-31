from formalgeo.tools import load_json, save_json, simple_show, show_solution
from formalgeo.solver import Interactor
from formalgeo.parse import parse_theorem_seqs
from fgdat.formalgeo7k_v1.problems.format_problems import get_cleaned_theorem_seqs
import os
import warnings
import time


def format_problem():
    for pid in range(1, 7001):
        problem_cdl = load_json(f"problems/{pid}.json")
        new_problem_cdl = {
            "problem_id": problem_cdl["problem_id"],
            "annotation": problem_cdl["annotation"],
            "annotation_img": problem_cdl["annotation_img"],
            "source": problem_cdl["source"],
            "problem_text_cn": problem_cdl["problem_text_cn"],
            "problem_text_en": problem_cdl["problem_text_en"],
            "problem_img": problem_cdl["problem_img"],
            "construction_cdl": problem_cdl["construction_cdl"],
            "text_cdl": problem_cdl["text_cdl"],
            "image_cdl": problem_cdl["image_cdl"],
            "goal_cdl": problem_cdl["goal_cdl"],
            "problem_answer": problem_cdl["problem_answer"],
            "theorem_seqs": problem_cdl["theorem_seqs"],
            "theorem_seqs_dag": problem_cdl["theorem_seqs_dag"],
        }

        save_json(new_problem_cdl, f"problems/{pid}.json")
        print(f"{pid} ok.")


def add_img_annotation():
    cowork_log = load_json("files/img_annotation.json")
    for date in cowork_log:
        for worker in cowork_log[date]:
            for problems in cowork_log[date][worker]:
                start_pid, end_pid = problems.split("-")
                for pid in range(int(start_pid), int(end_pid) + 1):
                    problem_cdl = load_json(f"problems/{pid}.json")
                    new_problem_cdl = {
                        "problem_id": problem_cdl["problem_id"],
                        "annotation": problem_cdl["annotation"],
                        "annotation_img": f"{worker}_{date}",
                        "source": problem_cdl["source"],
                        "problem_level": problem_cdl["problem_level"],
                        "problem_text_cn": problem_cdl["problem_text_cn"],
                        "problem_text_en": problem_cdl["problem_text_en"],
                        "problem_img": problem_cdl["problem_img"],
                        "construction_cdl": problem_cdl["construction_cdl"],
                        "text_cdl": problem_cdl["text_cdl"],
                        "image_cdl": problem_cdl["image_cdl"],
                        "goal_cdl": problem_cdl["goal_cdl"],
                        "problem_answer": problem_cdl["problem_answer"],
                        "theorem_seqs": problem_cdl["theorem_seqs"],
                        "theorem_seqs_dag": problem_cdl["theorem_seqs_dag"],
                    }

                    save_json(new_problem_cdl, f"problems/{pid}.json")
                    print(f"{pid} ok.")


def auto_check_problem():
    warnings.filterwarnings("ignore")
    solver = Interactor(load_json("gdl/predicate_GDL.json"), load_json("gdl/theorem_GDL.json"))
    log = {"unsolved": [], "error": {}, "no_theorem": []}

    for pid in range(1, 7001):
        timing = time.time()
        try:
            problem_cdl = load_json(f"problems/{pid}.json")
            solver.load_problem(problem_cdl)

            for t_name, t_branch, t_para in parse_theorem_seqs(problem_cdl["theorem_seqs"]):
                solver.apply_theorem(t_name, t_branch, t_para)
            solver.problem.check_goal()

            if solver.problem.goal.solved:
                theorem_seqs, theorem_seqs_dag = get_cleaned_theorem_seqs(solver, problem_cdl, True)
                problem_cdl["theorem_seqs"] = theorem_seqs
                problem_cdl["theorem_seqs_dag"] = theorem_seqs_dag
                problem_cdl["problem_level"] = len(theorem_seqs)
                save_json(problem_cdl, f"problems/{pid}.json")

                if len(theorem_seqs) == 0:
                    log["no_theorem"].append(pid)
            else:
                log["unsolved"].append(pid)

            simple_show(solver.problem, time.time() - timing)  # show solved msg

        except BaseException as e:  # exception
            log["error"][pid] = repr(e)
            print(f"pid:{pid} error: {repr(e)}")

    save_json(log, f"log/auto_check_problem_log_{int(time.time())}.json")


def check_problem(clean_theorem=False):
    solver = Interactor(load_json("gdl/predicate_GDL.json"), load_json("gdl/theorem_GDL.json"))

    while True:
        try:
            pid = int(input("pid:"))
            problem_cdl = load_json(f"problems/{pid}.json")
        except BaseException as e:
            print(f"error: {repr(e)}")
            print()
            continue
        solver.load_problem(problem_cdl)
        for t_name, t_branch, t_para in parse_theorem_seqs(problem_cdl["theorem_seqs"]):
            solver.apply_theorem(t_name, t_branch, t_para)
        solver.problem.check_goal()

        if clean_theorem and solver.problem.goal.solved:
            theorem_seqs, theorem_seqs_dag = get_cleaned_theorem_seqs(solver, problem_cdl, True)
            problem_cdl["theorem_seqs"] = theorem_seqs
            problem_cdl["theorem_seqs_dag"] = theorem_seqs_dag
            problem_cdl["problem_level"] = len(theorem_seqs)
            save_json(problem_cdl, f"problems/{pid}.json")

        show_solution(solver.problem)
        print()


if __name__ == '__main__':
    working_directory = "../../../../projects/formalgeo7k-v2"
    os.chdir(working_directory)
    format_problem()
    # add_img_annotation()
    # auto_check_problem()
    # check_problem()
