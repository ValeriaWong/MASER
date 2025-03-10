from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import torch
from modelscope import AutoTokenizer as AT, AutoModelForCausalLM as AMC
from abc import abstractmethod
import time
from .base_engine import Engine
from utils.register import register_class, registry

@register_class(alias="Engine.wisdomI")
class wisdomInterrogatory(Engine):
    def __init__(self):
        self.model_path = '/attached/remote-home/source/DISC-LawLLM-v2/Model/zju_model_0813_100k'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path, device_map="auto",
                                                          torch_dtype=torch.float16,
                                                          trust_remote_code=True
                                                          )
        self.generation_config = {
            "temperature": 0,
            "max_new_tokens": 512
        }

    def get_response(self, messages):
        retry = 0
        while retry < 5:
            try:
                torch.cuda.empty_cache()

                input_text = ''
                pairs = [(messages[1:-1][i], messages[1:-1][i + 1]) for i in range(0, len(messages[:-1]) - 1, 2)]

                for pair in pairs:
                    human = pair[0]['content']
                    assistant = pair[1]['content']
                    input_text += f"</s>Human:{human} </s>Assistant: {assistant}"
                input_text += f"</s>Human:{messages[-1]['content']} </s>Assistant: "

                input_ids = self.tokenizer(input_text, return_tensors="pt").to("cuda")
                with torch.no_grad():
                    pred = self.model.generate(**input_ids, max_new_tokens=4096)
                response = self.tokenizer.decode(pred.cpu()[0], skip_special_tokens=True)

                return response.split("Assistant: ")[-1]
            except Exception as e:
                print(f"Error occurred: {e}")
                retry += 1
                time.sleep(10)


