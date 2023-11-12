from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import os
import sys
from openai import OpenAI
from time import sleep
from dotenv import load_dotenv
from tqdm.auto import tqdm #helps observe embed progress
from read_case_files import read_pdf
from tokenize_case_files import create_chunks

def define_index(index_name, metric, dimension):
    """
        This function connects to an index in pinecone vectorstore
    """


    # find API key in console at app.pinecone.io
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY') or 'PINECONE_API_KEY'
    # find ENV (cloud region) next to API key in console
    PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT') or 'PINECONE_ENVIRONMENT'
    try:
        pinecone.init(api_key=PINECONE_API_KEY,environment=PINECONE_ENVIRONMENT)
    except:
        print("could not init pinecone connection")
        sys.exit(1)

    if index_name not in pinecone.list_indexes():
        # we create a new index
        pinecone.create_index(
            name=index_name,
            metric=metric,
            dimension= dimension
        )

    index = pinecone.Index(index_name) # get the index

    return index

# def config_open_ai():
#     openai.api_key = os.getenv('OPEN_AI_API_KEY')


def embed_chunks(chunks):
    """
    This program generates embeddings for the chunks using openai's ada 002.
    The embeddings are stored in a pinecone db
    """
    load_dotenv()

    openai_api_key = os.getenv('OPEN_AI_API_KEY')
    openai_base_url = os.getenv('OPEN_AI_BASE_URL')

    model = 'text-embedding-ada-002'
    index = define_index('psychiatry-case-studies', 'cosine', 1536) #1536 is the size of ada's embeddings
    open_ai_client = OpenAI(api_key=openai_api_key, base_url=openai_base_url)

    batch_size = 50 #this is the number of chunks we embed and insert at once
    for i in tqdm(range(0, len(chunks), batch_size)):
        i_end = min(len(chunks), i+batch_size)
        meta_batch = chunks[i:i_end]
        # get ids
        ids_batch = [x['id'] for x in meta_batch]
        # get texts to encode
        texts = [x['text'] for x in meta_batch]
        # create embeddings (try-except added to avoid RateLimitError)
        try:
            res = open_ai_client.embeddings.create(input=texts, model=model)
        except BaseException as e:
            print(f"An error happened and the reason is: \n  {str(e)}")
            done = False
            while not done:
                sleep(5)
                try:
                    res = open_ai_client.embeddings.create(input=texts, model=model)
                    done = True
                except:
                    pass
       
        embeds = [record.embedding for record in res.data]
        # cleanup metadata
        meta_batch = [{ 'text': x['text'], 'chunk': x['chunk']} for x in meta_batch]

        to_embed = list(zip(ids_batch, embeds, meta_batch)) # zip ids, embeddings and metadata
        # upsert to Pinecone
        index.upsert(vectors=to_embed)
        print('bach upserted')


if __name__ == "__main__":
    input_file = sys.argv[1]
    document = read_pdf(input_file)
    chunks = create_chunks(document)
    embed_chunks(chunks)
