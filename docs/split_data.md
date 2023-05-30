# SplitData

The **SplitData** class is a custom operator that recursively splits text into chunks based on the provided parameters. This operator can be useful for large-scale data processing and text analysis tasks, where the input data needs to be split into smaller, more manageable pieces. The functionality of this operator is mostly carried out in the `run_step` and helper methods.

Text splitting is done using the **RecursiveCharacterTextSplitter** class, which is imported at the beginning of the script. Apart from the standard declarations for name, parameters, inputs, and outputs, there are three key methods in this class: `run_step`, `process`, and `split`.

## run_step

```python
def run_step(
        self,
        step,
        ai_context: AiContext
):
    params = step['parameters']
    split_text = self.process(params, ai_context)
    ai_context.set_output('rts_processed_content', split_text, self)
    ai_context.add_to_log("Successfully split text!")
```

`run_step` is the main method that is called when executing this operator. It takes the `step` and `ai_context` objects as inputs and then extracts the parameters from the `step` object. After this, it runs the `process` method with these parameters and the `ai_context`.

Once the processing is done, the method sets the output using the `ai_context.set_output` method and logs that the text has been successfully split.

## process

```python
def process(self, params, ai_context):
    text = ai_context.get_input('text', self)
    formatted = self.split(params, ai_context, text)
    return formatted
```

The `process` method takes the `params` and `ai_context` as inputs and gets the text that needs to be split from the `ai_context` object. Then, it calls the `split` method with the `params`, `ai_context`, and `text`. After splitting is done, it returns the split text.

## split

```python
def split(self, params, ai_context, content):
    chunk_size = params.get('chunk_size', '2000')
    chunk_overlap = params.get('chunk_overlap', '100')

    if chunk_size:
        chunk_size = int(chunk_size)
    else:
        chunk_size = 2000

    if chunk_overlap:
        chunk_overlap = int(chunk_overlap)
    else:
        chunk_overlap = 100
    ai_context.add_to_log(f"Splitting text with {chunk_size} size and {chunk_overlap} overlap")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(content)
    return texts
```

The `split` method takes the `params`, `ai_context`, and `content` as inputs and first extracts the `chunk_size` and `chunk_overlap` from the `params`. It then converts these values to integers and sets the defaults if they are not provided.

Next, the method logs the settings that it will use for splitting the text. It then creates an instance of the `RecursiveCharacterTextSplitter` with the specified `chunk_size` and `chunk_overlap`, and calls its `split_documents` method to split the content into smaller chunks.

Finally, the split texts are returned as the output of the method.