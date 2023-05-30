# ChatBot

`ChatBot` is a class that inherits from `BaseOperator`. Its main functionality is to provide an answer to a query using a given Vector Index and the conversation history of the user.

**Important sections**:

1. **run_step**
2. **Helper Functions**

## run_step

`run_step` is the main function in the `ChatBot` class. It takes the "step" and "ai_context" objects as arguments.

The purpose of this function is to generate a response to a user's query by incorporating both the Hybrid Search results and the user's chat history into the model's input prompt. Here, the Vector Index (which is fetched using the `vi_uuid` from `step['parameters']`) is utilized for retrieving contextually relevant data. The function starts by obtaining the maximum token limit for the given model, a prompt is generated with `query` as its base, and the number of tokens spent is calculated.

As a part of its functionality, `run_step` allocates token budgets for context and chat history. It then uses the helper functions `sort_chunks_by_similarity` and `select_most_relevant_chunks` to select the most relevant chunks from the Vector Index using the Hybrid Search mechanism. These selected chunks are added to the input prompt, along with chat history from the relevant conversation.

Finally, the function runs the chat completion using the generated input prompt (which includes context and chat history) and saves the result as the chatbot's response. It also adds the user's query and chatbot's response to the chat history memory.

## Helper Functions:

- **sort_chunks_by_similarity**: This function sorts chunks based on their similarity to a given query with the help of a Vector Index.

- **select_most_relevant_chunks**: This function selects the most relevant chunks given a sorted list, a token budget, and a model name.

- **get_max_tokens_for_model**: A utility function used to determine the maximum number of tokens permitted for the AI model.

- **count_tokens**: A utility function used to count the tokens in a given text for a specified model.