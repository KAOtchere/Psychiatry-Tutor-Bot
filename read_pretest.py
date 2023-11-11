
import sys
print(sys.path)
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
    pattern = re.compile(r'(\d+\.\w) (.+?)(?=(\d+\.\w|\Z))', re.DOTALL)

    # Find all matches in the text
    matches = pattern.findall(text)

    # Create a dictionary to store questions and answers
    questions_dict = {}

    # Iterate through matches and populate the dictionary
    for match in matches:
        question_number = match[0]
        question_text = match[1].strip()
        questions_dict[question_number] = {'question': question_text, 'answers': []}

    # Use regex to extract answer choices for each question
    for question_number, _, next_question_number in matches:
        start_pos = text.find(question_number) + len(question_number) + 1
        end_pos = text.find(next_question_number) if next_question_number else None
        question_text = text[start_pos:end_pos].strip()
        answers = re.findall(r'([a-e]\. .+?)(?=(\n[a-e]\.|$))', question_text)
        questions_dict[question_number]['answers'] = [answer[0] for answer in answers]

    # Print the resulting dictionary
    for question_number, data in questions_dict.items():
        print(f"{question_number}: {data['question']}")
        for answer in data['answers']:
            print(f"  {answer}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: odnoneove")
    
    input_file = sys.argv[1]

    read_pretest_pdf(input_file)