from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()

def get_trending_context(topic):
    dataset = load_dataset("heegyu/news-category-dataset")
    # print(f"Dataset: {dataset}")
    matching_rows = []

    # Extract rows that have information on topic
    for row in dataset['train']:
        if topic.lower() in row['headline'].lower() or topic.lower() in row['category'].lower():
            if len(matching_rows) > 5:
                break
            else:
                matching_rows.append(row)

    # Return headlines of matching rows
    return "\n\n".join([row['headline'] for row in matching_rows])




def generate_ideas(topic, content_type="blog post"):
    # Get trending context
    trending_context = get_trending_context(topic)
    # Initialize the model - prompt - parser
    llm = ChatOllama(model="llama3.2",
                     temperature=0.1)

    prompt = ChatPromptTemplate.from_template("""
        Build a social media post in the form of {content_type} based on the trending {topic} context:

        Context:
        {context}
        """
    )

    parser = StrOutputParser()

    # Create and run it through the LCEL chain
    chain = prompt | llm | parser

    response = chain.invoke({
        "context": trending_context,
        "content_type": content_type,
        "topic": topic
    })

    # Returns the output
    return response

if __name__ == "__main__":
    response = generate_ideas("horse")
    print(response)