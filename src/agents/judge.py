from .base_agent import Agent
from utils.register import register_class

@register_class(alias="Agent.Judge.GPT")
class Judge(Agent):
    def __init__(self, args):
        super().__init__(engine=None)

class GPTJudge: pass
class ChatGLMJudge: pass
class MinimaxJudge: pass
class WenXinJudge: pass
class QwenJudge: pass
class HuatuoGPTJudge: pass
class HFJudge: pass
