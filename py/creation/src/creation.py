'''
Dummy
'''
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def create(anchor: str, target: str, dirname: str) -> str:
    '''
    Creates a new directory and initializes the necessary files.
    Also returns a poem about anchor, target, and dirname.
    '''

    # Create directory if it doesn't exist
    os.makedirs(dirname, exist_ok=True)

    # Set the OpenAI API key (inline for now)
    # os.environ["OPENAI_API_KEY"] = ""  # 🔐 Replace with your actual key

    # Initialize the OpenAI chat model
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)

    # Generate a poem prompt
    prompt = f"""
    Write a short and whimsical poem about:
    - an anchor named '{anchor}'
    - a target named '{target}'
    - and a magical place called '{dirname}'
    """

    # Invoke the model with the prompt
    response = llm.invoke([HumanMessage(content=prompt)])

    return response.content
