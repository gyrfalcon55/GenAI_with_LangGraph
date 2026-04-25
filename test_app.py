from langchain_ollama import ChatOllama
# from langsmith import traceable
from dotenv import load_dotenv
import os 

os.environ['LANGSMITH_PROJECT']="TAGS AND METADATA ADDED"


load_dotenv()

llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0.5
)

config = {
    'tags':['llm','sample_project'],
    'metadata':{'model':'llama3.2:latest','inference':'ChatOllama'}
}

# @traceable(run_type="llm")
def llm_call(query:str) -> str:
    result = llm.invoke(query,config=config)
    return result.content

print(llm_call("hi, my name is junaid"))