#import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os
import pandas as pd
import tiktoken
import openai
from openai.embeddings_utils import distances_from_embeddings
import numpy as np
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity
openai.api_key = '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'
def chatbot(text):
    def remove_newlines(serie):
        serie = serie.str.replace('\n', ' ')
        serie = serie.str.replace('\\n', ' ')
        serie = serie.str.replace('  ', ' ')
        serie = serie.str.replace('  ', ' ')
        return serie

    # Create a list to store the text files
    texts=[("text", text)]

    df = pd.DataFrame(texts, columns = ['fname', 'text'])

    # Set the text column to be the raw text with the newlines removed
    df['text'] = df.fname + ". " + remove_newlines(df.text)
    df.to_csv('scraped.csv')
    df.head()

    # Load the cl100k_base tokenizer which is designed to work with the ada-002 model
    tokenizer = tiktoken.get_encoding("cl100k_base")

    df = pd.read_csv('scraped.csv', index_col=0)
    df.columns = ['title', 'text']

    # Tokenize the text and save the number of tokens to a new column
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    # Visualize the distribution of the number of tokens per row using a histogram
    df.n_tokens.hist()

    max_tokens = 500

    # Function to split the text into chunks of a maximum number of tokens
    def split_into_many(text, max_tokens = max_tokens):

        # Split the text into sentences
        sentences = text.split('. ')

        # Get the number of tokens for each sentence
        n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]
        
        chunks = []
        tokens_so_far = 0
        chunk = []

        # Loop through the sentences and tokens joined together in a tuple
        for sentence, token in zip(sentences, n_tokens):

            # If the number of tokens so far plus the number of tokens in the current sentence is greater 
            # than the max number of tokens, then add the chunk to the list of chunks and reset
            # the chunk and tokens so far
            if tokens_so_far + token > max_tokens:
                chunks.append(". ".join(chunk) + ".")
                chunk = []
                tokens_so_far = 0

            # If the number of tokens in the current sentence is greater than the max number of 
            # tokens, go to the next sentence
            if token > max_tokens:
                continue

            # Otherwise, add the sentence to the chunk and add the number of tokens to the total
            chunk.append(sentence)
            tokens_so_far += token + 1

        return chunks
        

    shortened = []

    # Loop through the dataframe
    for row in df.iterrows():

        # If the text is None, go to the next row
        if row[1]['text'] is None:
            continue

        # If the number of tokens is greater than the max number of tokens, split the text into chunks
        if row[1]['n_tokens'] > max_tokens:
            shortened += split_into_many(row[1]['text'])
        
        # Otherwise, add the text to the list of shortened texts
        else:
            shortened.append( row[1]['text'] )

    df = pd.DataFrame(shortened, columns = ['text'])
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    df.n_tokens.hist()

    # Note that you may run into rate limit issues depending on how many files you try to embed
    # Please check out our rate limit guide to learn more on how to handle this: https://platform.openai.com/docs/guides/rate-limits

    df['embeddings'] = df.text.apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])
    df.to_csv('embeddings.csv')
    df.head()

    df=pd.read_csv('embeddings.csv', index_col=0)
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

    df.head()
<<<<<<< HEAD
    return df
    ################################################################################
    ### Step 12
    ################################################################################

    


    

def getResponse(df, question):
=======

>>>>>>> fecb1f2e49ce19c9f18e666b253a8fee4b898a0d
    def create_context(
        question, df, max_len=1800, size="ada"
    ):
        """
        Create a context for a question by finding the most similar context from the dataframe
        """

        # Get the embeddings for the question
        q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

        # Get the distances from the embeddings
        df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')


        returns = []
        cur_len = 0

        # Sort by distance and add the text to the context until the context is too long
        for i, row in df.sort_values('distances', ascending=True).iterrows():
            
            # Add the length of the text to the current length
            cur_len += row['n_tokens'] + 4
            
            # If the context is too long, break
            if cur_len > max_len:
                break
            
            # Else add it to the text that is being returned
            returns.append(row["text"])

        # Return the context
        return "\n\n###\n\n".join(returns)

    def answer_question(
        df,
        model="text-davinci-003",
        question="Am I allowed to publish model outputs to Twitter, without a human review?",
        max_len=1800,
        size="ada",
        debug=False,
        max_tokens=150,
        stop_sequence=None
    ):
        """
        Answer a question based on the most similar context from the dataframe texts
        """
        context = create_context(
            question,
            df,
            max_len=max_len,
            size=size,
        )
        # If debug, print the raw model response
        if debug:
            print("Context:\n" + context)
            print("\n\n")

        try:
            # Create a completions using the questin and context
            response = openai.Completion.create(
                prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"The question you asked is not within the notes you provided, but here is some information from me regarding your question!\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
                temperature=0,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=stop_sequence,
                model=model,
            )

            if response["choices"][0]["text"].strip() == "The question you asked is not within the notes you provided, but here is some information from me regarding your question!":
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=question,
                    temperature=0.1,
                    max_tokens=max_tokens,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )

                return response["choices"][0]["text"].strip()
            return response["choices"][0]["text"].strip()
        except Exception as e:
            print(e)
            return ""

    import webbrowser
    import openai
    import re
    #
    # from bs4 import BeautifulSoup
    #
    import requests

    def webgpt(query):
        url = "https://www.google.com/search?q=" + query
        webbrowser.open(url)

        # Extract links from Google search results
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.startswith('/url?q='):
                url = href.split('=')[1].split('&')[0]
                links.append(url)

        # Prompt GPT-3 to generate a response to the query
        # prompt = "GPT-3 prompt goes here"
        # response = openai.Completion.create(
        #   engine="davinci",
        #   prompt=prompt,
        #   max_tokens=100
        # )

        # Extract response text and add links to the end
        # text = response.choices[0].text
        link_text = '\nRelated links:\n'
        for link in links[:4]:
            link_text += link + '\n'
        return link_text
    #modify code to prompt on front end not backend and etc

    

    ################################################################################
    ### Step 14
    ################################################################################

    # create a webapi to call this function for me
    question = input("What is your question: ")
    answer = answer_question(df, question=question, debug=False)
    return answer + "\n" + webgpt(answer)
