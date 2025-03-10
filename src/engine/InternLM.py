from transformers import AutoTokenizer, AutoModelForCausalLM
from abc import abstractmethod
from .base_engine import Engine
from utils.register import register_class, registry

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams
import torch,time

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
@register_class(alias="Engine.Intern")
class InternLM(Engine):
    def __init__(self):
        self.model_path = '/attached/remote-home/source/DISC-LawLLM-v2/Model/InternLM2/internlm2_5-7b-chat'
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path, torch_dtype=torch.float16, trust_remote_code=True).cuda().eval()
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)

    def get_response(self, messages):
        user_input = messages[-1]["content"] 
        system_prompt = messages[0]["content"]

        history = []
        for i in range(1, len(messages), 2):
            if i <= len(messages)-3:
                history.append((messages[i]["content"],messages[i+1]["content"]))
        response, _ = self.model.chat(self.tokenizer, query=user_input, history = history, meta_instruction = system_prompt,max_new_tokens=1024)
        return response


# @register_class(alias="Engine.Intern")
# class InternLM(Engine):
#     def __init__(self):
#         self.model_path = "/attached/remote-home/source/DISC-LawLLM-v2/Model/InternLM2/internlm2_5-7b-chat"
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
#         self.sampling_params = SamplingParams(temperature=0, max_tokens=512)
#         self.llm = LLM(model = self.model_path, dtype = torch.float16, trust_remote_code=True)

#     def get_response(self, messages):
#         retry = 0 
#         while retry < 5:
#             try:
#                 text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
#                 outputs = self.llm.generate([text], self.sampling_params)
#                 for output in outputs: # prompt = output.prompt
#                     generated_text = output.outputs[0].text # print(f"Generated text: {generated_text!r}")
#                     response = generated_text
#                 return response
#             except Exception as e:
#                 print(f"Error occurred: {e}")
#                 retry += 1
#                 time.sleep(10)
