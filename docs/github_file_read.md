# GitHubFileReader

The **GitHubFileReader** class is a custom operator that reads files from a given GitHub repository, matches them based on a given regular expression, and then saves the file names and content in an output list.

## Main Function:

### run_step

The `run_step()` method serves as the main function for this operator. It is responsible for initiating the process of reading files from the specified GitHub repository.

It takes two parameters:
- `step`: A dictionary containing all necessary parameters for the task.
- `ai_context`: An AiContext object, which is used to access secrets and manage inputs and outputs.

This method starts by reading the parameters from the `step` dictionary and then calls the `read_github_files()` helper method with the given parameters and AiContext object.

## Helper Functions:

### read_github_files

The `read_github_files()` method is responsible for connecting to the specified GitHub repository, parsing the repository contents, and filtering them according to the provided regular expression (if any).

It takes two parameters:
- `params`: A dictionary containing the parameters necessary for filtering the files.
- `ai_context`: An AiContext object, which is used to access secrets and manage inputs and outputs.

Inside this function:

1. Repository details (name, folders, regular expression, and branch) are extracted from the `params` dictionary.
2. A connection to the GitHub API is established using the access token stored in the AiContext object.
3. A breadth-first search (BFS) algorithm is applied to traverse the repository content, using the `bfs_fetch_files()` function.
4. Files that match the given regular expression are collected and stored in the `files` list.
5. The list of files is added to the AiContext output under the key 'files'.

### bfs_fetch_files

The `bfs_fetch_files()` (breadth-first search) function is responsible for traversing the directories and gathering files that match the specified regular expression. The BFS approach is used to ensure that all subdirectories are properly visited and that all matched files are collected.

It takes one parameter:
- `folder_path`: The path to the directory to be searched.

Inside this function:

1. A queue is used to store unprocessed directory paths. The input path is added to the queue.
2. While the queue is not empty, the first directory path is dequeued and its content is fetched from the GitHub API.
3. For each item in the fetched content, if it is a file and its name matches the given regular expression, it is added to the output list.
4. If an item is a directory, its path is added to the queue for further processing.

This function ensures that all subdirectories are properly searched and that all matched files are collected.