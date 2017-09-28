import sys

base_dir = 'C:/projects/mine/gt'
sys.path.insert(0, base_dir)
sys.path.insert(0, base_dir + 'gt')
sys.path.insert(0, base_dir + 'gt/tests')
sys.path.insert(0, base_dir + 'gt/examples')

# from gt.tests.test_tsp_evolve import run
from test_tsp_evolve import run
run()