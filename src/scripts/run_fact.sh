export OPENAI_API_KEY="*"
export OPENAI_API_BASE="https://api.deepseek.com/v1"

cd ~/code/MASER/src
export PYTHONPATH="$(pwd):$PYTHONPATH"

python run_law_fact.py --scenario Law.Scenario.Fact
