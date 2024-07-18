# Summary
The `DiscordMessageSender` operator sends a message using the Discord API with the specified message content and channel ID.

# Inputs
- `message_content`: A string containing the message content to be sent. Optional if an embed is provided.
- `embed_title`: A string containing the title of the embed message. Optional.
- `embed_description`: A string containing the description of the embed message. Optional.
- `embed_fields`: A list of dictionaries containing the names and values of the fields of the embed. Optional.

# Parameters
- `channel_id`: A string representing the channel's ID where the message will be sent.
- `embed_color`: A string representing the color of the embed message as a hex code. Optional.

# Outputs
- `message_status`: A string indicating the status of the message sending process, either "Message sent successfully" or "Message sending failed".

# Functionality
The `run_step` function is responsible for the main logic of the operator. First, it reads the channel ID and embed color from the parameters. Next, it reads the message content and the embed options from the input. Then, this function retrieves the Discord bot API token from the AI context and calls the `send_message` helper function with the necessary parameters to send the message.

The `send_message` function configures the headers and data of the post request by formatting the parameters and inputs accordingly, and sends the message to the channel. It returns the status of the message sending process as a string.
