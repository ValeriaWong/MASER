from utils.register import registry
import engine,agents,hospital,utils
from utils.options_law_fact import get_parser

import os 
os.environ['OPENAI_API_KEY'] = '' # my

os.environ['OPENAI_API_BASE'] = ''
api_key = os.environ.get('OPENAI_API_KEY')
# print(api_key)

if __name__ == '__main__':
    args = get_parser()
    scenario = registry.get_class(args.scenario)(args)
    if not args.parallel:
        scenario.run()
    else:
        scenario.parallel_run()






