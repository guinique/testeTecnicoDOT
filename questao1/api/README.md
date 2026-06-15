# setup

conda create -n questao1

conda activate questao1

pip install fastapi uvicorn sqlalchemy pydantic pytest httpx

# run

uvicorn main:app --reload

# run tests

pytest test_main.py -v
