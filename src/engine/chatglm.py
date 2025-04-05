# import zhipuai
# from .base_engine import Engine
# from utils.register import register_class
# from transformers import AutoModel, AutoTokenizer
# from abc import abstractmethod
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from transformers import AutoTokenizer
# from vllm import LLM, SamplingParams
# import torch,time

# @register_class(alias="Engine.ChatGLM")
# class ChatGLMEngine(Engine):
#     def __init__(self, temperature=0.1, *args, **kwargs):
#         self.model_path = "/attached/remote-home/source/DISC-LawLLM-v2/Model/ChatGLM3-6B/chatglm3-6b/"
#         self.temperature = temperature
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
#         self.model = AutoModel.from_pretrained(self.model_path, trust_remote_code=True).half().eval()
#         # self.history = []  # 维护对话历史

#     def get_response(self, messages):
#         user_input = messages[-1]["content"] 
#         history = messages
#         response, _ = self.model.chat(self.tokenizer, query = user_input, history = history, temperature = self.temperature)
#         return response
    
    
# # @register_class(alias="Engine.ChatGLM")
# # class ChatGLMEngine(Engine):
# #     def __init__(self):
# #         self.model_path = "/attached/remote-home/source/DISC-LawLLM-v2/Model/ChatGLM3-6B/chatglm3-6b/"
# #         self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
# #         self.sampling_params = SamplingParams(temperature=0.1, max_tokens=512)
# #         self.llm = LLM(model = self.model_path, dtype = torch.float16, trust_remote_code=True)

# #     def get_response(self, messages):
# #         retry = 0 
# #         while retry < 5:
# #             try:
# #                 text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
# #                 outputs = self.llm.generate([text], self.sampling_params)
# #                 for output in outputs: # prompt = output.prompt
# #                     generated_text = output.outputs[0].text # print(f"Generated text: {generated_text!r}")
# #                     response = generated_text
# #                 return response
# #             except Exception as e:
# #                 print(f"Error occurred: {e}")
# #                 retry += 1
# #                 time.sleep(10)



import zhipuai
from .base_engine import Engine
from utils.register import register_class


@register_class(alias="Engine.ChatGLM")
class ChatGLMEngine(Engine):
    def __init__(self, model_name="glm-4", temperature=0.0, top_p=0.9, incremental=True, *args, **kwargs):
        zhipuai.api_key = "36752e8b69327346ba50f6062b78b2c7.VzLRWlyrF43kmEvY"
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.incremental = incremental

    def get_response(self, messages):
        response = zhipuai.model_api.sse_invoke(
            model=self.model_name,
            prompt=messages,
            temperature=self.temperature,
            top_p=self.top_p,
            incremental=self.incremental
        )
        
        data = ""
        for event in response.events():
            data += event.data
            if event.event == "finish":
                meta = event.meta
                break
        return data
    