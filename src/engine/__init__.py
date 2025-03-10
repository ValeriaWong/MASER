# 注册不同的Engine
from .base_engine import Engine
from .gpt import GPTEngine
from .baichuan2 import BaichuanEngine
from .chatglm import ChatGLMEngine
from .minimax import MiniMaxEngine
from .wenxin import WenXinEngine
from .qwen import QwenEngine
from .qwen_trained import QwentrainedEngine
from .huatuogpt import HuatuoGPTEngine
from .hf import HFEngine
from .InternLM import InternLM
from .LLaMa31 import LLaMa
from .Mistral7b import Mistral

from .wisdomInterrogatory import wisdomInterrogatory
from .LawLLM import DISC_v1
from .fuzimingcha import FuzimingCha 
from .hanfei import hanfei
from .qwen72B import qwen72Engine

__all__ = [
    "Engine",
    "GPTEngine",
    "ChatGLMEngine",
    "MiniMaxEngine",
    "WenXinEngine",
    "QwenEngine",
    "QwentrainedEngine",
    "HuatuoGPTEngine",
    "HFEngine",
    "BaichuanEngine",
    "InternLM",
    "lawyer",
    "LLaMa",
    "Mistral",
    "wisdomInterrogatory",
    "DISC_v1",
    "FuzimingCha",
    "hanfei",
    "qwen72Engine"
]



