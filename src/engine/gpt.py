import os
import openai
from openai import OpenAI
from utils.register import register_class
from .base_engine import Engine
import time


@register_class(alias="Engine.GPT")
class GPTEngine(Engine):
    def __init__(self, openai_api_key, openai_api_base=None, openai_model_name=None, temperature=0.0, max_tokens=2048, top_p=1, frequency_penalty=0, presence_penalty=0):
        openai_api_key = openai_api_key if openai_api_key is not None else os.environ.get('OPENAI_API_KEY')
        assert openai_api_key is not None
        openai_api_base = openai_api_base if openai_api_base is not None else os.environ.get('OPENAI_API_BASE')

        self.model_name = openai_model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

        if openai_api_base is not None:
            self.client = OpenAI(
                api_key=openai_api_key,
                base_url=openai_api_base
            )
        else:
            self.client = OpenAI(
                api_key=openai_api_key,
            )

    def get_response(self, messages):
        # while True:
        #     try: 
        model_name = self.model_name
        i = 0
        while i < 5:
            try:
                # print("model name", model_name) 
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    top_p=self.top_p,
                    frequency_penalty=self.frequency_penalty,
                    presence_penalty=self.presence_penalty)
                break
            except openai.BadRequestError as e:
                print("error BadRequestError gpt:", e)
                time.sleep(20)
                i += 1
            except openai.RateLimitError as e:
                print("error RateLimitError gpt:", e)
                time.sleep(20)
                i += 1
            except Exception as e:
                print("error Exception gpt:", e)
                i += 1
                time.sleep(20)
                continue
        return response.choices[0].message.content

            # except:
            #     time.sleep(600)

            






