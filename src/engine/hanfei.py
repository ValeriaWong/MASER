import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
import torch
from abc import abstractmethod

from .base_engine import Engine
from utils.register import register_class, registry
import time

@register_class(alias="Engine.Hanfei")
class hanfei(Engine):
    def __init__(self):
        self.model_name = '/attached/remote-home/source/DISC-LawLLM-v2/Model/hanfei-1.0'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_mode=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

    def get_response(self, messages):
        retry = 0
        while retry < 5:
            try:
                input_text = "一位用户和法律大模型韩非之间的对话。对于用户的法律咨询，韩非给出准确的、详细的、温暖的指导建议。对于用户的指令问题，韩非给出有益的、详细的、有礼貌的回答。\n\n"
                pairs = [(messages[1:-1][i], messages[1:-1][i + 1]) for i in range(0, len(messages[:-1]) - 1, 2)]

                for pair in pairs:
                    human = pair[0]['content']
                    assistant = pair[1]['content']
                    input_text += f"用户：{human} 韩非：{assistant}"
                input_text += f"用户：{messages[-1]['content']} 韩非："
                print("input_text: " ,input_text, "\n\n\n\n")
                input_id = self.tokenizer([input_text], return_tensors="pt")
                outputs = self.model.generate(
                    input_id.input_ids,
                    max_new_tokens=1024,
                    temperature=0
                )
                response = self.tokenizer.decode(outputs[0])
                response = response.split('韩非：')[-1].replace("</s>","")
                if "用户" in response:
                    response = response.split("用户")[0]
                print("response: ", response, "\n\n\n")

                return response
            except Exception as e:
                print(f"Error occurred: {e}")
                retry += 1
                time.sleep(10)



