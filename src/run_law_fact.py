from utils.register import registry
import engine,agents,legal,utils
from utils.options_law_fact import get_parser

import os 
os.environ['OPENAI_API_KEY'] = '60b7743008eac454da8079fd3a9c063e2a78c7cb' # my

os.environ['OPENAI_API_BASE'] = 'https://aistudio.baidu.com/llm/lmapi/v3'
api_key = os.environ.get('OPENAI_API_KEY')
# print(api_key)

if __name__ == '__main__':
    args = get_parser()
    scenario = registry.get_class(args.scenario)(args)
    if not args.parallel:
        scenario.run()
    else:
        scenario.parallel_run()






