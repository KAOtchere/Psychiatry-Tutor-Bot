from openai import OpenAI
import os
from dotenv import load_dotenv
from make_embeddings import define_index
from read_case_files import normalise_whitespace
import tiktoken

OPEN_AI_KEY = os.getenv('OPEN_AI_API_KEY')
OPEN_AI_BASE_URL = os.getenv('OPEN_AI_BASE_URL')

OPEN_AI_CLIENT = OpenAI(api_key=OPEN_AI_KEY, base_url=OPEN_AI_BASE_URL)
MODEL = 'text-embedding-ada-002'

def ask_question(query=None):
    primer = f""" You are a pyschiatry tutor trying to teach a student via case studies. 
    Formulate a case style question using the information provided above. 
    You should describe the goal and objective of the question you are posing."""

    res = OPEN_AI_CLIENT.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = {
            {"role": "system", "content": primer},
            {"role": "user", "content": query}
        },temperature= 0.3,
        top_p = 1,
        stream = False
    )

    return res["choices"][0]["message"]["content"]

def give_feedback(query):
    primer = f""" You are a pyschiatry tutor trying to teach a student via case studies. 
    You asked the student a question and this was their response. Based on the context section,
    analyse the user's response and and give them feedback about their answer.
    """

    res = OPEN_AI_CLIENT.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = {
            {"role": "system", "content": primer},
            {"role": "user", "content": query}
        },temperature= 0.3,
        top_p = 1,
        stream = False
    )

    return res["choices"][0]["message"]["content"]

def clarify_feedback(query):
    primer = f""" You are a pyschiatry tutor trying to teach a student via case studies. 
    You gave them feedback and they are not clear on what you said. Clarify their question on your feedback based on the context section.
    If you are not able to answer apologise and say your knowledge base is not deep enough to help
    """

    res = OPEN_AI_CLIENT.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = {
            {"role": "system", "content": primer},
            {"role": "user", "content": query}
        },temperature= 0.5,
        top_p = 1,
        stream = False
    )

    return res["choices"][0]["message"]["content"]

def answer_question(query):
    primer = f""" You are a pyschiatry tutor trying to teach a student via case studies.
    They have asked you a question about a concept they do not understand. Using the context provided, answer their question.
    If you are unable to use the context provided, you may use your own knowledge base granted you say where you got this knowledge from
    so it may be verified.
    """

    res = OPEN_AI_CLIENT.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = {
            {"role": "system", "content": primer},
            {"role": "user", "content": query}
        },temperature= 0.2,
        top_p = 1,
        stream = False
    )

    return res["choices"][0]["message"]["content"]

    

def agent(prompt_mode=None, query=None):
    """
    This program will be used to interact with the user.
    It may either start the conversation by asking a user to analyse a case,
    give them feedback about their  analysis,
    clarify misunderstanding in feedback provided
    or answer a question
    """

    

    modes = {None: ask_question, "feedback": give_feedback, "question": answer_question, "question_about_feedback": clarify_feedback}

    mode = modes[prompt_mode]
    
    output = mode(query)

    return output

def sanitise_text(text):
    text = normalise_whitespace(text)

    #tokenize text and make sure it does not exceed token limit
    tokenizer = tiktoken.get_encoding('cl100k_base')
    tokens = tokenizer.encode(text, disallowed_special=())
    
    #strip text till the num tokens is less than max token len 1536
    if len(tokens) > 1536:
        length_exceeded = sum(len(s) for s in tokens[1536:])
        text = text[:length_exceeded]
    
    return text

def generate_query(text):

    index = define_index('psychiatry-case-studies', 'cosine', 1536)

    text = sanitise_text(text)

    res = OPEN_AI_CLIENT.embeddings.create(input=[text], model=MODEL)

    text_embedding = res.data[0].embedding

    res = index.query(vector=text_embedding, top_k=5)

    contexts = [item['metadata']['text'] for item in res['matches']]

    query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+text

    return query

    

#TODO define environment to interact with the agent