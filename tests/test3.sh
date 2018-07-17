echo
echo '>> Solving pddl/logistics/problems/strips-log-x-1.pddl ...'
echo
python3 pystrips.py solve pddl/logistics/domain.pddl pddl/logistics/problems/strips-log-x-1.pddl 

echo
echo '>> Solving pddl/logistics/problems/strips-log-x-5.pddl ...'
echo
python3 pystrips.py solve pddl/logistics/domain.pddl pddl/logistics/problems/strips-log-x-2.pddl 

echo
echo '>> Solving pddl/logistics/problems/strips-log-x-2.pddl ...'
echo
python3 pystrips.py solve pddl/logistics/domain.pddl pddl/logistics/problems/strips-log-x-2.pddl 
