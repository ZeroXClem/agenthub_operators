import requests

from .base_operator import BaseOperator
from ai_context import AiContext


class TrelloCardCreator(BaseOperator):
    @staticmethod
    def declare_name():
        return "trello_card_creator"

    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.ACT.value

    @staticmethod
    def declare_parameters():
        return [
            {
                "name": "list_id",
                "data_type": "string",
                "placeholder": "Enter the list ID",
            },
        ]

    @staticmethod
    def declare_inputs():
        return [
            {
                "name": "name",
                "data_type": "string",
                "optional": "1",
            },
            {
                "name": "description",
                "data_type": "string",
                "optional": "1",
            },
            {
                "name": "label_ids",
                "data_type": "string[]",
                "optional": "1",
            },
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "created_card",
                "data_type": "json",
            },
        ]

    def run_step(self, step, ai_context: AiContext):
        try:
            params: dict[str, str] = step["parameters"]
            list_id: str = params.get("list_id")

            name: str = ai_context.get_input("name", self)
            description: str = ai_context.get_input("description", self)
            label_ids: list[str] = ai_context.get_input("label_ids", self)

            key: str = ai_context.get_secret("trello_key")
            token: str = ai_context.get_secret("trello_token")

            created_card = self.create_card(
                list_id, name, description, label_ids, key, token, ai_context
            )
            ai_context.set_output("created_card", created_card, self)
        except Exception as error:
            ai_context.add_to_log(f"An error occurred: {str(error)}")

    def create_card(
        self,
        list_id: str,
        name: str,
        description: str,
        label_ids: list[str],
        key: str,
        token: str,
        ai_context: AiContext,
    ):
        url = "https://api.trello.com/1/cards"
        headers = {"Accept": "application/json"}
        query = {
            "idList": list_id,
            "key": key,
            "token": token,
            "name": name,
            "desc": description,
            "idLabels": ",".join(label_ids),
        }

        try:
            session = requests.Session()
            response = session.post(url, headers=headers, params=query)

            if not 200 <= response.status_code < 300:
                ai_context.add_to_log(f"An error occurred: {response.text}")
                return

            return response.text
        except requests.RequestException as error:
            ai_context.add_to_log(f"An error occurred: {str(error)}")
            return
