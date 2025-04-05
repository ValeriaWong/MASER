export OPENAI_API_KEY="*"
export OPENAI_API_BASE="https://api.deepseek.com/v1"

cd ~/code/MASER/src
export PYTHONPATH="$(pwd):$PYTHONPATH"

# 进入 src 目录
# cd "$(dirname "$0")/MASER-main/src"

python run_maser.py --case_database data/legal.json --lawyer Agent.Lawyer.FactGPT --lawyer_openai_model_name deepseek-r1 --plaintiff Agent.Plaintiff.FactGPT --plaintiff_openai_model_name deepseek-r1 --supervisor Agent.Supervisor.GPT --supervisor_openai_model_name deepseek-r1 --save_path src/outputs/dialog_history/train_law_fact_gpt3.jsonl --max_conversation_turn 15  --parallel True