## HybridSearch

The `HybridSearch` class is a custom operator designed to perform a hybrid search using embeddings and the model's capabilities. It inherits from the `BaseOperator` class, and has specific methods that handle its unique functionality. The main goal of this operator is to perform a search based on the input query and the vector index and then generate a response using the model. It does so by using the `run_step` function along with some helper functions to process the input and generate the output. 

### run_step

This method is responsible for executing the main logic of the operator. It takes two parameters: `step` and `ai_context`. It starts by extracting the `query` parameter and embedding it using `ai_context.embed_text()` function. 

Next, it sorts the chunks from the `vector_index` input using the `sort_chunks_by_similarity()` helper function, which takes the query embedding and the vector index as arguments. 

It then constructs a prompt string to be used as input for the model and calculates the token limit and budget using the `count_tokens()` and `get_max_tokens_for_model()` helper functions. The tokens are necessary to ensure that the model can process the input without exceeding its maximum token capacity.

Following this, the operator selects the most relevant chunks using the `select_most_relevant_chunks()` function. This function takes the sorted chunks, token budget, and model name as inputs and returns the selected chunks.

After selecting the chunks, they are added to the prompt and the model is executed using `ai_context.run_chat_completion()` with the constructed prompt. Finally, the operator sets the output of the operator as the response from the model and logs the response.

### sort_chunks_by_similarity

This helper function takes the query embeddings and the vector index as inputs, and it sorts the chunks based on their similarity with the query embeddings. It returns the sorted list of chunks.

### select_most_relevant_chunks

This helper function takes the sorted_chunks, token_budget, and model_name as inputs and returns the most relevant chunks without exceeding the token budget. It ensures that the model can efficiently process the input without hitting the token limit.

### get_max_tokens_for_model

This utility function retrieves the maximum number of tokens that a specific model can handle.

### count_tokens

This utility function counts the number of tokens in a given text prompt based on the model name provided.

By using the HybridSearch operator, you can perform a hybrid search and generate a response using the model, while effectively managing the token budget and exploiting the capabilities of embeddings and the model itself.