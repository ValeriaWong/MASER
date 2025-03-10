
from utils.register import register_class, registry
import random

def temper(role, fact, speak_style):
    engine = registry.get_class("Engine.GPT")(openai_api_key=None,openai_api_base=None,openai_model_name="gpt-4o-2024-08-06",temperature=0.5, max_tokens=2048,top_p=1,frequency_penalty=0,presence_penalty=0)
    
    choice = ["设想你正在经历一种轻微的意识模糊，请用一种不太连贯的方式复述以下文字，并在内容上做一些小的调整：",
              "现在需要你复述以下信息，请尽量**精神涣散**地复述以下文字，请注意，你复述的事实应该具有些许偏差：",
              "想象你在一个迷失的状态中，请将下面的文字用一种不清晰的方式复述，确保有些信息是错误的或缺失的：",
              "你感到有些精神恍惚，请复述以下内容，尽量使其变得模糊且不准确，并添加一些轻微的偏差：",
              "现在请用一种不太确定的方式复述下面的文本，确保包含一些小的错误："
              ]
    idx = random.randint(0,4)
    
    # content = "你是一个出现了轻微幻觉的患者，现在需要你复述以下信息，请尽量**精神涣散**地复述以下文字，请注意，你复述的事实应该具有些许偏差："
    content = choice[idx] 
    print("模糊content~~~~~~~~~~~",content)
    content += fact + "\n\n"
    
    content += \
          "请注意：\n你是原告，以第一人称回复叙述事实。" + \
          "你的说话语气特点为：{}" .format(speak_style["tone"]) + \
          "你的说话内容特点为：{}" .format(speak_style["content"]) + \
          "你的互动行为特点为：{}" .format(speak_style["interaction"]) 

    messages = []
    # messages.append({'role': 'system', "content": SYSTEM_PROMPT})
    messages.append({'role':'user',"content":content})
    response = engine.get_response(messages)
    tamp_fact = response.split("##篡改后的案件事实##：")[-1]
    return tamp_fact 

if __name__ == "__main__":
    fact = "2017年12月份经原告对被告村子村民修建的养殖牛羊棚圈验收后，根据棚圈补助标准（非建档立卡户每个棚圈补助4140元，建档立卡户每个棚圈补助6000元），原告工作人员给被告周玉新提供的账号为×××信用社银行账户内转入10个棚圈的项目补助款41400元。同时因工作人员失误把与被告周玉新同名同音的桃山村二社建档立卡户周玉兴的棚圈补助款也转入了被告周玉新提供的另一个账号为×××的信用社银行账户内，被告周玉新收到错付的6000元棚圈补助款没有合法根据，属不当得利。原告工作人员发现付款错误后，与被告周玉新联系，要求返还该补助款，但被告不偿还。"
    temper(role = "",fact=fact)

