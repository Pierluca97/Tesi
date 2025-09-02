from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
import argparse
import json


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user-input", type=str, help="The question to find the subject on Europeana")
    return parser.parse_args()


def main():
    args = parse_arguments()



    llm_model = Ollama(model="llama3.2", base_url="http://localhost:11434")

    template = """Extract the most important subject from the sentence in Question field, note that the subject must be a person

    Question: {question}

    Answer: Use the following schema for the answer and don't say anything else

    Schema: {{"subject": "<answer>"}} 
    """

    prompt = PromptTemplate.from_template(template)


    chain = prompt | llm_model
    response = chain.invoke({"question": args.user_input})

    response = json.loads(response)

    print("\nLLM Response:\n", response['subject'])


if __name__ == "__main__":
    main()