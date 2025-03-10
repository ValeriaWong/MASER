import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig

from .base_engine import Engine
from utils.register import register_class, registry
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams
import torch,time

@register_class(alias="Engine.Baichuan2")
class BaichuanEngine(Engine):
    def __init__(self, version):
        self.ver = {'13b': 'Baichuan2-13B-Chat', '7b': 'Baichuan2-7B-Chat'}[version]
        self.model_path = f'/attached/remote-home/source/DISC-LawLLM-v2/Model/Baichuan2-Chat/{self.ver}'
        # self.model_path = "/root/model/Mistral-7B-v02" 
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path,
                                                       trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path,
                                                          device_map="auto",
                                                          torch_dtype=torch.float16,
                                                          trust_remote_code=True)
        self.model.generation_config = GenerationConfig.from_pretrained(self.model_path, revision="v2.0")

    def get_response(self, messages):
        print(messages)
        response = self.model.chat(self.tokenizer, messages)
        torch.cuda.empty_cache()
        return response



# @register_class(alias="Engine.Baichuan2")
# class BaichuanEngine(Engine):
#     def __init__(self, version):
#         self.ver = {'13b': 'Baichuan2-13B-Chat', '7b': 'Baichuan2-7B-Chat'}[version]
#         self.model_path = f'/attached/remote-home/source/DISC-LawLLM-v2/Model/Baichuan2-Chat/{self.ver}'

#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True) 
#         self.sampling_params = SamplingParams(temperature=0, max_tokens=512)
#         self.llm = LLM(model = self.model_path, dtype = torch.float16, trust_remote_code=True)

#     @torch.inference_mode() 
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



