import requests

from .base_operator import BaseOperator
from ai_context import AiContext


class DiscordMessageSender(BaseOperator):
    @staticmethod
    def declare_name():
        return "discord_send_message"

    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.ACT.value

    @staticmethod
    def declare_parameters():
        return [
            {
                "name": "channel_id",
                "data_type": "string",
                "placeholder": "Enter the channel ID",
            },
            {
                "name": "embed_color",
                "data_type": "string",
                "placeholder": "Enter the embed color as a hex code",
                "optional": "1",
            },
        ]

    @staticmethod
    def declare_inputs():
        return [
            {
                "name": "message_content",
                "data_type": "string",
                "optional": "1",
            },
            {
                "name": "embed_title",
                "data_type": "string",
                "optional": "1",
            },
            {
                "name": "embed_description",
                "data_type": "string",
                "optional": "1",
            },
            {
                "name": "embed_fields",
                "data_type": "{name, value}[]",
                "optional": "1",
            },
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "message_status",
                "data_type": "string",
            },
        ]

    def run_step(self, step, ai_context: AiContext):
        params: dict[str, str] = step["parameters"]
        channel_id: str = params.get("channel_id")
        embed_color: str = params.get("embed_color")

        message_content: str = ai_context.get_input("message_content", self)
        embed_title: str = ai_context.get_input("embed_title", self)
        embed_description: str = ai_context.get_input("embed_description", self)
        embed_fields: list[dict[str, str]] = ai_context.get_input("embed_fields", self)

        token: str = ai_context.get_secret("discord_bot_token")

        message_status = self.send_message(
            channel_id,
            message_content,
            embed_title,
            embed_description,
            embed_fields,
            embed_color,
            token,
            ai_context,
        )
        ai_context.set_output("message_status", message_status, self)

    def send_message(
        self,
        channel_id: str,
        message_content: str,
        embed_title: str,
        embed_description: str,
        embed_fields: list[dict[str, str]],
        embed_color: str,
        token: str,
        ai_context: AiContext,
    ):
        try:
            contains_embed = any((embed_title, embed_description, embed_fields))
            if not message_content and not contains_embed:
                ai_context.add_to_log("No message content or embeds provided.")
                return "Message sending failed"

            url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
            headers = {
                "Authorization": f"Bot {token}",
                "Content-Type": "application/json",
            }

            data = {"content": message_content}

            if contains_embed:
                embed = {}
                if embed_title:
                    embed["title"] = embed_title
                if embed_description:
                    embed["description"] = embed_description
                if embed_fields:
                    embed["fields"] = embed_fields
                if embed_color:
                    embed_color = int(embed_color.replace("#", ""), 16)
                    embed["color"] = embed_color
                data["embeds"] = [embed]

            session = requests.Session()
            response = session.post(url, headers=headers, json=data)

            if 200 <= response.status_code < 300:
                return "Message sent successfully"
            else:
                ai_context.add_to_log(f"An error occurred: {response.text}")
                return "Message sending failed"
        except Exception as error:
            ai_context.add_to_log(f"An error occurred: {str(error)}")
            return "Message sending failed"
