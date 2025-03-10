from .base_agent import Agent
from utils.register import register_class, registry

@register_class(alias="Agent.Plaintiff.FactGPT")
class Plaintiff_fact(Agent):
    def __init__(self, args, id, plaintiff_type, reason, laws, case_r_f, plaintiff,defendant,claim,evidence,less,law_level,personality,speak_style): 
        engine = registry.get_class("Engine.GPT")(
            openai_api_key=args.plaintiff_openai_api_key,
            openai_api_base=args.plaintiff_openai_api_base,
            openai_model_name=args.plaintiff_openai_model_name,
            temperature=args.plaintiff_temperature,
            max_tokens=args.plaintiff_max_tokens,
            top_p=args.plaintiff_top_p,
            frequency_penalty=args.plaintiff_frequency_penalty,
            presence_penalty=args.plaintiff_presence_penalty)

        if plaintiff_type == "company":self.system_message = "你是公司的法定代表人，你代表公司与律师沟通。你需要遵循以下的设定。\n" 
        elif plaintiff_type == "personal":self.system_message = "你是案件的原告，你需要遵循以下的原告人物设定。\n" 
        
        self.system_message += "#人物设定#：\n"
        self.system_message += "<基本信息>{}\n".format(plaintiff) 
        self.system_message += "<懂法程度> {}\n".format(law_level)
        self.system_message += "<性格特点> {}\n".format(personality) # personality 
        self.system_message += "<说话语气特点> {}\n".format(speak_style["tone"])
        self.system_message += "<说话内容特点> {}\n".format(speak_style["content"])
        self.system_message += "<互动行为特点> {}\n\n".format(speak_style["interaction"])

        self.system_message += "#案件信息#：\n"
        self.system_message += "<你的诉求> {}\n".format(claim["非诉讼费用内容"].strip())
        self.system_message += "<诉讼费用> {}\n".format(claim["诉讼费用内容"].strip())
        # print(id) 
        self.system_message += "<事实与理由> {}\n".format(case_r_f)
        self.system_message += "<被告信息> {}\n".format(defendant)
        # if "原告" in evidence.keys():
        # print(id)
        self.system_message += "<你的证据> {}\n".format(evidence["原告"])
        self.system_message += "\n"

        self.system_message += \
            "现在你的律师代理人需要向你收集案件相关的信息，你需要：\n" + \
            "(1) 回复时需要以第一人称模拟给定的<说话语气特点>、<说话内容特点>、<互动行为特点>和<懂法程度>，不能直接复述给定的基本信息和案件信息。\n" + \
            "(2) 你在回答诉讼请求时，不需要回复“诉讼费用”。\n"+ \
            "(3) 你需要根据**对话监督者**的建议修改**待修正响应**，输出**修正后响应**。\n" + \
            "(4) 如果被告是公司，你需要完整的提供公司名称、地址、负责人或法定代表人。如果被告是个人你需要完整的提供姓名、性别、出生日期、民族、地址。\n"+ \
            "(5) 当律师的回复中有特殊字符<询问结束>，意味着律师对你询问结束。"
            
            # "(2) 在描述案件事实的时候，你不需要一次性的把<事实与理由>全说出来，需要在律师的引导下逐步将<事实与理由>描述得清楚、完整。\n" + \
          # "(7) 当<律师>起草起诉书后，请确认起诉状的内容是否准确。如果有需要添加或修改的部分需主动告知律师，待律师修改正确后在对话的末尾加上特殊字符<结束>；如果没有需要添加或修改的部分，在对话的末尾加上特殊字符<结束>。"

        super(Plaintiff_fact, self).__init__(engine)
        # case_type=None, case_facts=None, case_r_f=None, plaintiff=None, less=None, law_level=None, defendant=None, claim=None, evidence=None
        self.id = id
        self.plaintiff = plaintiff
        self.law_level = law_level
        self.speak_style = speak_style
        self.personality = personality
        self.less = less

        self.case_r_f = case_r_f
        self.defendant = defendant
        self.claim = claim
        self.evidence = evidence
        self.plaintiff_type = plaintiff_type
        self.reason = reason
        self.laws = laws
        
        self.plaintiff_greet = "您好，我想写一份起诉状。"
        # self.medical_records = medical_records

    @staticmethod
    def add_parser_args(parser):
        # group = parser.add_argument_group('Agent.Plaintiff.GPT Arguments')
        parser.add_argument('--plaintiff_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--plaintiff_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--plaintiff_openai_model_name', type=str, help='API model name for OpenAI')
        parser.add_argument('--plaintiff_temperature', type=float, default=0.5, help='temperature')
        parser.add_argument('--plaintiff_max_tokens', type=int, default=2048, help='max tokens')
        parser.add_argument('--plaintiff_top_p', type=float, default=1, help='top p')
        parser.add_argument('--plaintiff_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--plaintiff_presence_penalty', type=float, default=0, help='presence penalty')

    def speak(self, role, content, save_to_memory=True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        # content = f"<{role}> {content}"
        messages.append({"role": "user", "content": content})
        
        responese = self.engine.get_response(messages)
        if save_to_memory:
            self.memorize(("user", content))
            self.memorize(("assistant", responese))
        return responese
        
    def correct_speak(self, advice, false_reply, content, save_to_memory=False):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        
        if save_to_memory:self.memorize(("user", content))
        # content = f"<{role}> {content}"   
        # content = f"**律师**： {content}" + "\n" #**Lawyer**：  
        content += f"**对话监督者**： {advice}" + "\n" #**对话监督者**：  
        content += f"##待修正响应##： {false_reply}" + "\n" ###待修正响应##：  
        content += "##修正后响应##： \n"   
        # print("content",content) 

        messages.append({"role": "user", "content": content})
        
        responese = self.engine.get_response(messages)

        if save_to_memory:self.memorize(("assistant", responese))
        return responese
    
    @staticmethod
    def parse_role_content(responese):
        responese = responese.strip()
        # if responese.startswith("<对医生讲>"):
        #     speak_to = "医生"
        # elif responese.startswith("<对检查员讲>"):
        #     speak_to = "检查员"
        # else:
        #     speak_to = "医生"
        # if responese.startswith("<对律师讲>"):
        #     speak_to = "律师"
        # else:
        #     raise Exception("Response of PlaintiffAgent must start with '<对律师讲>', but current repsonse is: {}".format(responese))
        speak_to = "律师"
        # responese = responese.replace("<对律师讲>", "").strip()

        return speak_to, responese



@register_class(alias="Agent.Plaintiff.Factqwen72b")
class Plaintiffqwen72b_fact(Agent):
    def __init__(self, args, id, plaintiff_type, reason, laws, case_r_f, plaintiff,defendant,claim,evidence,less,law_level,personality,speak_style): 
        engine = registry.get_class("Engine.qwen72B")()

        if plaintiff_type == "company":self.system_message = "你是公司的法定代表人，你代表公司与律师沟通。你需要遵循以下的设定。\n" 
        elif plaintiff_type == "personal":self.system_message = "你是案件的原告，你需要遵循以下的原告人物设定。\n" 
        
        self.system_message += "#人物设定#：\n"
        self.system_message += "<基本信息>{}\n".format(plaintiff) 
        self.system_message += "<懂法程度> {}\n".format(law_level)
        self.system_message += "<性格特点> {}\n".format(personality) # personality 
        self.system_message += "<说话语气特点> {}\n".format(speak_style["tone"])
        self.system_message += "<说话内容特点> {}\n".format(speak_style["content"])
        self.system_message += "<互动行为特点> {}\n\n".format(speak_style["interaction"])

        self.system_message += "#案件信息#：\n"
        self.system_message += "<你的诉求> {}\n".format(claim["非诉讼费用内容"].strip())
        self.system_message += "<诉讼费用> {}\n".format(claim["诉讼费用内容"].strip())
        # print(id) 
        self.system_message += "<事实与理由> {}\n".format(case_r_f)
        self.system_message += "<被告信息> {}\n".format(defendant)
        # if "原告" in evidence.keys():
        # print(id)
        self.system_message += "<你的证据> {}\n".format(evidence["原告"])
        self.system_message += "\n"

        self.system_message += \
            "现在你的律师代理人需要向你收集案件相关的信息，你需要：\n" + \
            "(1) 回复时需要以第一人称模拟给定的<说话语气特点>、<说话内容特点>、<互动行为特点>和<懂法程度>，不能直接复述给定的基本信息和案件信息。\n" + \
            "(3) 你在回答诉讼请求时，不需要回复“诉讼费用”。\n"+ \
            "(4) 你需要根据**对话监督者**的建议修改**待修正响应**，输出**修正后响应**。\n" + \
            "(5) 如果被告是公司，你需要完整的提供公司名称、地址、负责人或法定代表人。如果被告是个人你需要完整的提供姓名、性别、出生日期、民族、地址。\n"+ \
            "(6) 当律师的回复中有特殊字符<询问结束>，意味着律师对你询问结束。"
            
            # "(2) 在描述案件事实的时候，你不需要一次性的把<事实与理由>全说出来，需要在律师的引导下逐步将<事实与理由>描述得清楚、完整。\n" + \
          # "(7) 当<律师>起草起诉书后，请确认起诉状的内容是否准确。如果有需要添加或修改的部分需主动告知律师，待律师修改正确后在对话的末尾加上特殊字符<结束>；如果没有需要添加或修改的部分，在对话的末尾加上特殊字符<结束>。"


        super(Plaintiffqwen72b_fact, self).__init__(engine)
        # case_type=None, case_facts=None, case_r_f=None, plaintiff=None, less=None, law_level=None, defendant=None, claim=None, evidence=None
        self.id = id
        self.plaintiff = plaintiff
        self.law_level = law_level
        self.speak_style = speak_style
        self.personality = personality
        self.less = less

        self.case_r_f = case_r_f
        self.defendant = defendant
        self.claim = claim
        self.evidence = evidence
        self.plaintiff_type = plaintiff_type
        self.reason = reason
        self.laws = laws
        
        self.plaintiff_greet = "您好，我想写一份起诉状。"
        # self.medical_records = medical_records

    @staticmethod
    def add_parser_args(parser):
        # group = parser.add_argument_group('Agent.Plaintiff.GPT Arguments')
        parser.add_argument('--plaintiff_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--plaintiff_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--plaintiff_openai_model_name', type=str, help='API model name for OpenAI')
        parser.add_argument('--plaintiff_temperature', type=float, default=0.5, help='temperature')
        parser.add_argument('--plaintiff_max_tokens', type=int, default=2048, help='max tokens')
        parser.add_argument('--plaintiff_top_p', type=float, default=1, help='top p')
        parser.add_argument('--plaintiff_frequency_penalty', type=float, default=0, help='frequency penalty')
        parser.add_argument('--plaintiff_presence_penalty', type=float, default=0, help='presence penalty')

    def speak(self, role, content, save_to_memory=True):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        # content = f"<{role}> {content}"
        messages.append({"role": "user", "content": content})
        
        responese = self.engine.get_response(messages)
        if save_to_memory:
            self.memorize(("user", content))
            self.memorize(("assistant", responese))
        return responese
        
    def correct_speak(self, advice, false_reply, content, save_to_memory=False):
        messages = [{"role": memory[0], "content": memory[1]} for memory in self.memories]
        
        if save_to_memory:self.memorize(("user", content))
        # content = f"<{role}> {content}"   
        # content = f"**律师**： {content}" + "\n" #**Lawyer**：  
        content += f"**对话监督者**： {advice}" + "\n" #**对话监督者**：  
        content += f"##待修正响应##： {false_reply}" + "\n" ###待修正响应##：  
        content += "##修正后响应##： \n"   
        # print("content",content) 

        messages.append({"role": "user", "content": content})
        
        responese = self.engine.get_response(messages)

        if save_to_memory:self.memorize(("assistant", responese))
        return responese
    
    @staticmethod
    def parse_role_content(responese):
        responese = responese.strip()
        # if responese.startswith("<对医生讲>"):
        #     speak_to = "医生"
        # elif responese.startswith("<对检查员讲>"):
        #     speak_to = "检查员"
        # else:
        #     speak_to = "医生"
        # if responese.startswith("<对律师讲>"):
        #     speak_to = "律师"
        # else:
        #     raise Exception("Response of PlaintiffAgent must start with '<对律师讲>', but current repsonse is: {}".format(responese))
        speak_to = "律师"
        # responese = responese.replace("<对律师讲>", "").strip()

        return speak_to, responese
