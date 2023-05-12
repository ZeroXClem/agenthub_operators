import ast
import requests
from .base_operator import BaseOperator

from ai_context import AiContext

class GitHubDocsWriter(BaseOperator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def declare_name():
        return 'Write documentation to GitHub'
    
    @staticmethod    
    def declare_parameters():
        return [
            {
                "name": "repo_owner",
                "data_type": "string",
                "placeholder": "Enter the GitHub repository owner username"
            },
            {
                "name": "repo_name",
                "data_type": "string",
                "placeholder": "Enter the GitHub repository name"
            },
            {
                "name": "doc_file_name",
                "data_type": "string",
                "placeholder": "Enter the name of the documentation file"
            }
        ]
    
    @staticmethod    
    def declare_inputs():
        return [
            {
                "name": "code_content",
                "data_type": "string"
            }
        ]
    
    @staticmethod    
    def declare_outputs():
        return [
            {
                "name": "doc_file_url",
                "data_type": "string"
            }
        ]

    def run_step(
        self, 
        step, 
        ai_context : AiContext
    ):
        params = step['parameters']
        code_content = ai_context.get_input('code_content', self)
        doc_content = self.generate_docs(code_content)
        doc_file_url = self.write_docs_to_github(params, doc_content, ai_context)
        ai_context.set_output('doc_file_url', doc_file_url, self)
        return True

    def generate_docs(self, code_content):
        # Parse the code to extract docstrings from functions and classes
        parsed_code = ast.parse(code_content)
        docstrings = []
        for node in parsed_code.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and ast.get_docstring(node):
                docstrings.append(ast.get_docstring(node))
        return '\n'.join(docstrings)
    
    def write_docs_to_github(self, params, doc_content, ai_context):
        # Write the generated docs to a file in the specified repo
        repo_owner = params['repo_owner']
        repo_name = params['repo_name']
        doc_file_name = params['doc_file_name']
        access_token = params['github_access_token']
        
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{doc_file_name}"
        headers = {
            "Authorization": f"token {ai_context.get_secret('github_access_token')}",
            "Accept": "application/vnd.github+json"
        }
        data = {
            "message": "Create documentation",
            "content": doc_content.encode('utf-8').hex()
        }
        
        response = requests.put(api_url, json=data, headers=headers)
        response.raise_for_status()
        contents = response.json()
        return contents['content']['html_url']

