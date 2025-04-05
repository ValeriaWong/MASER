# import sys
# import os
# sys.path.append(os.getcwd())

import sys
paths = sys.path
for path in paths:
    print(path)


import argparse
import os
import json
from typing import List
import jsonlines
from tqdm import tqdm
import time
import concurrent
import random
from utils.register import register_class, registry
# from retrievel.query_xb import query

# import sys
# print("import path!!!!!!")
# print(sys.path)
