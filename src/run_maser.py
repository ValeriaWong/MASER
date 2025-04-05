import os
import sys
import json
import argparse
import engine  # 触发所有模型注册
import legal
from utils.register import registry
import engine,agents,legal,utils
from utils.options_law_fact import get_parser

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.register import registry
from agents.supervisor import Supervisor


def parse_args():
    parser = argparse.ArgumentParser(description="Run MASER multi-agent simulation")

    # agent setting
    parser.add_argument('--lawyer', type=str, required=True)
    parser.add_argument('--lawyer_openai_model_name', type=str, required=True)
    parser.add_argument('--lawyer_openai_api_key', type=str, default="")
    parser.add_argument('--lawyer_openai_api_base', type=str, default="")
    parser.add_argument('--lawyer_temperature', type=float, default=0.7)
    parser.add_argument('--lawyer_max_tokens', type=int, default=1024)
    parser.add_argument('--lawyer_top_p', type=float, default=1.0)
    parser.add_argument('--lawyer_frequency_penalty', type=float, default=0.0)
    parser.add_argument('--lawyer_presence_penalty', type=float, default=0.0)

    parser.add_argument('--plaintiff', type=str, required=True)
    parser.add_argument('--plaintiff_openai_model_name', type=str, required=True)
    parser.add_argument('--plaintiff_openai_api_key', type=str, default="")
    parser.add_argument('--plaintiff_openai_api_base', type=str, default="")
    parser.add_argument('--plaintiff_temperature', type=float, default=0.7)
    parser.add_argument('--plaintiff_max_tokens', type=int, default=1024)
    parser.add_argument('--plaintiff_top_p', type=float, default=1.0)
    parser.add_argument('--plaintiff_frequency_penalty', type=float, default=0.0)
    parser.add_argument('--plaintiff_presence_penalty', type=float, default=0.0)

    parser.add_argument('--supervisor', type=str, required=True)
    parser.add_argument('--supervisor_openai_model_name', type=str, required=True)
    parser.add_argument('--supervisor_openai_api_key', type=str, default="")
    parser.add_argument('--supervisor_openai_api_base', type=str, default="")
    parser.add_argument('--supervisor_temperature', type=float, default=0.7)
    parser.add_argument('--supervisor_max_tokens', type=int, default=1024)
    parser.add_argument('--supervisor_top_p', type=float, default=1.0)
    parser.add_argument('--supervisor_frequency_penalty', type=float, default=0.0)
    parser.add_argument('--supervisor_presence_penalty', type=float, default=0.0)

    # general options
    parser.add_argument('--case_database', type=str, required=True)
    parser.add_argument('--save_path', type=str, default="outputs/dialog.jsonl")
    parser.add_argument('--max_conversation_turn', type=int, default=15)
    parser.add_argument('--parallel', type=bool, default=False)

    return parser.parse_args()


def main():
    args = parse_args()

    os.environ['OPENAI_API_KEY'] = args.supervisor_openai_api_key
    os.environ['OPENAI_API_BASE'] = args.supervisor_openai_api_base

    # 加载 case 数据
    with open(args.case_database, 'r', encoding='utf-8') as f:
        case_list = json.load(f)
    case = case_list[0]  # 默认使用第一个 case

    # 获取 agent 类
    lawyer_cls = registry.get_class(args.lawyer)
    plaintiff_cls = registry.get_class(args.plaintiff)
    supervisor_cls = registry.get_class(args.supervisor)

    # 初始化 agent
    lawyer = lawyer_cls(args)
    plaintiff = plaintiff_cls(args, **case)
    supervisor = supervisor_cls(args)

    # 构造对话场景
    scenario = registry.get_class(args.scenario)(args)
    
    # 启动
    if args.parallel:
        scenario.parallel_run()
    else:
        scenario.run()


if __name__ == "__main__":
    main()
