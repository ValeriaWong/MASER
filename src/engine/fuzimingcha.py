from transformers import AutoTokenizer, AutoModel
from abc import abstractmethod
import time
from .base_engine import Engine
from utils.register import register_class, registry


@register_class(alias="Engine.FuzimingCha")
class FuzimingCha(Engine):
    def __init__(self): 
        self.model_path = "/attached/remote-home/source/DISC-LawLLM-v2/Model/fuzi-mingcha/fuzi-mingcha-v1_0"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(self.model_path, trust_remote_code=True).half().cuda()

    def get_response(self, messages):
        retry = 0
        while retry < 5:
            try:
                prompt = messages[-1]['content']
                history = [message for message in messages[1:-1]]
                print("prompt: ", prompt)
                print("history: ", history)
                response = self.model.chat(self.tokenizer, prompt, history=history)
                ### probably cause CUDA out of Memory  ########

                return response[0]
            except Exception as e:
                print(f"Error occurred: {e}")
                retry += 1
                time.sleep(10)
