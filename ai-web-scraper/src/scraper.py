from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests
from bs4 import BeautifulSoup


def scrape_web(url, query, truncate_size=5000):
    # Get response from HTTP Get request -> returns object with status_code, header + HTML text
    request_response = requests.get(url)

    # Converts Raw HTML into a Document Object Model (DOM) for dynamic access
    soup = BeautifulSoup(request_response.text, "html.parser")

    # Exctracts text from DOM ( removes HTML tags )
    cleaned_text = " ".join(soup.get_text().split())
    truncated_text = cleaned_text[:truncate_size]

    # initialize the model
    model = ChatOllama(model="llama3.2",
                       temperature=0.1)

    # initialize parser - converts AIMessage into plain string
    parser = StrOutputParser()

    # Create Prompt template for langchain to use during execution
    prompt = ChatPromptTemplate.from_template(
        """
        Answer the user's question based on the webpage content.

        Webpage Content:
        {context}

        Question:
        {question}
        """
    )

    # Create Chain (LCEL) - Langchain Expression Language Pipeline
    chain = prompt | model | parser

    # Executes the pipeline / Chain
    agent_response = chain.invoke({
        "context": truncated_text,
        "question": query
    })

    print(agent_response)
    return agent_response


if __name__ == "__main__":
    test_url = "https://www.sfu.ca/fas/computing/news-events/news/2025/july/new-sfu-study-transforms-drug-design--promises-faster-life-savin.html"

    test_query = "what does AI have to do with designing drugs?"

    scrape_web(test_url, test_query)