import os
from formalgeo.solver import Interactor
from formalgeo.tools import load_json, save_json, show_solution, get_used_pid_and_theorem
from formalgeo.parse import parse_theorem_seqs, parse_one_theorem, inverse_parse_one_theorem


def main(clean_theorem=False, interactive=True):
    solver = Interactor(load_json(os.path.join("../gdl/", "predicate_GDL.json")),
                        load_json(os.path.join("../gdl/", "theorem_GDL.json")))
    while True:
        try:
            pid = input("pid:")
            filename = "{}.json".format(pid)
            problem_CDL = load_json(os.path.join("../problems/", filename))
        except BaseException as e:
            print("Exception: {}\n".format(repr(e)))
            continue

        solver.load_problem(problem_CDL)
        print("Construction complete.")
        for t_name, t_branch, t_para in parse_theorem_seqs(problem_CDL["theorem_seqs"]):
            solver.apply_theorem(t_name, t_branch, t_para)
        solver.problem.check_goal()  # check goal after applied theorem seqs
        show_solution(solver.problem)
        print()

        if interactive:
            while not solver.problem.goal.solved:
                theorem = input("input theorem (enter q to exit): ").strip().replace("\n", "")
                try:
                    t_name, t_branch, t_para = parse_one_theorem(theorem)
                    if theorem == "q":
                        print()
                        break
                    update = solver.apply_theorem(t_name, t_branch, t_para)  # apply_theorem
                except BaseException as e:
                    print("Exception: {}\n".format(repr(e)))
                else:
                    solver.problem.check_goal()  # check goal after applied theorem seqs
                    show_solution(solver.problem)
                    print("Theorem <{}> applied: {}\n".format(theorem, update))

        if clean_theorem and solver.problem.goal.solved:
            _, theorem_seqs = get_used_pid_and_theorem(solver.problem)  # clean theorem seqs
            theorem_seqs = [inverse_parse_one_theorem(t, solver.parsed_theorem_GDL) for t in theorem_seqs]
            problem_CDL["theorem_seqs"] = theorem_seqs
            save_json(problem_CDL, os.path.join("../problems/", filename))


if __name__ == '__main__':
    main(clean_theorem=False, interactive=False)
