

def get_max_tokens_for_model(model_name: str) -> int:
    token_limits = {
        "gpt-3.5-turbo": 4096,
        "gpt-4": 8192,
        "gpt-4-32k": 32768,
    }

    max_tokens = token_limits.get(model_name)

    if max_tokens is None:
        raise ValueError(f"Model '{model_name}' is not supported. Please use one of the supported models: {', '.join(token_limits.keys())}")

    return max_tokens
