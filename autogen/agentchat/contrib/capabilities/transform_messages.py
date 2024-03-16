import sys
from typing import Dict, List, Optional, Protocol, Union

import tiktoken
from termcolor import colored

from autogen import ConversableAgent, token_count_utils
from autogen import code_utils


class MessageTransform(Protocol):
    """Defines a contract for message transformation.

    Classes implementing this protocol should provide an `apply_transform` method
    that takes a list of messages and returns the transformed list.
    """

    def apply_transform(self, messages: List[Dict]) -> List[Dict]:
        """Applies a transformation to a list of messages.

        Args:
            messages: A list of dictionaries representing messages.

        Returns:
            A new list of dictionaries containing the transformed messages.
        """
        ...


class TransformMessages:
    """Agent capability for transforming messages before reply generation.

    This capability allows you to apply a series of message transformations to
    a ConversableAgent's incoming messages before they are processed for response
    generation. This is useful for tasks such as:

    - Limiting the number of messages considered for context.
    - Truncating messages to meet token limits.
    - Filtering sensitive information.
    - Customizing message formatting.

    To use `TransformMessages`:

    1. Create message transformations (e.g., `MaxMessagesTransform`, `TruncateMessageTransform`).
    2. Instantiate `TransformMessages` with a list of these transformations.
    3. Add the `TransformMessages` instance to your `ConversableAgent` using `add_to_agent`.

    NOTE: Order of message transformations is important. You could get different results based on
        the order of transformations.

    Example:
        ```python
        from agentchat import ConversableAgent
        from agentchat.contrib.capabilities import TransformMessages, MaxMessagesTransform, TruncateMessageTransform

        max_messages = MaxMessagesTransform(max_messages=2)
        truncate_messages = TruncateMessageTransform(max_tokens=500)
        transform_messages = TransformMessages(transforms=[max_messages, truncate_messages])

        agent = ConversableAgent(...)
        transform_messages.add_to_agent(agent)
        ```
    """

    def __init__(self, *, transforms: List[MessageTransform] = []):
        """
        Args:
            transforms: A list of message transformations to apply.
        """
        self._transforms = transforms

    def add_to_agent(self, agent: ConversableAgent):
        """Adds the message transformations capability to the specified ConversableAgent.

        This function performs the following modifications to the agent:

        1. Registers a hook that automatically transforms all messages before they are processed for
            response generation.
        """
        agent.register_hook(hookable_method="process_all_messages_before_reply", hook=self._transform_messages)

    def _transform_messages(self, messages: List[Dict]) -> List[Dict]:
        temp_messages = messages.copy()
        system_message = None

        if messages[0]["role"] == "system":
            system_message = messages[0].copy()
            temp_messages.pop(0)

        for transform in self._transforms:
            temp_messages = transform.apply_transform(temp_messages)

        if system_message:
            temp_messages.insert(0, system_message)

        self._print_stats(messages, temp_messages)

        return temp_messages

    def _print_stats(self, pre_transform_messages: List[Dict], post_transform_messages: List[Dict]):
        pre_transform_messages_len = len(pre_transform_messages)
        post_transform_messages_len = len(post_transform_messages)

        if pre_transform_messages_len < post_transform_messages_len:
            print(
                colored(
                    f"Number of messages reduced from {pre_transform_messages_len} to {post_transform_messages_len}.",
                    "yellow",
                )
            )


class MessageHistoryLimiter:
    """Limits the number of messages considered by an agent for response generation."""

    def __init__(self, max_messages: Optional[int] = None):
        """
        Args:
            max_messages (None or int): Maximum number of messages to keep in the context.
            Must be greater than 0 if not None.
        """
        self._validate_max_messages(max_messages)
        self._max_messages = max_messages if max_messages else sys.maxsize

    def apply_transform(self, messages: List[Dict]) -> List[Dict]:
        if self._max_messages is None:
            return messages

        processed_messages = messages[-self._max_messages :]
        print(f"len of messages: {len(processed_messages)}")
        return processed_messages

    def _validate_max_messages(self, max_messages: Optional[int]):
        if max_messages is not None and max_messages < 1:
            raise ValueError("max_messages must be None or greater than 1")


class MessageTokenLimiter:
    """Truncates messages to meet token limits for efficient processing and response generation.

    This class allows you to control the length of messages an agent receives and considers for response.
    Truncation can be applied to individual messages or the entire conversation history
    """

    def __init__(
        self,
        max_tokens_per_message: Optional[int] = None,
        max_tokens: Optional[int] = None,
        model: str = "gpt-3.5-turbo-0613",
    ):
        """
        Args:
            max_tokens_per_message (None or int): Maximum number of tokens to keep in each message.
                Must be greater than or equal to 0 if not None.
            max_tokens (Optional[int]): Maximum number of tokens to keep in the chat history.
                Must be greater than or equal to 0 if not None.
            model (str): The target OpenAI model for tokenization alignment.
        """
        self._validate_max_tokens(max_tokens_per_message)
        self._validate_max_tokens(max_tokens)

        self._max_tokens_per_message = max_tokens_per_message if max_tokens_per_message else sys.maxsize
        self._max_tokens = max_tokens if max_tokens else sys.maxsize
        self._model = model

    def apply_transform(self, messages: List[Dict]) -> List[Dict]:
        assert self._max_tokens_per_message is not None
        assert self._max_tokens is not None

        temp_messages = messages.copy()
        processed_messages = []
        processed_messages_tokens = 0

        # calculate tokens for all messages
        total_tokens = sum(token_count_utils.count_token(msg["content"]) for msg in temp_messages)

        for msg in reversed(temp_messages):
            msg["content"] = self._truncate_str_to_tokens(
                msg["content"], self._max_tokens_per_message, model=self._model
            )
            msg_tokens = token_count_utils.count_token(msg["content"])

            if processed_messages_tokens + msg_tokens > self._max_tokens:
                break

            # append the message to the beginning of the list to preserve order
            processed_messages_tokens += msg_tokens
            processed_messages.insert(0, msg)

        if total_tokens > processed_messages_tokens:
            print(
                colored(
                    f"Truncated {total_tokens - processed_messages_tokens} tokens. Tokens reduced from {total_tokens} to {processed_messages_tokens}",
                    "yellow",
                )
            )

        return processed_messages

    def _truncate_str_to_tokens(self, text: Union[str, List], max_tokens: int, model: str = "gpt-3.5-turbo-0613"):
        """Truncate a string so that the number of tokens is less than or equal to max_tokens using tiktoken.

        Args:
            text: The string to truncate.
            max_tokens: The maximum number of tokens to keep.
            model: The target OpenAI model for tokenization alignment.

        Returns:
            The truncated string.
        """

        encoding = tiktoken.encoding_for_model(model)  # Get the appropriate tokenizer

        encoded_tokens = encoding.encode(code_utils.content_str(text))
        truncated_tokens = encoded_tokens[:max_tokens]
        truncated_text = encoding.decode(truncated_tokens)  # Decode back to text

        return truncated_text

    def _validate_max_tokens(self, max_tokens: Optional[int] = None):
        if max_tokens is not None and max_tokens < 0:
            raise ValueError("max_tokens and max_tokens_per_message must be None or greater than or equal to 0")