from .base_agent import Agent
# from .doctor import (
#     Doctor, 
#     GPTDoctor, 
#     ChatGLMDoctor, 
#     MinimaxDoctor, 
#     WenXinDoctor, 
#     QwenDoctor, 
#     HuatuoGPTDoctor,
#     HFDoctor
# )
# from .patient import Patient
# from .reporter import Reporter, ReporterV2
# from .host import Host
# _________________分割线______________________
# _________________consult_____________________
from .plaintiff_consult import Plaintiff_consult
from .lawyer_consult import (
    Lawyer_consult,
    HFLawyer_consult,
    QwenLawyer_consult,
    GPTLawyer_consult,
    MinimaxLawyer_consult,
    WenXinLawyer_consult,
    ChatGLMLawyer_consult,
    HuatuoGPTLawyer_consult)

# _________________fact_____________________
from .plaintiff_fact import (Plaintiff_fact, Plaintiffqwen72b_fact)
from .supervisor import (Supervisor, Supervisor_qwen72b)

from .lawyer_fact import (
    Lawyer_fact,
    HFLawyer_fact,
    QwenLawyer_fact,
    GPTLawyer_fact,
    MinimaxLawyer_fact,
    WenXinLawyer_fact,
    ChatGLMLawyer_fact,
    HuatuoGPTLawyer_fact)

from .lawyer_fact_evaluate import (
    Lawyer_fact_evaluate,
    GPTLawyer_fact_evaluate,
    BaichuanLawyer_fact_evaluate,
    DISCv1Lawyer_fact_evaluate,
    FuzimingChaLawyer_fact_evaluate,
    ChatGLMLawyer_fact_evaluate,
    QwenLawyer_fact_evaluate,
    Qwentrained_Lawyer_fact_evaluate,
    LLaMaLawyer_fact_evaluate,
    lawyerllamaLawyer_fact_evaluate,
    wisdomILawyer_fact_evaluate,
    MistralLawyer_fact_evaluate,
    InternLawyer_fact_evaluate,
    Qwen72BLawyer_fact_evaluate)

# _________________debate_____________________
from .plaintiff_debate import Plaintiff_debate
from .defendant_debate import Defendant_debate
from .judge import (
    Judge,
    GPTJudge,
    ChatGLMJudge,
    MinimaxJudge,
    WenXinJudge,
    QwenJudge,
    HuatuoGPTJudge,
    HFJudge
)
__all__ = [
    "Agent",
    # "Doctor",
    # "GPTDoctor",
    # "ChatGLMDoctor",
    # "MinimaxDoctor",
    # "WenXinDoctor",
    # "QwenDoctor",
    # "HuatuoGPTDoctor",
    # "HFDoctor",
    # "Patient",
    # "Reporter",
    # "ReporterV2",
    # "Host",
    "Plaintiff_consult",
    "Lawyer_consult",
    "HFLawyer_consult",
    "QwenLawyer_consult",
    "GPTLawyer_consult",
    "MinimaxLawyer_consult",
    "WenXinLawyer_consult",
    "ChatGLMLawyer_consult",
    "HuatuoGPTLawyer_consult",
    "Plaintiff_fact",
    "Lawyer_fact",
    "HFLawyer_fact",
    "QwenLawyer_fact",
    "GPTLawyer_fact",
    "MinimaxLawyer_fact",
    "WenXinLawyer_fact",
    "ChatGLMLawyer_fact",
    "HuatuoGPTLawyer_fact",
    "Plaintiff_debate",
    "Defendant_debate",
    "Judge",
    "GPTJudge",
    "ChatGLMJudge",
    "MinimaxJudge",
    "WenXinJudge",
    "QwenJudge",
    "HuatuoGPTJudge",
    "HFJudge",
    "Supervisor",
    "Lawyer_fact_evaluate",
    "GPTLawyer_fact_evaluate",
    "BaichuanLawyer_fact_evaluate",
    "DISCv1Lawyer_fact_evaluate",
    "FuzimingChaLawyer_fact_evaluate",
    "ChatGLMLawyer_fact_evaluate",
    "QwenLawyer_fact_evaluate",
    "Qwentrained_Lawyer_fact_evaluate",
    "LLaMaLawyer_fact_evaluate",
    "lawyerllamaLawyer_fact_evaluate",
    "wisdomILawyer_fact_evaluate",
    "MistralLawyer_fact_evaluate",
    "InternLawyer_fact_evaluate",
    "Qwen72BLawyer_fact_evaluate",
    "Plaintiffqwen72b_fact",
    "Supervisor_qwen72b"
]



