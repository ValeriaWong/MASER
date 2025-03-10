python run_maser.py --case_database /data/legal.json \
--lawyer Agent.Lawyer.FactGPT \
--lawyer_openai_model_name gpt-4o-2024-08-06 \
--plaintiff Agent.Plaintiff.FactGPT \
--plaintiff_openai_model_name gpt-4o-2024-08-06 \
--supervisor Agent.Supervisor.GPT \
--supervisor_openai_model_name gpt-4o-2024-08-06 \
--save_path /src/outputs/dialog_history/train_law_fact_gpt3.jsonl \
--max_conversation_turn 15 \
--parallel True







