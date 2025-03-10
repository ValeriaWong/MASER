
from utils.register import register_class, registry

def guide(role, question):
    engine = registry.get_class("Engine.GPT")(openai_api_key=None,openai_api_base=None,openai_model_name="gpt-4o-2024-08-06",temperature=0,max_tokens=1024,top_p=1,frequency_penalty=0,presence_penalty=0)
    
    content = "给出一段##文本##，你的任务是判断这段文本的类型。"    
    content += \
        "可选的文本类型如下：\n" + \
        "<原告的基本信息>\n" + \
        "<被告的基本信息>\n" + \
        "<案件的事实>\n" + \
        "<原告的诉讼请求>\n" + \
        "<原告的证据>\n" 

    content += "##文本##：" + question
    content += \
    "按照下面的格式输出。\n" + \
    "##文本的类型##：xxx \n" 
    # "若##文本##是原告的姓名、性别等内容，则回复：“##文本的类型##：<原告的基本信息>” \n" + \
    # "若##文本##是被告的基本信息等内容，则回复：“##文本的类型##：<被告的基本信息>” \n" + \
    # "若##文本##的内容是案件的基本情况、则事件发生的时间、地点、事件经过等相关内容，则回复：“##文本的类型##：<案件的事实>” \n" + \
    # "若##文本##是被告需要采取的具体行动、承担诉讼费用等内容，则回复：“##文本的类型##：<原告的诉讼请求>” \n" + \
    # "若##文本##是证据相关内容时，则回复：“##文本的类型##：<原告的证据>” \n" 
    # "若##文本##是其他内容时，回复：“##文本的类型##：<其他>” \n"

    if role == "原告":
        content += "\n 请注意##文本##中的“我”和“我们”都是指“原告”。"
    if role == "律师":
        content += "\n 请注意##文本##中的“您”或者“你”是指“原告”。"

    messages = []
    # messages.append({'role': 'system', "content": SYSTEM_PROMPT})
    messages.append({'role':'user',"content":content})
    response = engine.get_response(messages)
    stage = response.split("##文本的类型##：")[-1]
    return stage