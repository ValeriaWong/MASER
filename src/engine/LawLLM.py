from abc import abstractmethod
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from .base_engine import Engine
from utils.register import register_class
from vllm import LLM, SamplingParams
import time


@register_class(alias="Engine.DISCv1")
class DISC_v1(Engine):
    def __init__(self):
        #self.messages = [] 
        self.model_path = "/attached/remote-home/source/DISC-LawLLM-v2/Model/LawLLM-chat"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, use_fast = False, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
        self.model.generation_config = GenerationConfig.from_pretrained(self.model_path)

    def get_response(self, messages):
        print(messages)
        messages[1]["content"] = "system prompt:" + messages[0]["content"] + "\n\n" + "user:" + messages[1]["content"]
        del messages[0]
        # print("message为：——————————————————", messages)

        retry = 0
        st = time.time()
        while retry < 5:
            try:
                response = self.model.chat(self.tokenizer, messages)
                torch.cuda.empty_cache()
                return response
            except Exception as e:
                print(f"Error occurred: {e}")
                retry += 1
                time.sleep(10)
        print(time.time-st)



# @register_class(alias="Engine.DISCv1")
# class DISC_v1(Engine):
#     def __init__(self):
#         #self.messages = []
#         self.model_path = "/remote-home/share/DISC-LawLLM-v2/Model/LawLLM-chat"
#         # self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, use_fast = False, trust_remote_code=True)
#         # self.model = AutoModelForCausalLM.from_pretrained(self.model_path, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
#         # self.model.generation_config = GenerationConfig.from_pretrained(self.model_path)
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
#         self.sampling_params = SamplingParams(temperature=0.0, max_tokens=512)
#         self.llm = LLM(model=self.model_path, dtype = torch.float16, trust_remote_code=True, gpu_memory_utilization=0.9, max_model_len=3072)


#     def get_response(self, messages):
#         retry = 0
#         st = time.time()
#         text =  self.tokenizer.apply_chat_template(
#         messages,
#             tokenize=False,
#             add_generation_prompt=True)
#         response = self.llm.generate([text], self.sampling_params)
#         for output in response:
#             # prompt = output.prompt
#             generated_text = output.outputs[0].text
#         # response = self.model.chat(self.tokenizer, messages)
#         print(time.time-st)
#         return generated_text

