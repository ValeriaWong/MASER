from .base_agent import Agent
from utils.register import register_class

@register_class(alias="Agent.Defendant.DebateGPT")
class Defendant_debate(Agent):
    def __init__(self, args):
        super().__init__(engine=None)
