# Code Summary

This code includes several utility functions related to working with different GPT models, calculating cosine similarity, and selecting the most relevant text chunks.

## **get_max_tokens_for_model**

Given a model name, this function returns the maximum tokens supported by the model. It raises a ValueError if the model is not supported.

```python
def get_max_tokens_for_model(model_name: str) -> int:
``` 

## **cosine_distance**

This function calculates the cosine similarity between two vectors v1 and v2.

```python
def cosine_distance(v1, v2):
``` 

## **count_tokens**

This function takes a string and a model name, and returns the number of tokens in the string according to the model's tokenization.

```python
def count_tokens(s: str, model_name: str) -> int:
``` 

## *Hybrid Search Helpers*

### **sort_chunks_by_similarity**

This function sorts a list of text chunks based on their similarity to the given query embedding. It uses the cosine distance function to calculate similarity.

```python
def sort_chunks_by_similarity(query_emb, vector_index):
``` 

### **select_most_relevant_chunks**

This function selects the most relevant text chunks according to their sorted similarity score and the token budget constraint. It keeps adding chunks to the selected list until the token budget is exhausted or all chunks have been evaluated.

```python
def select_most_relevant_chunks(sorted_chunks, token_budget, model_name):
``` 

The code outlined above provides a set of utility functions for working with GPT models, calculating cosine similarity between two vectors, and selecting the most relevant text chunks based on their similarity to a query embedding. These functions can be used in various NLP tasks, such as information retrieval or text summarization.