## ListProcessor

**ListProcessor** is a class that extends the **BaseOperator** class, allowing it to perform different operations on the input list based on the prompt provided. As part of the **BaseOperator** class, the **ListProcessor** must declare its name, parameters, inputs, and outputs.

### Parameters

The only parameter of the **ListProcessor** is:

- `prompt` (type: string): The user's instruction to the AI for processing the list items.

### Inputs

The required input for the **ListProcessor** is:

- `list` (type: {name,content}[]): A list of objects containing name and content attributes.

### Outputs

The output of the **ListProcessor** is:

- `result_list` (type: {name,content}[]): A list of processed objects containing name and content attributes.

### run_step Function

The main function of the **ListProcessor** class is `run_step`. This function takes two arguments - `step` and `ai_context`. It first retrieves the input list and checks if it is valid. If the input 'list' is not present in AiContext, it logs an error message and returns `False`.

For each element in the input list, the function constructs a `prompt` using the provided `step['parameters']['prompt']` and passes it to ai_context's `run_chat_completion` method to get the AI response. The result is a processed list containing the new content from the AI and the same element name.

The function then appends this processed element to the `result_list` and sets the output as `result_list` in `ai_context`. If the entire processing is successful, the function returns `True`.

### Example of Generated Markdown

```
## ListProcessor

**ListProcessor** is a class that extends the **BaseOperator** class, allowing it to perform different operations on the input list based on the prompt provided. As part of the **BaseOperator** class, the **ListProcessor** must declare its name, parameters, inputs, and outputs.

### Parameters

The only parameter of the **ListProcessor** is:

- `prompt` (type: string): The user's instruction to the AI for processing the list items.

### Inputs

The required input for the **ListProcessor** is:

- `list` (type: {name,content}[]): A list of objects containing name and content attributes.

### Outputs

The output of the **ListProcessor** is:

- `result_list` (type: {name,content}[]): A list of processed objects containing name and content attributes.

### run_step Function

The main function of the **ListProcessor** class is `run_step`. This function takes two arguments - `step` and `ai_context`. It first retrieves the input list and checks if it is valid. If the input 'list' is not present in AiContext, it logs an error message and returns `False`.

For each element in the input list, the function constructs a `prompt` using the provided `step['parameters']['prompt']` and passes it to ai_context's `run_chat_completion` method to get the AI response. The result is a processed list containing the new content from the AI and the same element name.

The function then appends this processed element to the `result_list` and sets the output as `result_list` in `ai_context`. If the entire processing is successful, the function returns `True`.
```