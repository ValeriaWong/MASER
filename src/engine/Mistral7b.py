from transformers import pipeline
from abc import abstractmethod
from .base_engine import Engine
from utils.register import register_class, registry

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams
import torch,time


# @register_class(alias="Engine.Mistral")
# class Mistral(Engine):
#     def __init__(self):        
#         self.model_path = "/attached/remote-home/source/DISC-LawLLM-v2/Model/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3"
#         self.chatbot = pipeline("text-generation", model=self.model_path, max_new_tokens=384)

#     def get_response(self, messages):
#         response = self.chatbot(messages)
#         return response[0]['generated_text'][-1]['content']


@register_class(alias="Engine.Mistral")
class Mistral(Engine):
    def __init__(self):
        self.model_path = "/attached/remote-home/source/DISC-LawLLM-v2/Model/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.sampling_params = SamplingParams(temperature=0, max_tokens=1536)
        self.llm = LLM(model = self.model_path, dtype = torch.float16)

    def get_response(self, messages):
        retry = 0 
        while retry < 5:
            try:
                text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                outputs = self.llm.generate([text], self.sampling_params)
                for output in outputs: # prompt = output.prompt
                    generated_text = output.outputs[0].text # print(f"Generated text: {generated_text!r}")
                    response = generated_text
                return response
            except Exception as e:
                print(f"Error occurred: {e}")
                retry += 1
                time.sleep(10)