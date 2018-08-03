import argparse
import time
import signal

from parser     import Parser
from planner    import RRTPlan
from heuristics import h_naive, h_add

def parse():
    usage = 'python3 pystrips.py {show, ground, solve} <DOMAIN> <INSTANCE> [OPTIONS]'
    description = 'PyStrips is a classical planner using RRT-Plan for PDDL/STRIPS language.'
    help_commands = '''
    show PDDL files, ground all actions or solve domain/problem instance.
    '''.strip()
    parser = argparse.ArgumentParser(usage=usage, description=description)
    parser.add_argument('command', choices=['show', 'ground', 'solve'], help=help_commands)
    parser.add_argument('domain',  type=str, help='path to PDDL domain file')
    parser.add_argument('problem', type=str, help='path to PDDL problem file')
    parser.add_argument('-log', '--log', action='store_true', help='outputs a log file regarding sampling')
    parser.add_argument('-plt', '--plot', action='store_true', help='outputs a plot of RandomTree')
    # parser.add_argument('-w', '--weight', type=float, default=1.0, help='heuristics weight (default=1.0)')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse()

    uptime = {}

    start_time = time.time()
    domain  = Parser.parse(args.domain)
    problem = Parser.parse(args.problem)
    end_time = time.time()
    uptime['parsing'] = end_time - start_time

    if args.command == 'show':
        print(domain)
        print(problem)
    elif args.command == 'ground':
        print(domain)
        print(problem)
        all_actions = problem.ground_all_actions(domain)
        for action in all_actions:
            print(action)
    elif args.command == 'solve':
        start_time = time.time()
        planner = RRTPlan(domain, problem)
        end_time = time.time()
        uptime['grounding'] = end_time - start_time

        # TESTS - RRT PLAN #

        start_time = time.time()
        #signal.signal(signal.SIGALRM, signal.SIG_DFL)
        #signal.alarm(120)
        if args.log:
            solution, rand = planner.solve_log()
        elif args.plot:
            solution, rand = planner.solve_graph_plot()
        else:
            solution, rand = planner.solve()
        #signal.alarm(0)
        end_time = time.time()
        uptime['planning'] = end_time - start_time


        # print statistics
        print('>> solution length =', len(solution))
        print('>> time: parsing = {0:.4f}, grounding = {1:.4f}, planning = {2:.4f}'.format(
              uptime['parsing'], uptime['grounding'], uptime['planning']))
        print()
        print(solution)
     
        if args.verbose:
            print('>> Initial state:')
            print(', '.join(sorted(problem.init)))
            print()
            print('>> Solution:')
            print('\n'.join(map(repr, solution)))
            print()
            print('>> Goal state:')
            print(', '.join(sorted(problem.goal)))
