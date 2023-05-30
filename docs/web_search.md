# WebSearch

This class is designed to perform a web search using the Google Custom Search API. The primary function of this operator is to take input from an AI Context and search the web using the given information.

**Functionality:**

- Declare name, parameters, inputs, and outputs - Designed for compatibility with other operators
- `run_step()` - Perform a web search and provide the results as output
- Helper functions for internal use by the operator

Below are more in-depth analyses of the crucial functions in this class.

## run_step

This function is responsible for performing a web search based on the given parameters and AI context. It starts by calling the `gen_prompt()` function, which creates a specific prompt to pass to the AI context. The AI context then generates a chat response using the prompt. Following this, the `google_search()` function is called to perform the web search based on the AI response, which is then processed using additional helper functions.

## get_urls_and_snippets

This helper function is called within `run_step()` and is responsible for processing the Google search results by extracting URLs and snippets from the JSON response. It extracts the title and snippet from each search result item and combines them into a single string, then appends the corresponding URLs separately. It ultimately returns two lists - one for the URLs and one for the titles and snippets.

## gen_prompt

This function constructs a prompt that will be fed to the AI context in order to generate a chat response. It takes the query from either the input provided by the AI context or the `query` parameter in the `step`. The constructed prompt requests intent for a Google search with the given goal or question.

## google_search

This function performs the actual web search using the Google Custom Search API. It takes a query and number of results as input, as well as the AI context, which is used to access the required API keys. The function uses the `customsearch` and `v1` services in the Google API, along with the input parameters, to perform a search and return the response as a JSON object.

Note that the function is designed to handle various errors, such as an invalid API key or general HTTP error, and will return a relevant error message when necessary.

## to_utf8_json_list

This is a utility function that converts a given list of strings to a valid JSON string, while ensuring it is encoded in UTF-8. This may be useful when working with web search results that include non-ASCII characters.