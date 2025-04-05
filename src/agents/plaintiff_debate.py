from .base_agent import Agent
from utils.register import register_class

@register_class(alias="Agent.Plaintiff.DebateGPT")
class Plaintiff_debate(Agent):
    def __init__(self, args):
        super().__init__(engine=None)
