from typing import TypedDict

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

class ResearchState(TypedDict):
    topic: str
    sub_questions: list
    results: list
    summary: str

def planner_node(state):
    topic = state['topic']

    # Create and run chain
    llm = ChatOllama(model="llama3.2",
                     temperature=0.1)
    parser = StrOutputParser()
    prompt = ChatPromptTemplate.from_template(
    """
    Generate 3 sub-questions about the research {topic}
    """
    )

    chain = prompt | llm | parser
    response = chain.invoke({
        "topic": topic
    })

    # Extract sub-questions to pass to searcher node
    sub_questions = [line[3:] for line in response.split('\n') if '?' in line]

    return {"sub_questions": sub_questions}

def searcher_node(state):
    sub_questions = state['sub_questions']
    search = DuckDuckGoSearchRun()
    results = []

    # iterate through questions
    for question in sub_questions:
        results.append(search.run(question))

    return {"results": results}

def writer_node(state):
    topic = state['topic']
    results = state['results']
    joined_results = " ".join(results)

    # Create and run chain
    llm = ChatOllama(model="llama3.2",
                     temperature=0.1)
    parser = StrOutputParser()
    prompt = ChatPromptTemplate.from_template("""
    Create a summary of the search results on {topic}:

    Search Results:
    {results}
    """
    )

    chain = prompt | llm | parser
    summary = chain.invoke({
        "topic": topic,
        "results": joined_results
    })

    return {"summary": summary}




if __name__ == "__main__":
    state = ResearchState(topic="Data Mining")
    planner_node(state)