
from utils.register import register_class, registry
import random

def style(to_revised, speak_style, law_level): # 给出建议，让原告自己修改
    engine = registry.get_class("Engine.GPT")(openai_api_key=None,openai_api_base=None,openai_model_name="gpt-4o-2024-08-06",temperature=0,max_tokens=1024,top_p=1,frequency_penalty=0,presence_penalty=0)
    
    content = "你是一名专业的说话风格分析师，擅长从角色发言中分析角色的说话风格。\n"
    content += "<角色发言>" + to_revised + "\n"
    content += "<说话特点>" + speak_style["tone"].replace("你的","").replace("你","")
    content += speak_style["content"].replace("你的","").replace("你","")
    content += speak_style["interaction"].replace("你的","").replace("你","") 
    content += law_level + "\n\n"

    content += \
        "你需要判断<角色发言>是否与<说话特点>相匹配。" + \
        "按照下面的格式输出。" + \
        "如果<角色发言>与<说话特点>不匹配，用十分简洁的语言给出说话风格的修正建议。\n" + \
        "**匹配程度**：不匹配。\n**建议**xxx\n" + \
        "如果<角色发言>与<说话特点>相匹配，则回复：\n" + \
        "**匹配程度**：匹配。\n**建议**无\n" 
    
    # print("style content~~~~~~~~~~~",content) 
    messages = []
    messages.append({'role':'user',"content":content})
    
    response = engine.get_response(messages)
    style_advice = response.replace("**匹配程度**：","").replace("**匹配程度**：匹配","").replace("**匹配程度**：不匹配","").replace("不匹配","").replace("匹配","") 
    # print("style_advice", style_advice)
    return style_advice 







