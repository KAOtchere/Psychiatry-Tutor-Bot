from langchain.document_loaders import PyPDFLoader
import re
import sys

def read_pretest_pdf(input_file):
    langchain_loader = PyPDFLoader(input_file)
    pages = langchain_loader.load_and_split()
    text = pages[5].page_content
    print(text)
    # print(text)
    # print('\n' * 3)
    # print('-' * 20)
    # extract_q_n_a(text)

def extract_q_n_a(text):
    pattern = re.compile(r'(\d+\.[A-Z].*?)(?=\d+\.[A-Z]|$)', re.DOTALL)

    # Find all matches in the text
    matches = pattern.findall(text)

    # Create a dictionary to store questions and answers
    questions_dict = {}

    # Iterate through matches and populate the dictionary
    for match in matches:
        match = match.strip()
        question_match = re.match(r'(\d+\.[A-Z].*?)(?=\d+\.[A-Z]|$)', match, re.DOTALL)
        if question_match:
            question_text = question_match.group(1).strip()
            answers = re.findall(r'[A-E]\. .*?(?=[A-E]\. |\Z)', match)
            question_number = re.match(r'(\d+)\.', question_text).group(1)
            #TODO: 1. strip number from beginning of question. 2. determine where to start reading from 3. determine topic (page numbers can be used)
            #TODO: 2. determine where to start reading from 
            #TODO: 3. determine topic (page numbers can be used)
            #TODO: 4. create db to hold questions and answers
            #TODO: 5. Map right answer to question and embed explanation
            questions_dict[question_number] = {'question': question_text, 'answers': [answer.strip() for answer in answers]}

    # Print the resulting dictionary
    for question_number, data in questions_dict.items():
        print(f"{question_number}: {data['question']}")
        for answer in data['answers']:
            print(f"  {answer}")
        print()

if __name__ == "__main__":
    # Set the path to your PDF file in Google Colab
    pdf_path = sys.argv[1]

    read_pretest_pdf(pdf_path)
