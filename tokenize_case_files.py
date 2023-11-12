import tiktoken
from uuid import uuid4
from langchain.text_splitter import RecursiveCharacterTextSplitter
from read_case_files import read_pdf
import sys

def determine_num_tokens(text):
    """
    This function determines how many tokens will be derived from a string.
    It returns the count of tokens.
    Helper function for chunking the text to be embedded 
    """
    tokenizer = tiktoken.get_encoding('cl100k_base') #p50k_base for gpt-4

    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)

def wrapper_text_splitter():
    """
    This is a wrapper function that chunks the data using langchain's textsplitter
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50, length_function=determine_num_tokens,separators=["\n\n", "\n", " ", ""])

    #The chunk overlap parameter helps chunks keep context between each other and recognise text next to each other
    return text_splitter

def create_chunks(document):
    """
    This function reads a document and returns a list of chunks of the text
    """
    #combine pages to single text
    page_content = document[0].page_content
    for i in range(1, len(document)):
        page_content = page_content + "\n\n" + document[i].page_content

    
    #chunk document text
    text_splitter = wrapper_text_splitter()
    chunks = []
    
    texts = text_splitter.split_text(page_content)
    chunks.extend([{
        'id': str(uuid4()),
        'text': texts[i],
        'chunk': i
    } for i in range(len(texts))])
    
    return chunks

