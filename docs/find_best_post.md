# FindBestPost

**FindBestPost** is a class that extends the **BaseOperator**. Its main goal is to find the best post out of a given list of post titles and links that closely matches the user's query. The main functionality can be found in the `run_step()` and `find_best_post()` methods.

## run_step()

`run_step()` is the primary entry point for the FindBestPost operation. It gets the step and the AI context as parameters and calls `find_best_post()` method to execute the main logic.

```python
def run_step(self, step, ai_context: AiContext):
    params = step['parameters']
    self.find_best_post(params, ai_context)
```

## find_best_post()

`find_best_post()` is the primary function where the main logic is executed. It starts by retrieving the user query and the list of posts. Then, it filters the list to exclude any links that have already been used, as indicated in the comments of the code:

```python
used_links = ai_context.memory_get_list('tweeted_links')
title_link_dict = {title: url for title, url in title_link_dict.items() if url not in used_links}
```

Once the list has been filtered, the function converts the remaining titles into a single context string for the AI to analyze. 

```python
context_string = ', '.join(title_link_dict.keys())
```

Thereafter, the script prepares a prompt string for the chatbot, which should return the best matching post title for the specified query:

```python
message = f"From the following post titles: {context_string}, pick the post that most closely reflects this desire: {query}? Return the title of the post selected and nothing else."
```

Next, the chatbot processes the prompt and returns the best post title.

```python
best_post_title = ai_context.run_chat_completion(msgs=msgs)
```

Before obtaining the best corresponding link, the function checks if the title exists in the input title_link_dict. If it exists, it returns the title in the expected link format.

```python
if best_post_title not in title_link_dict and best_post_title.endswith('.'):
    best_post_title = best_post_title[:-1]  # Remove the last character (the period)
best_post_link = title_link_dict.get(best_post_title, '')
```

Finally, the script informs the user about the selected best post and sets the output to the best_post_link for further processing.

```python
ai_context.add_to_log(f"The most relevant post to your query is titled: {best_post_title}. With Link: {best_post_link}", self)
ai_context.set_output('best_post_link', best_post_link, self)
```

---
This markdown summary provides insight into the main structure of the FindBestPost class, focusing on the `run_step()` and `find_best_post()` functions where the key logic is implemented.