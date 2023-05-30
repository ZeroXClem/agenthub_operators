from .base_operator import BaseOperator
from github import Github
from ai_context import AiContext
import os
import time
import random

class GitHubDocsWriter(BaseOperator):
    @staticmethod
    def declare_name():
        return 'GitHub Docs Writer'
    
    @staticmethod    
    def declare_parameters():
        return [
            {
                "name": "repo_name",
                "data_type": "string",
                "placeholder": "user_name/repository_name"
            },
            {
                "name": "docs_folder_name",
                "data_type": "string",
                "placeholder": "docs_folder_name"
            }
        ]
    
    @staticmethod    
    def declare_inputs():
        return [
            {
                "name": "code_content",
                "data_type": "{name,content}[]"
            }
        ]
    
    @staticmethod    
    def declare_outputs():
        return []

    def run_step(
        self, 
        step, 
        ai_context : AiContext
    ):
        params = step['parameters']
        l = ai_context.get_input('code_content', self)

        g = Github(ai_context.get_secret('github_access_token'))
        repo = g.get_repo(params['repo_name'])
        forked_repo = repo.create_fork()

        base_branch_name = 'main'
        base_branch = repo.get_branch(base_branch_name)

        all_files = []
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                file = file_content
                all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))


        new_branch_name = f"agent_hub_{ai_context.get_run_id()}"
        GitHubDocsWriter.create_branch_with_backoff(forked_repo, new_branch_name, base_branch.commit.sha)

        run_url = f'https://agenthub.dev/agent?run_id={ai_context.get_run_id()}'

        for el in l:
            file_path = el['name']
            name = os.path.splitext(os.path.basename(file_path))[0] + '.md'
            file_name = params['docs_folder_name'] + '/' + name
            file_content_string = el['content']

            commit_message = f"{file_path} - commit created by {run_url}"

            if file_name in all_files:
                file = repo.get_contents(file_name, ref=base_branch_name)
                forked_repo.update_file(file_name, commit_message, file_content_string.encode("utf-8"), file.sha, branch=new_branch_name)
            else:
                forked_repo.create_file(file_name, commit_message, file_content_string.encode("utf-8"), branch=new_branch_name)

        # Create a pull request to merge the new branch in the forked repository into the original branch
        pr_title = f"PR created by {run_url}"
        pr_body = f"PR created by {run_url}"

        pr = repo.create_pull(
            title=pr_title, 
            body=pr_body, 
            base=base_branch_name, 
            head=f"{forked_repo.owner.login}:{new_branch_name}"
        )
        
        ai_context.add_to_log(f"Pull request created: {pr.html_url}")

    @staticmethod  
    def create_branch_with_backoff(forked_repo, new_branch_name, base_branch_sha, max_retries=3, initial_delay=5):
        delay = initial_delay
        retries = 0

        while retries < max_retries:
            try:
                forked_repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=base_branch_sha)
                return
            except Exception as e:
                if retries == max_retries - 1:
                    raise e

                sleep_time = delay * (2 ** retries) + random.uniform(0, 0.1 * delay)
                print(f"Error creating branch. Retrying in {sleep_time:.2f} seconds. Error: {e}")
                time.sleep(sleep_time)
                retries += 1
