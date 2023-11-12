from langchain.document_loaders import PyPDFLoader
import re

def read_pdf(input_file):
    """
    This function reads a PDF file and returns a 'sanitised' version of its pages
    """
    langchain_loader = PyPDFLoader(input_file)
    document = langchain_loader.load()
    cleaned_document = remove_special_tokens(document)
    return cleaned_document
     
def normalise_whitespace(text):
    """
    This function reads a string and replaces all extra whitespace with a single whitespace. 
    newline and tab characters are also replaced with a single whitespace
    """
    cleaned_text = re.sub(r'\s+', ' ', text) 

    return cleaned_text

def remove_special_tokens(document):
    """
    This function reads a document and removes special tokens listed below from its pages iteratively.
    It also sanitises the text on a page by removing extra whitespace
    """

    special_tokens = ['>|endoftext|', '<|fim_prefix|', '<|fim_middle|', '<|fim_suffix|', '<|endofprompt|>']
    for page in document:
        content = page.page_content 
        for special in special_tokens:
            content = content.replace(special, '') 
            page.page_content = normalise_whitespace(content)
    return document



