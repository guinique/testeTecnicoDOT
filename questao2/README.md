# setup

conda create -n questao2

conda activate questao2

pip install langchain langchain-openai langchain-core python-dotenv

## setup langsmith

# windows

set LANGCHAIN_TRACING_V2=true
set LANGCHAIN_API_KEY=<your-api-key>

# linux

export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY="<your-api-key>"

# or in env

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=<your-api-key>

# run

python chatbot.py
