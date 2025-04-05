from .base_agent import Agent
from utils.register import register_class

@register_class(alias="Agent.Lawyer.FactEvalGPT")
class Lawyer_fact_evaluate(Agent):
    def __init__(self, args):
        super().__init__(engine=None)  # Placeholder

class GPTLawyer_fact_evaluate: pass
class BaichuanLawyer_fact_evaluate: pass
class DISCv1Lawyer_fact_evaluate: pass
class FuzimingChaLawyer_fact_evaluate: pass
class ChatGLMLawyer_fact_evaluate: pass
class QwenLawyer_fact_evaluate: pass
class Qwentrained_Lawyer_fact_evaluate: pass
class LLaMaLawyer_fact_evaluate: pass
class lawyerllamaLawyer_fact_evaluate: pass
class wisdomILawyer_fact_evaluate: pass
class MistralLawyer_fact_evaluate: pass
class InternLawyer_fact_evaluate: pass
class Qwen72BLawyer_fact_evaluate: pass
