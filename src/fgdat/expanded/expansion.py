import os
import time
import warnings
from formalgeo.solver import Interactor
from formalgeo.core import EquationKiller as EqKiller
from formalgeo.parse import parse_theorem_seqs, inverse_parse_one, inverse_parse_one_theorem
from formalgeo.tools import safe_save_json, load_json, save_json, debug_print
from func_timeout import FunctionTimedOut, func_set_timeout


class Expander:
    def __init__(self, path_datasets, random_search, debug=False):
        self.path_datasets = path_datasets
        self.random_search = random_search
        self.stop_pid = load_json(os.path.join(self.path_datasets, "info.json"))["problem_number"] + 1
        self.debug = debug

        self.solver = Interactor(
            load_json(os.path.join(self.path_datasets, "gdl/", "predicate_GDL.json")),
            load_json(os.path.join(self.path_datasets, "gdl/", "theorem_GDL.json"))
        )
        if self.random_search:
            EqKiller.use_cache = True
            self.t_msg = load_json(os.path.join(self.path_datasets, "files/", "t_info.json"))

        if "expanded_log.json" not in os.listdir(os.path.join(self.path_datasets, "files/")):
            self.log = {"break_pid": 1, "pid_count": self.stop_pid}
        else:
            self.log = load_json(os.path.join(self.path_datasets, "files/", "expanded_log.json"))

        self.data = None

    def start(self):
        while self.log["break_pid"] < self.stop_pid:
            problem_CDL = load_json(
                os.path.join(self.path_datasets, "problems", "{}.json".format(self.log["break_pid"])))

            print("\033[36m(pid={})\033[0m Start Expanding.".format(self.log["break_pid"]))

            try:
                self.load_problem(problem_CDL)  # init problem and apply theorem
            except FunctionTimedOut:
                pass
            self.solver.problem.check_goal()

            self.data = []
            self.expand()

    @func_set_timeout(300)
    def load_problem(self, problem_CDL):
        EqKiller.cache_eqs = {}  # init cache
        EqKiller.cache_target = {}
        self.solver.load_problem(problem_CDL)
        if self.random_search:
            timing = time.time()
            count = 0
            update = True
            while update:
                update = False
                for t_name in self.t_msg:
                    if self.t_msg[t_name][0] != 1:
                        continue
                    update = self.solver.apply_theorem(t_name) or update
                    debug_print(
                        self.debug,
                        "\033[34m(pid={},random_search=True,timing={:.4f}s,count={})\033[0m Apply theorem <{}>.".format(
                            self.log["break_pid"], time.time() - timing, count, t_name)
                    )
                    count += 1

            update = True
            while update:
                update = False
                for t_name in self.t_msg:
                    if self.t_msg[t_name][0] == 3:
                        continue
                    update = self.solver.apply_theorem(t_name) or update
                    debug_print(
                        self.debug,
                        "\033[34m(pid={},random_search=True,timing={:.4f}s,count={})\033[0m Apply theorem <{}>.".format(
                            self.log["break_pid"], time.time() - timing, count, t_name)
                    )
                    count += 1
        else:
            timing = time.time()
            for t_name, t_branch, t_para in parse_theorem_seqs(problem_CDL["theorem_seqs"]):
                self.solver.apply_theorem(t_name, t_branch, t_para)
            debug_print(self.debug,
                        "\033[34m(pid={},random_search=False,timing={:.4f}s,count={})\033[0m Apply theorems.".format(
                            self.log["break_pid"], time.time() - timing, len(problem_CDL["theorem_seqs"])))

    def expand(self):
        problem = self.solver.problem
        expanded_cid = []  # (cid, goal_GDL, problem_answer)

        for cid in range(len(problem.condition.items)):  # generate logic goal
            predicate, item, premise, theorem, step = problem.condition.items[cid]
            if predicate in ["Shape", "Collinear", "Cocircular", "Point", "Line", "Arc",
                             "Angle", "Polygon", "Circle"] \
                    or theorem[0] in ["prerequisite", "extended"]:
                continue

            goal_GDL = inverse_parse_one(predicate, item, problem)
            if "Equation" in goal_GDL or "Value" in goal_GDL:
                continue

            if "Equal" in goal_GDL:  # algebra
                problem_answer = "0"
            else:  # logic
                problem_answer = goal_GDL
                goal_GDL = "Relation({})".format(goal_GDL)

            expanded_cid.append((cid, goal_GDL, problem_answer))

        for sym in problem.condition.value_of_sym:  # generate algebra goal
            value = problem.condition.value_of_sym[sym]
            if value is None:
                continue
            try:
                cid = problem.condition.get_id_by_predicate_and_item("Equation", sym - value)
            except KeyError:
                continue

            problem_answer = str(value).replace(" ", "")
            attr, paras = problem.condition.attr_of_sym[sym]
            if attr == "Free":
                goal_GDL = "Value(" + "".join(paras[0]) + ")"
            else:
                goal_GDL = "Value(" + attr + "(" + "".join(paras[0]) + "))"

            expanded_cid.append((cid, goal_GDL, problem_answer))

        expanded = []  # list of (added_conditions, goal_GDL, problem_answer, theorem_seqs)
        for cid, goal_GDL, problem_answer in expanded_cid:
            print(str((cid, goal_GDL, problem_answer)))
            theorem_seqs = []
            _, _, premise, theorem, _ = problem.condition.items[cid]
            if theorem[0] not in ["solve_eq", "prerequisite", "extended"]:
                theorem_seqs.append(theorem)
            premises = self.select_premises(premise)

            while len(premises) > 0:

                if len(theorem_seqs) > 0:  # add expanded problems
                    added_conditions = []
                    for i in premises:
                        predicate, item, _, _, _ = problem.condition.items[i]
                        condition = inverse_parse_one(predicate, item, problem)
                        if "Value" in condition:
                            condition = condition.replace("Value", "Equal")
                        added_conditions.append(condition)
                    added = (tuple(added_conditions), goal_GDL, problem_answer, tuple(theorem_seqs[::-1]))
                    if added not in expanded:
                        expanded.append(added)

                _, _, premise, theorem, _ = problem.condition.items[premises[0]]
                premises.pop(0)  # remove condition 0
                for i in range(len(premises))[::-1]:  # remove condition i which in same group with premises[0]
                    _, _, new_premise, new_theorem, _ = problem.condition.items[premises[i]]
                    if theorem == new_theorem and premise == new_premise:
                        premises.pop(i)

                theorem_seqs.append(theorem)
                for i in self.select_premises(premise):
                    if i not in premises:
                        premises.append(i)

            if len(theorem_seqs) > 0:
                added = (tuple([]), goal_GDL, problem_answer, tuple(theorem_seqs[::-1]))
                if added not in expanded:
                    expanded.append(added)

        saved = set()    # save expanded
        file_to_save = {}
        filename = "{}.json".format(self.log["break_pid"])
        if filename in os.listdir(os.path.join(self.path_datasets, "expanded/")):  # ensure no duplicate problems
            file_to_save = load_json(os.path.join(self.path_datasets, "expanded/", filename))
            for pid in file_to_save:
                saved.add((tuple(file_to_save[pid]["added_cdl"]), file_to_save[pid]["goal_cdl"]))

        for added_conditions, goal_GDL, problem_answer, theorem_seqs in expanded:
            if (added_conditions, goal_GDL) in saved:
                continue

            cleaned_theorem_seqs = []
            for theorem in theorem_seqs:
                if theorem not in cleaned_theorem_seqs:
                    cleaned_theorem_seqs.append(theorem)

            new_data = {
                "problem_id": self.log["pid_count"],
                "added_cdl": added_conditions,
                "goal_cdl": goal_GDL,
                "problem_answer": problem_answer,
                "theorem_seqs": [inverse_parse_one_theorem(t, self.solver.parsed_theorem_GDL)
                                 for t in cleaned_theorem_seqs]
            }
            file_to_save[str(self.log["pid_count"])] = new_data
            self.log["pid_count"] += 1

        safe_save_json(file_to_save, os.path.join(self.path_datasets, "expanded/", filename))

        debug_print(
            self.debug,
            "\033[34m(pid={},count={})\033[0m Save Expanded.\n".format(self.log["break_pid"], len(self.data)))
        self.log["break_pid"] += 1
        safe_save_json(self.log, os.path.join(self.path_datasets, "files/", "expanded_log.json"))

    def select_premises(self, premises):
        problem = self.solver.problem
        premises = list(premises)

        update = True
        while update and len(premises) > 0:
            update = False
            new_premises = []

            for i in premises:
                _, _, premise, theorem, _ = problem.condition.items[i]
                if theorem[0] not in ["solve_eq", "prerequisite", "extended"]:
                    new_premises.append(i)  # add premise i if getting i need theorem
                else:
                    for p in premise:  # add premises of premise i if getting i don't need theorem
                        if p != -1 and p not in new_premises:
                            new_premises.append(p)
                            update = True

            premises = new_premises

        return list(premises)


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    # expander = Expander(path_datasets="../../../projects/formalgeo7k", random_search=False)
    expander = Expander(path_datasets="../../../projects/formalgeo-imo", random_search=False, debug=True)
    expander.start()
