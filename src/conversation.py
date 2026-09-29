def build_conversation_context(
    messages,
    max_messages=6
):
    """
    Convert recent chat messages into text that can
    help interpret a follow-up question.

    The government document remains the factual
    knowledge source.
    """

    try:

        if not messages:
            return ""

        recent_messages = messages[
            -max_messages:
        ]

        conversation_parts = []

        for message in recent_messages:

            role = message.get(
                "role",
                ""
            )

            content = message.get(
                "content",
                ""
            )

            if not content:
                continue

            if role == "user":
                speaker = "User"

            elif role == "assistant":
                speaker = "GovAssist"

            else:
                continue

            conversation_parts.append(
                f"{speaker}: {content}"
            )

        return "\n".join(
            conversation_parts
        )

    except Exception:

        return ""