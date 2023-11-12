import re

with open('/Users/kwabenaaboagye-otchere/Desktop/problem_questions.txt', 'r') as file:
    content = file.read()

def extract_numbers_and_create_set(section):
    numbers_matches = re.findall(r'(\d+(?:,\s*\d+)*)', section)
    return [set(map(int, match.split(','))) for match in numbers_matches]

# Split the content based on the "Concatenated question," "Concatenated answers," "Has table in Q," and "Has table in A" labels
question_sections = re.split(r'Concatenated question\n|Concatenated answers\n|Has table in Q\n|Has table in A\n', content)[1:]

# Extract each section
concatenated_question_section = extract_numbers_and_create_set(question_sections[0].strip())
concatenated_answers_section = extract_numbers_and_create_set(question_sections[1].strip())
has_table_in_q_section = extract_numbers_and_create_set(question_sections[2].strip())
has_table_in_a_section = extract_numbers_and_create_set(question_sections[3].strip())

# Print each section
print("Concatenated Question Section:")
print(concatenated_question_section)

print("\nConcatenated Answers Section:")
print(concatenated_answers_section)

print("\nHas Table in Q Section:")
print(has_table_in_q_section)

print("\nHas Table in A Section:")
print(has_table_in_a_section)
