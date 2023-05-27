import json
import re

from github import Github

from .base_operator import BaseOperator

from ai_context import AiContext


class GitHubFileReader(BaseOperator):
    @staticmethod
    def declare_name():
        return 'Get files from GitHub'
    
    @staticmethod    
    def declare_parameters():
        return [
            {
                "name": "repo_name",
                "data_type": "string",
                "placeholder": "user_name/repository_name"
            },
            {
                "name": "folders",
                "data_type": "string",
                "placeholder": "Enter the file paths, separated by commas",
                "input_format": "commaSeparatedList"
            },
            {
                "name": "file_regex",
                "data_type": "string",
                "placeholder": "Enter the regex to filter file names (e.g. '.*\.py' )"
            },
            {
                "name": "branch",
                "data_type": "string",
                "placeholder": "Enter the branch (default is main)"
            }
        ]
    
    @staticmethod    
    def declare_inputs():
        return []
    
    @staticmethod    
    def declare_outputs():
        return [
            {
                "name": "files",
                # List of dictionaries, each of which has keys 'name' and 'contnet' set.
                # All values stored in the dictionary objects are assumed to be strings.
                # Note that for now the data_type string below is just a string, it has 
                # no semantic meaning other than the fact that Overlord class would only
                # connect output of one operator to the input of another if their types match.
                "data_type": "{name,content}[]",
            }
        ]

    def run_step(
        self, 
        step, 
        ai_context : AiContext
    ):
        # We expect user to define a json dictionary in the input field that would include
        # all necessary parameter for the task.
        params = step['parameters']
        self.read_github_files(params, ai_context)
            
            
    def read_github_files(self, params, ai_context):
        repo_name = params['repo_name']
        folders = params.get('folders')
        file_regex = params.get('file_regex')
        branch = params.get('branch', 'master')

        g = Github(ai_context.get_secret('github_access_token'))
        repo = g.get_repo(repo_name)

        files = []

        def file_matches_regex(file_path, file_regex):
            if not file_regex:
                return True

            return re.fullmatch(file_regex, file_path)

        def bfs_fetch_files(folder_path):
            queue = [folder_path]

            while queue:
                current_folder = queue.pop(0)

                contents = repo.get_contents(current_folder, ref=branch)

                for item in contents:
                    if item.type == "file" and file_matches_regex(item.path, file_regex):
                        file_content = item.decoded_content.decode('utf-8')
                        files.append(
                            {
                                'name': item.path,
                                'content': file_content
                            }
                        )

                    elif item.type == "dir":
                        queue.append(item.path)

        for folder_path in folders:
            bfs_fetch_files(folder_path)

        list_of_file_paths = [d['name'] for d in files]
        ai_context.add_to_log(f"{self.declare_name()} Fetched {len(list_of_file_paths)} files from GitHub repo {repo_name}:\n\r{list_of_file_paths}", color='blue', save=True)

        ai_context.set_output('files', files, self)
        return True

