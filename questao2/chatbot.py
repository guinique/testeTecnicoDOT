import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

# Carrega variáveis do .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY não encontrada. "
        "Crie um arquivo .env com sua chave."
    )


def create_chain():

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4o-mini",
        temperature=0.5
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a senior software engineer researcher in Python and LLMs.

            Rules:
            - Answer clearly.
            - Give concise code examples.
            - If appropriate, explain step by step.
            - Consider previous conversation context when answering.
            """
        ),
        ("placeholder", "{history}"),
        ("human", "{question}")
    ])

    parser = StrOutputParser()

    # chain do langchain melhorada para manter o contexto da conversa e gerar respostas mais relevantes
    chain = prompt | llm | parser

    return chain


def run_examples(chain):
    examples = [
        "Como criar uma lista em Python?",
        "Qual a diferença entre lista e tupla?",
        "O que é uma LLM e como ela funciona?",
    ]

    history = []

    print("\n===== EXEMPLOS =====\n")

    for question in examples:

        print(f"You: {question}")

        answer = chain.invoke({
            "history": history,
            "question": question
        })

        print(f"\nBot: {answer}\n")

        history.append(
            HumanMessage(content=question)
        )

        history.append(
            AIMessage(content=answer)
        )

        print("-" * 80)

    print("\n===== FIM DOS EXEMPLOS =====\n")


def run_chatbot():

    chain = create_chain()

    history = []

    print("Python Expert Chatbot Started!")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() in ["exit", "quit"]:
            print("Exiting chatbot. Goodbye!")
            break

        if not question.strip():
            continue

        print("Thinking...")

        try:

            answer = chain.invoke({
                "history": history,
                "question": question
            })

            print(f"\nBot: {answer}\n")

            history.append(
                HumanMessage(content=question)
            )

            history.append(
                AIMessage(content=answer)
            )

        except Exception as e:

            print(
                f"Error communicating with OpenAI: {e}\n"
            )


if __name__ == "__main__":

    chain = create_chain()

    # demonstração solicitada no exercício
    run_examples(chain)

    # Chat interativo
    run_chatbot()