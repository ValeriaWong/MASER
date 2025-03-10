import argparse
import os
import json
from typing import List
import jsonlines
from tqdm import tqdm
import time
import concurrent
import random
from utils.register import register_class, registry
from utils.tamperer import temper


@register_class(alias="Law.Scenario.Fact")
class Law_Fact:
    def __init__(self, args):
        case_database = json.load(open(args.case_database,'r', encoding='utf-8'))
        self.args = args 
        # self.lawyer = registry.get_class(args.lawyer)(args)  
        self.plaintiffs = []
        for plaintiff_profile in case_database[5000:]:
            plaintiff = registry.get_class(args.plaintiff)(
                args,
                id=plaintiff_profile["id"],
                case_r_f=plaintiff_profile["case_r_f"],
                plaintiff=plaintiff_profile["plaintiff"],
                defendant=plaintiff_profile["defendant"],
                claim=plaintiff_profile["claim"],
                evidence=plaintiff_profile["evidence"],
                less=plaintiff_profile["less"],
                law_level=plaintiff_profile["law_level"],
                speak_style=plaintiff_profile["speak_style"],
                personality=plaintiff_profile["personality"],
                plaintiff_type=plaintiff_profile["plaintiff_type"],
                reason=plaintiff_profile["reason"],
                laws=plaintiff_profile["laws"])
            self.plaintiffs.append(plaintiff)

        # 根据你与当事人(原告)的历史对话  
        self.extract_information = "根据你和当事人（原告）对话总结以下信息：" + \
                                    "按照下面的格式给出。\n" + \
                                    "#原告信息#\nxx\n\n" + \
                                    "#被告信息#\nxx\n\n" + \
                                    "#诉讼请求#\nxx\n\n" + \
                                    "#事实和理由#\nxx\n\n" + \
                                    "#证据和证据来源，证人姓名和住所#\nxx"
        self.draft_indictment = """
        最后你需要参照给定的起诉状模板，将你和当事人（原告）对话整理成起诉状。
        起诉状模板为：
                                                起诉状
        
            原告：×××，男/女，××××年××月××日生，×族，单位……(写明工作单位和职务或职业)，地址……。身份证号……，联系方式：……。
            被告：×××，男/女，××××年××月××日生，×族，单位……(写明工作单位和职务或职业)，地址……。身份证号……，联系方式：……。
            委托诉讼代理人：×××。
            诉讼请求：……（多个请求分点为1.2.……）
            事实和理由：……
            证据和证据来源，证人姓名和住所：……（多个证据分点为1.2.……）
            
                此致
            ××××人民法院
        
                                                                    起诉人：(亲笔签名)
                                                                    ××××年××月××日
            
    """

        self.max_conversation_turn = args.max_conversation_turn
        self.delay_between_tasks = args.delay_between_tasks
        self.max_workers = args.max_workers
        self.save_path = args.save_path
        self.ff_print = args.ff_print
        self.start_time = time.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def add_parser_args(parser: argparse.ArgumentParser):
        parser.add_argument("--case_database", default="/attached/remote-home/thuang/new_AI_Law_main_2/vs_AI_Law_main/src/data/case_msf_train.json", type=str)
        parser.add_argument("--plaintiff", default="Agent.Plaintiff.FactGPT", help="registry name of plaintiff agent")
        parser.add_argument("--lawyer", default="Agent.Lawyer.FactGPT", help="registry name of doctor agent")
        parser.add_argument("--supervisor", default="Agent.Supervisor.GPT", help="registry name of supervisor agent")
        parser.add_argument("--max_conversation_turn", default=15, type=int, help="max conversation turn between doctor and patient")
        parser.add_argument("--max_workers", default=10, type=int, help="max workers for parallel diagnosis")
        parser.add_argument("--delay_between_tasks", default=10, type=int, help="delay between tasks")
        parser.add_argument("--save_path", default="/attached/remote-home/thuang/new_AI_Law_main_2/vs_AI_Law_main/src/outputs/dialog_history_iiyi/train_law_fact_gpt3.jsonl", help="save path for dialog history")
        parser.add_argument("--ff_print", default=True, action="store_true", help="print dialog history")
        parser.add_argument("--parallel", default=False, action="store_true", help="parallel diagnosis")

    def remove_processed_cases(self): # 移除掉已经询问过的cases 
        processed_case_ids = {}
        if os.path.exists(self.save_path):
            with jsonlines.open(self.save_path, "r") as f:
                for obj in f:
                    processed_case_ids[obj["case_id"]] = 1
            f.close()
        plaintiff_num = len(self.plaintiffs)
        for i, plaintiff in enumerate(self.plaintiffs[::-1]): # 从头到尾返回一个新的、元素顺序相反的序列
            if processed_case_ids.get(plaintiff.id) is not None:
                self.plaintiffs.pop((plaintiff_num-(i+1)))
            
        # random.shuffle(self.plaintiffs) # 打乱顺序
        print("To-be-facted case Number: ", len(self.plaintiffs))

    def find_less(self,text,less):
        # 搜索“民族：”关键字后面的内容
        start = text.find(less + "：") + len(less + "：")
        if start != -1:
            # 找到“民族：”之后的第一个逗号，确定民族信息的结束位置
            end = text.find("，", start)
            if end != -1:
                # 提取民族信息
                ethnicity = text[start:end].strip()
            else:
                # 如果没有找到逗号，说明民族信息是最后一个字段
                ethnicity = text[start:].strip()
        else:
            print("less信息未找到")
        return ethnicity
    
    def run(self):
        self.remove_processed_cases()
        # st = time.time()
        
        for plaintiff in tqdm(self.plaintiffs):
            self._diagnosis(plaintiff)
            # patient.forget() 
            # self.doctor.forget() 
        # print("duration: ", time.time() - st)

    def parallel_run(self):
        self.remove_processed_cases()

        st = time.time() 
        print("Parallel Consult Start")
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 使用 map 来简化提交任务和获取结果的过程 
            # executor.map(self._diagnosis, self.patients) 
            futures = [executor.submit(self._diagnosis, plaintiff) for plaintiff in self.plaintiffs]
            # 使用 tqdm 来创建一个进度条 
            for _ in tqdm(concurrent.futures.as_completed(futures), total=len(self.plaintiffs)):
                pass

        print("duration: ", time.time() - st)
        
    def _diagnosis(self, plaintiff):
        print("id", plaintiff.id)
        
        # if plaintiff.id != 6028:
        #     print("nono")
        #     return

        # print("原告信息————", plaintiff.plaintiff)
        # print("被告信息————",plaintiff.defendant)
        # print("---------------------------------------------------------------") 
        # print("懂法程度————",plaintiff.law_level)
        # print("说话方式————",plaintiff.speak_style)
        # print("性格特点————",plaintiff.personality)
        # print("---------------------------------------------------------------") 
        # print("缺失————",plaintiff.less)
        # print("事实理由————",plaintiff.case_r_f)
        
        # case_type=None, case_facts=None, case_r_f=None, plaintiff=None, less=None, law_level=None, defendant=None, claim=None, evidence=None
        lawyer = registry.get_class(self.args.lawyer)(self.args, plaintiff_type = plaintiff.plaintiff_type, reason = plaintiff.reason, laws = plaintiff.laws)
        supervisor = registry.get_class(self.args.supervisor)(self.args)  

        dialog_history = [{"turn": 0, "role": "Plaintiff", "content": plaintiff.plaintiff_greet}]
        dialog_history.append({"turn": 0, "role": "Lawyer", "content": lawyer.lawyer_greet})

        history = "**原告**：" + plaintiff.plaintiff_greet + "\n" 
        history += "**律师**：" + lawyer.lawyer_greet + "\n"
        
        plaintiff.memorize(("assistant", plaintiff.plaintiff_greet))
        plaintiff.memorize(("user", lawyer.lawyer_greet))
        lawyer.memorize(("user", plaintiff.plaintiff_greet), plaintiff.id)
        lawyer.memorize(("assistant", lawyer.lawyer_greet), plaintiff.id)

        if self.ff_print:
            print("############### Dialog ###############")
            print("--------------------------------------")
            print(dialog_history[-1]["turn"], dialog_history[-1]["role"])
            print(dialog_history[-1]["content"])
        
        # 储存**修改建议**   
        revise_history = []

        for turn in range(self.max_conversation_turn): 
            revise_dict = {}
            revise_dict["turn"] = turn + 1
            revise_dict["plaintiff"] = {}
            revise_dict["lawyer"] = {}

            if turn == 0:
                plaintiff_response = plaintiff.speak(dialog_history[-1]["role"], content = dialog_history[-1]["content"])
            else:
                plaintiff_response = plaintiff.speak(dialog_history[-1]["role"], content = dialog_history[-1]["content"], save_to_memory=False)
                print("_________________________________________________start________________________________________________________________")
                print("修改前————", plaintiff_response)
                revise_dict["plaintiff"]["修改前"] = plaintiff_response

                history += "**律师**：" + dialog_history[-1]["content"] + "\n"
                supervisor_response = supervisor.speak(speak_style=plaintiff.speak_style,law_level=plaintiff.law_level,less=plaintiff.less, history=history, role="Plaintiff", to_revised=plaintiff_response, question=lawyer_response, PLAINTIFF=plaintiff.plaintiff, DEFENDANT=plaintiff.defendant, case_r_f=plaintiff.case_r_f, claim=plaintiff.claim, evidence=plaintiff.evidence)
                print("advice", supervisor_response)
                revise_dict["plaintiff"]["advice"] = supervisor_response

                if len(supervisor_response) == 2: 
                    plaintiff_response = supervisor_response[1]
                    print("修改后————",plaintiff_response)
                    revise_dict["plaintiff"]["修改后"] = plaintiff_response 

                    plaintiff.memorize(("user", dialog_history[-1]["content"]))
                    plaintiff.memorize(("assistant", plaintiff_response)) 
                else: 
                    if "回复无误" not in supervisor_response: # 需要修改  
                        plaintiff_response = plaintiff.correct_speak(advice=supervisor_response, false_reply = plaintiff_response, content = dialog_history[-1]["content"], save_to_memory=True)
                        print("修改后————",plaintiff_response)
                        revise_dict["plaintiff"]["修改后"] = plaintiff_response
                        print("______________________________________________________end_______________________________________________________")
                    elif "回复无误" in supervisor_response: # 不需要修改  
                        plaintiff.memorize(("user", dialog_history[-1]["content"]))
                        plaintiff.memorize(("assistant", plaintiff_response))
                plaintiff_response   

            dialog_history.append({"turn": turn+1, "role": "Plaintiff", "content": plaintiff_response})
            if self.ff_print:
                print("----------------------------------------------------------------------------------------")
                print(dialog_history[-1]["turn"], dialog_history[-1]["role"])
                print(dialog_history[-1]["content"]) 
            

            
            if turn == 0:
                history += "**原告**：" + plaintiff_response + "\n"
                lawyer_response = lawyer.speak(plaintiff_response, plaintiff.id)
            else:
                lawyer_response = lawyer.speak(plaintiff_response, plaintiff.id, save_to_memory=False)
                print("______________________________________________________start________________________________________________________")
                print("修改前————",lawyer_response)
                revise_dict["lawyer"]["修改前"] = lawyer_response

                history += "**原告**：" + plaintiff_response + "\n"
                supervisor_response = supervisor.speak(speak_style=plaintiff.speak_style, less=plaintiff.less, history=history, role="Lawyer" , to_revised=lawyer_response, question=plaintiff_response, PLAINTIFF=plaintiff.plaintiff, DEFENDANT=plaintiff.defendant, case_r_f=plaintiff.case_r_f, claim=plaintiff.claim, evidence=plaintiff.evidence)
                print("advice",supervisor_response)
                revise_dict["lawyer"]["advice"] = supervisor_response

                if "回复无误" not in supervisor_response: # 需要修改 
                    lawyer_response = lawyer.correct_speak(advice=supervisor_response, false_reply = lawyer_response, content = plaintiff_response, case_id = plaintiff.id, save_to_memory=True) 
                    print("修改后————",lawyer_response)
                    revise_dict["lawyer"]["修改后"] = lawyer_response
                    print("______________________________________________________end________________________________________________________")
                elif "回复无误" in supervisor_response: # 不需要修改 
                    lawyer.memorize(("user", plaintiff_response), plaintiff.id)
                    lawyer.memorize(("assistant", lawyer_response), plaintiff.id)
                lawyer_response   

            dialog_history.append({"turn": turn+1, "role": "Lawyer", "content": lawyer_response})
            revise_history.append(revise_dict)
            if self.ff_print:
                print("----------------------------------------------------------------------------------------")
                print(dialog_history[-1]["turn"], dialog_history[-1]["role"])
                print(dialog_history[-1]["content"])
            if "<询问结束>" in lawyer_response: break

             
        # conclusion = lawyer.speak(self.extract_information, plaintiff.id)
        # dialog_history.append({"turn": turn + 1, "role": "Lawyer", "content": conclusion})

        lawyer_response = lawyer.speak(self.draft_indictment, plaintiff.id)
        dialog_history.append({"turn": turn+2, "role": "Lawyer", "content": lawyer_response})
        if self.ff_print:
            print("----------------------------------------------------------------------------------------")
            print(dialog_history[-1]["turn"], dialog_history[-1]["role"])
            print(dialog_history[-1]["content"])
            # self.evaluate(patient_profile, doctor_response)  

        dialog_info = {
            "case_id": plaintiff.id,
            "lawyer": self.args.lawyer,
            "lawyer_engine_name": lawyer.engine.model_name,
            "plaintiff": self.args.plaintiff,
            "plaintiff_engine_name": plaintiff.engine.model_name,
            "law_level": plaintiff.law_level,
            "speak_style": plaintiff.speak_style,
            "personality": plaintiff.personality,
            "dialog_history": dialog_history,
            "time": self.start_time,
        }

        self.save_dialog_info(dialog_info) # 保存报错原因之一：self.save_path这个jsonl文件里面最后一行没有换行符

        # 储存所有数据 
        all_info = {
            "case_id": plaintiff.id,
            "lawyer": self.args.lawyer,
            "lawyer_engine_name": lawyer.engine.model_name,
            "plaintiff": self.args.plaintiff,
            "plaintiff_engine_name": plaintiff.engine.model_name,
            "law_level": plaintiff.law_level,
            "speak_style": plaintiff.speak_style,
            "personality": plaintiff.personality,
            "dialog_history": dialog_history,
            "revise_history": revise_history,
            "time": self.start_time,
        }
        with jsonlines.open("/attached/remote-home/thuang/new_AI_Law_main_2/vs_AI_Law_main/src/outputs/dialog_history_iiyi/train_law_fact_gpt3_alldata.jsonl", "a") as f:
            f.write(all_info)
        f.close()


    def save_dialog_info(self, dialog_info):
        with jsonlines.open(self.save_path, "a") as f:
            f.write(dialog_info)
        f.close()





