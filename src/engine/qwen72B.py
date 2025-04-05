import os
import openai
from openai import OpenAI
from utils.register import register_class
from .base_engine import Engine
import time
import tiktoken


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


@register_class(alias="Engine.qwen72B")
class qwen72Engine(Engine):
    def __init__(self, temperature=0.0, max_tokens=1024, top_p=1, frequency_penalty=0, presence_penalty=0):
        openai_api_key = "1234"
        openai_api_base = "http://10.28.5.226:51480/v1"

        self.model_name = "qwen2.5-72b"
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

        if openai_api_base is not None:
            self.client = OpenAI(
                api_key=openai_api_key,
                base_url=openai_api_base)
        else:
            self.client = OpenAI(
                api_key=openai_api_key,)

    def get_response(self, messages):
        # tokens_len = 0
        # for m in messages:
        #     if m["content"]

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
                    presence_penalty=self.presence_penalty
                )
                break
            except openai.BadRequestError as e:
                print("error BadRequestError qwen72b:", e)
                time.sleep(10)
                i += 1
            except openai.RateLimitError as e:
                print("error RateLimitError qwen72b:", e)
                time.sleep(60)
                i += 1
            except Exception as e:
                print("error other qwen72b:",e)
                i += 1
                time.sleep(10)
                continue
            # else:
            #     i += 1 
        return response.choices[0].message.content


            






