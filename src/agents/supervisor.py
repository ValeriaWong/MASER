import re,random
from .base_agent import Agent
from utils.register import register_class, registry
from utils.guider import guide
from utils.tamperer import temper
from utils.styler import style
import numpy as np

@register_class(alias="Agent.Supervisor.GPT")
class Supervisor(Agent):
    def __init__(self, args, supervisor_info=None):
        engine = registry.get_class("Engine.GPT")(
            openai_api_key=args.supervisor_openai_api_key, 
            openai_api_base=args.supervisor_openai_api_base,
            openai_model_name=args.supervisor_openai_model_name, 
            temperature=args.supervisor_temperature, 
            max_tokens=args.supervisor_max_tokens,
            top_p=args.supervisor_top_p,
            frequency_penalty=args.supervisor_frequency_penalty,
            presence_penalty=args.supervisor_presence_penalty)

        self.edit_query = True
        if supervisor_info is None:
            self.system_message = \
                "你是一个**对话监督者**，在律师向原告询问的过程中，你负责提醒**原告**和**律师**的发言。\n\n" # ，目的是保证律师能够通过与原告对话获得完整的#案件存档#
        else: self.system_message = supervisor_info
        self.stage_list = []
        self.disturbance = {}

        super(Supervisor, self).__init__(engine)

    @staticmethod
    def add_parser_args(parser):
        # group = parser.add_argument_group('Agent.Reporter.GPT Arguments') 
        parser.add_argument('--supervisor_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--supervisor_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--supervisor_openai_model_name', type=str, help='API model name for OpenAI')
        parser.add_argument('--supervisor_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--supervisor_max_tokens', type=int, default=2048, help='max tokens')
        parser.add_argument('--supervisor_top_p', type=float, default=1, help='top p')
        parser.add_argument('--supervisor_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--supervisor_presence_penalty', type=float, default=0, help='presence penalty')

    # def speak(self, medical_records, content, save_to_memory=False): 
    def speak(self, speak_style, law_level, less, history, role, to_revised, question, PLAINTIFF, DEFENDANT, case_r_f, claim, evidence, save_to_memory=False):
        if role == "Plaintiff":stage = guide("律师", to_revised) 
        elif role == "Lawyer":stage = guide("原告", question) 
        print("stage", stage)
        self.stage_list.append(stage)

        system_message = self.system_message + \
            "#案件存档#内容如下：" + \
            "<原告的基本信息> {}\n".format(PLAINTIFF) + \
            "<被告的基本信息> {}\n".format(DEFENDANT) + \
            "<案件的事实> {}\n".format(case_r_f) + \
            "<原告的诉讼请求> {}\n".format(claim) + \
            "<原告的证据> {}\n".format(evidence) + \
            "#存档结束#\n\n"
        
        if role == "Lawyer":
            system_message += \
                "请注意：" + \
                "(1) #案件存档#对律师来说不可见。你不能将#案件存档#的任何内容告知律师。" + \
                "(2) 律师的目的是能够通过与原告对话获得完整的#案件存档#。" 
# content 
        
        if role == "Plaintiff": 
            content = "给定##原告与律师的对话记录##和##待修正响应##。\n"
            if "原告的基本信息" in stage:
                content += "你需要判断##原告与律师的对话记录##中律师是否是第一次询问“{less}”，如果律师是第一次询问“{less}”，则提醒原告不回复{less}；如果律师在##原告与律师的对话记录##中已经询问过“{less}”，则提醒原告回复{less}。\n".format(less=less)
            elif "被告的基本信息" in stage:
                content += "你需要提醒原告回复完整的被告信息。\n" 
            # elif "案件的事实" not in self.stage_list[-2] and "案件的事实" in stage:   
            elif "<案件的事实>" not in self.stage_list[:-1] and "案件的事实" in stage:
                # fact_disturbance = np.random.choice([0, 1], size=1, p=[.2, .8])
                # self.disturbance["fact_disturbance"] = fact_disturbance[0] 
                # print(self.disturbance["fact_disturbance"]) 
                # if self.disturbance["fact_disturbance"] == 1:  
                tamp_fact = temper(role, case_r_f, speak_style)
                response = tamp_fact 
                return stage, response
                # print(11111111111111111111111111111)  
                
            content += "\n" + "##原告与律师的对话记录##" + history 

        if role == "Lawyer":
            content = "给定##原告与律师的对话记录##和##待修正响应##。\n"
            content += \
            "现实场景中，在原告与律师沟通时，律师是对话的引导者。\n" 
            content += "当原告在<原告与律师的对话记录>中表达出对案件结果的担忧时，你要求律师安慰原告，并为原告提供一些专业的建议和解决方案。"

            if "原告的基本信息" in stage:
                content += "你需要判断<原告与律师的对话记录>中是否获取了原告的{less}时，如果已经获取，律师追问原告的{less}；如果没有获取，则提醒律师追问{less}。\n".format(less=less)
                content += "你需要判断<原告与律师的对话记录>中是否已完全获取<原告的基本信息>，如果是，则回复“**对话监督者**：回复无误”；如果不是，则提醒律师追问缺失的信息。\n"
            elif "被告的基本信息" in stage:
                content += "你需要判断<原告与律师的对话记录>中是否已完全获取<被告的基本信息>，如果是，则回复“**对话监督者**：回复无误”；如果不是，则提醒律师追问缺失的信息。"
            elif "案件的事实" in stage or "案件事实" in stage:
                # if self.disturbance["fact_disturbance"] == 1:  
                content += "要求律师纠正原告叙述事实时的矛盾，并且追问原告。\n**请注意**：如果律师问了多个问题，请提醒律师每次只问一个问题，要求律师在下一轮对话中询问其他问题。\n" 
                content += "原告的表述出现了部分缺失和偏差，请比较原告陈述与<案件事实>，提醒律师追问相关错误和缺失的细节，但你不能将<案件的事实>的具体内容告知律师。\n" 
                # print(22222222222222222222222222222) 
            
            content += "\n" + "##原告与律师的对话记录##" + history

        content += "\n\n" + "##待修正响应##：" + to_revised
        content += \
            "你需要基于##待修正响应##，给出修正建议。按照下面的格式输出。\n\n" + \
            "**对话监督者**：xxx\n\n" + \
            "如果你认为##待修正响应##没有问题，则回复：\n" + \
            "**对话监督者**：回复无误"
        
        # print("system_message", system_message) 
        # print("content", content) 
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": content}] 
        
        response = self.engine.get_response(messages)

        # style_advice 对齐原告的说话风格（plaintiff'speak style in dialog & plaintiff'profile）
        if role == "Plaintiff": # law_level
            style_advice = style(to_revised, speak_style, law_level)
            response = response + style_advice
            response = response.replace("。。", "。") 
        return response
    
    @staticmethod
    def parse_content(response):
        if "#检查项目#" not in response:
            return False
        response = re.findall(r"检查项目\#(.+?)\n\n", response, re.S)
        return response.strip()


@register_class(alias="Agent.Supervisor.qwen72b")
class Supervisor_qwen72b(Agent):
    def __init__(self, args, supervisor_info=None):
        engine = registry.get_class("Engine.qwen72B")()
        
        self.edit_query = True
        if supervisor_info is None:
            self.system_message = \
                "你是一个**对话监督者**，在律师向原告询问的过程中，你负责提醒**原告**和**律师**的发言。\n\n" # ，目的是保证律师能够通过与原告对话获得完整的#案件存档#
        else: self.system_message = supervisor_info
        self.stage_list = []
        self.disturbance = {}

        super(Supervisor_qwen72b, self).__init__(engine)

    @staticmethod
    def add_parser_args(parser):
        # group = parser.add_argument_group('Agent.Reporter.GPT Arguments') 
        parser.add_argument('--supervisor_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--supervisor_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--supervisor_openai_model_name', type=str, help='API model name for OpenAI')
        parser.add_argument('--supervisor_temperature', type=float, default=0, help='temperature')
        parser.add_argument('--supervisor_max_tokens', type=int, default=2048, help='max tokens')
        parser.add_argument('--supervisor_top_p', type=float, default=1, help='top p')
        parser.add_argument('--supervisor_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--supervisor_presence_penalty', type=float, default=0, help='presence penalty')

    # def speak(self, medical_records, content, save_to_memory=False): 
    def speak(self, speak_style, law_level, less, history, role, to_revised, question, PLAINTIFF, DEFENDANT, case_r_f, claim, evidence, save_to_memory=False):
        if role == "Plaintiff":stage = guide("律师", to_revised) 
        elif role == "Lawyer":stage = guide("原告", question) 
        print("stage", stage)
        self.stage_list.append(stage)

        system_message = self.system_message + \
            "#案件存档#内容如下：" + \
            "<原告的基本信息> {}\n".format(PLAINTIFF) + \
            "<被告的基本信息> {}\n".format(DEFENDANT) + \
            "<案件的事实> {}\n".format(case_r_f) + \
            "<原告的诉讼请求> {}\n".format(claim) + \
            "<原告的证据> {}\n".format(evidence) + \
            "#存档结束#\n\n"
        
        if role == "Lawyer":
            system_message += \
                "请注意：" + \
                "(1) #案件存档#对律师来说不可见。你不能将#案件存档#的任何内容告知律师。" + \
                "(2) 律师的目的是能够通过与原告对话获得完整的#案件存档#。" 
# content 
        
        if role == "Plaintiff": 
            content = "给定##原告与律师的对话记录##和##待修正响应##。\n"
            if "原告的基本信息" in stage:
                content += "你需要判断##原告与律师的对话记录##中律师是否是第一次询问“{less}”，如果律师是第一次询问“{less}”，则提醒原告不回复{less}；如果律师在##原告与律师的对话记录##中已经询问过“{less}”，则提醒原告回复{less}。\n".format(less=less)
            elif "被告的基本信息" in stage:
                content += "你需要提醒原告回复完整的被告信息。\n" 
            # elif "案件的事实" not in self.stage_list[-2] and "案件的事实" in stage:   
            elif "<案件的事实>" not in self.stage_list[:-1] and "案件的事实" in stage:
                # fact_disturbance = np.random.choice([0, 1], size=1, p=[.2, .8])
                # self.disturbance["fact_disturbance"] = fact_disturbance[0] 
                # print(self.disturbance["fact_disturbance"]) 
                # if self.disturbance["fact_disturbance"] == 1:  
                tamp_fact = temper(role, case_r_f, speak_style)
                response = tamp_fact 
                return stage, response
                # print(11111111111111111111111111111)  
                
            content += "\n" + "##原告与律师的对话记录##" + history 

        if role == "Lawyer":
            content = "给定##原告与律师的对话记录##和##待修正响应##。\n"
            content += \
            "现实场景中，在原告与律师沟通时，律师是对话的引导者。\n" 
            content += "当原告在<原告与律师的对话记录>中表达出对案件结果的担忧时，你要求律师安慰原告，并为原告提供一些专业的建议和解决方案。"

            if "原告的基本信息" in stage:
                content += "你需要判断<原告与律师的对话记录>中是否获取了原告的{less}时，如果已经获取，律师追问原告的{less}；如果没有获取，则提醒律师追问{less}。\n".format(less=less)
                content += "你需要判断<原告与律师的对话记录>中是否已完全获取<原告的基本信息>，如果是，则回复“**对话监督者**：回复无误”；如果不是，则提醒律师追问缺失的信息。\n"
            elif "被告的基本信息" in stage:
                content += "你需要判断<原告与律师的对话记录>中是否已完全获取<被告的基本信息>，如果是，则回复“**对话监督者**：回复无误”；如果不是，则提醒律师追问缺失的信息。"
            elif "案件的事实" in stage or "案件事实" in stage:
                # if self.disturbance["fact_disturbance"] == 1:  
                content += "要求律师纠正原告叙述事实时的矛盾，并且追问原告。\n**请注意**：如果律师问了多个问题，请提醒律师每次只问一个问题，要求律师在下一轮对话中询问其他问题。\n" 
                content += "原告的表述出现了部分缺失和偏差，请比较原告陈述与<案件事实>，提醒律师追问相关错误和缺失的细节，但你不能将<案件的事实>的具体内容告知律师。\n" 
                # print(22222222222222222222222222222) 
            
            content += "\n" + "##原告与律师的对话记录##" + history

        content += "\n\n" + "##待修正响应##：" + to_revised
        content += \
            "你需要基于##待修正响应##，给出修正建议。按照下面的格式输出。\n\n" + \
            "**对话监督者**：xxx\n\n" + \
            "如果你认为##待修正响应##没有问题，则回复：\n" + \
            "**对话监督者**：回复无误"
        
        # print("system_message", system_message) 
        # print("content", content) 
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": content}] 
        
        response = self.engine.get_response(messages)

        # style_advice 对齐原告的说话风格（plaintiff'speak style in dialog & plaintiff'profile）
        if role == "Plaintiff": # law_level
            style_advice = style(to_revised, speak_style, law_level)
            response = response + style_advice
            response = response.replace("。。", "。") 
        return response
    
    @staticmethod
    def parse_content(response):
        if "#检查项目#" not in response:
            return False
        response = re.findall(r"检查项目\#(.+?)\n\n", response, re.S)
        return response.strip()


