from .base_agent import Agent
from utils.register import register_class, registry

@register_class(alias="Agent.Plaintiff.ConsultGPT")
class Plaintiff_consult(Agent):
    def __init__(self, args):
        engine = registry.get_class("Engine.GPT")(
            openai_api_key=args.plaintiff_openai_api_key,
            openai_api_base=args.plaintiff_openai_api_base,
            openai_model_name=args.plaintiff_openai_model_name,
            temperature=args.plaintiff_temperature,
            max_tokens=args.plaintiff_max_tokens,
            top_p=args.plaintiff_top_p,
            frequency_penalty=args.plaintiff_frequency_penalty,
            presence_penalty=args.plaintiff_presence_penalty
        )
        super(Plaintiff_consult, self).__init__(engine)

    @staticmethod
    def add_parser_args(parser):
        parser.add_argument('--plaintiff_openai_api_key', type=str, help='API key for OpenAI')
        parser.add_argument('--plaintiff_openai_api_base', type=str, help='API base for OpenAI')
        parser.add_argument('--plaintiff_openai_model_name', type=str, help='Model name for OpenAI')
        parser.add_argument('--plaintiff_temperature', type=float, default=0.7, help='Temperature')
        parser.add_argument('--plaintiff_max_tokens', type=int, default=1024, help='Max tokens')
        parser.add_argument('--plaintiff_top_p', type=float, default=1.0, help='Top-p')
        parser.add_argument('--plaintiff_frequency_penalty', type=float, default=0.0, help='Frequency penalty')
        parser.add_argument('--plaintiff_presence_penalty', type=float, default=0.0, help='Presence penalty')
