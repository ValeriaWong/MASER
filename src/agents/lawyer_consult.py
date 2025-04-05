from .base_agent import Agent
from utils.register import register_class, registry

@register_class(alias="Agent.Lawyer.ConsultGPT")
class Lawyer_consult(Agent):
    def __init__(self, args):
        engine = registry.get_class("Engine.GPT")(
            openai_api_key=args.lawyer_openai_api_key,
            openai_api_base=args.lawyer_openai_api_base,
            openai_model_name=args.lawyer_openai_model_name,
            temperature=args.lawyer_temperature,
            max_tokens=args.lawyer_max_tokens,
            top_p=args.lawyer_top_p,
            frequency_penalty=args.lawyer_frequency_penalty,
            presence_penalty=args.lawyer_presence_penalty
        )
        super(Lawyer_consult, self).__init__(engine)

class HFLawyer_consult: pass
class QwenLawyer_consult: pass
class GPTLawyer_consult: pass
class MinimaxLawyer_consult: pass
class WenXinLawyer_consult: pass
class ChatGLMLawyer_consult: pass
class HuatuoGPTLawyer_consult: pass
