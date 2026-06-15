import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

# Carrega variáveis do .env
load_dotenv()


# carrega a chave da API do OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY não encontrada. "
        "Crie um arquivo .env com sua chave."
    )


def run_chatbot():

    # Inicializa o modelo explicitando a chave
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
        )
    ])

    parser = StrOutputParser()

    # histórico da conversa
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

            # lista de mensagens:
            messages = prompt.format_messages()

            # adiciona todo o histórico
            messages.extend(history)

            # adiciona a nova pergunta
            messages.append(
                HumanMessage(content=question)
            )

            # chama o modelo
            response = llm.invoke(messages)

            answer = parser.invoke(response)

            print(f"\nBot: {answer}\n")

            # salva na memória
            history.append(
                HumanMessage(content=question)
            )

            history.append(
                AIMessage(content=answer)
            )

        except Exception as e:
            print(f"Error communicating with OpenAI: {e}\n")


if __name__ == "__main__":
    run_chatbot()