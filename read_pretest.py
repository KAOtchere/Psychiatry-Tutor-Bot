from langchain.document_loaders import PyPDFLoader
import re

def read_pretest_pdf(input_file):
    langchain_loader = PyPDFLoader(input_file)
    pages = langchain_loader.load_and_split()
    text = pages[17].page_content

    print(text)
    print('\n' * 3)
    print('-' * 20)
    extract_q_n_a(text)

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
            questions_dict[question_number] = {'question': question_text, 'answers': [answer.strip() for answer in answers]}

    # Print the resulting dictionary
    for question_number, data in questions_dict.items():
        print(f"{question_number}: {data['question']}")
        for answer in data['answers']:
            print(f"  {answer}")
        print()

if __name__ == "__main__":
    # Set the path to your PDF file in Google Colab
    pdf_path = "/content/input_file.pdf"

    read_pretest_pdf(pdf_path)
