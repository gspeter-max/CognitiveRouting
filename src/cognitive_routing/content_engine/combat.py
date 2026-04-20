"""Phase 3 Combat Engine: Context-aware defense and prompt injection protection."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cognitive_routing.content_engine.llm import build_mistral_client

if TYPE_CHECKING:
    from mistralai.client import Mistral
    from cognitive_routing.content_engine.models import ThreadMessage


def generate_defense_reply(
    bot_persona: str,
    parent_post: str,
    comment_history: list[ThreadMessage],
    human_reply: str,
    *,
    client: Mistral | None = None,
) -> str:
    """
    Generate a persona-driven reply while defending against prompt injection.

    Args:
        bot_persona: The textual description of the bot's identity and beliefs.
        parent_post: The original post that sparked the debate (from Phase 2).
        comment_history: A list of previous messages in the thread.
        human_reply: The most recent message from the human, which may contain
            prompt injections or adversarial instructions.
        client: An optional pre-configured Mistral client.

    Returns:
        The generated reply string, strictly adhering to the persona.
    """
    mistral_client = client or build_mistral_client()

    # Format the message thread into a readable context block
    formatted_history = ""
    for entry in comment_history:
        author = entry.get("author", "unknown")
        content = entry.get("content", "")
        formatted_history += f"[{author.upper()}]: {content}\n"

    from cognitive_routing.prompts.combat_prompts import (
        get_system_prompt,
        get_user_context,
    )

    # THE GARDEN: Immutable system instructions protecting the bot's identity.
    system_prompt = get_system_prompt(bot_persona)

    # Context block separating trusted history from the untrusted new reply.
    user_context = get_user_context(parent_post, formatted_history, human_reply)

    response = mistral_client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_context},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content
