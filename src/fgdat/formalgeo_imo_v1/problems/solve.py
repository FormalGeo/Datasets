# pip install formalgeo
import os
from formalgeo.tools import load_json, save_json, show_solution
from formalgeo.tools import get_solution_hypertree, draw_solution_hypertree, get_theorem_dag, draw_theorem_dag
from formalgeo.solver import Interactor
from formalgeo.parse import parse_theorem_seqs

working_directory = "../../../../projects/formalgeo-imo-v1"
os.chdir(working_directory)

solver = Interactor(
    load_json("gdl/predicate_GDL.json"),  # 配置形式化体系
    load_json("gdl/theorem_GDL.json")
)

pid = int(input("pid:"))
problem_cdl = load_json(f"problems/{pid}.json")  # 输入问题
solver.load_problem(problem_cdl)

for t_name, t_branch, t_para in parse_theorem_seqs(problem_cdl["theorem_seqs"]):  # 应用定理
    solver.apply_theorem(t_name, t_branch, t_para)
solver.problem.check_goal()

show_solution(solver.problem)

save_json(get_solution_hypertree(solver.problem), f"{pid}_hypertree.json")
save_json(get_theorem_dag(solver.problem), f"{pid}_dag.json")
draw_solution_hypertree(solver.problem, "./")
draw_theorem_dag(solver.problem, "./")
