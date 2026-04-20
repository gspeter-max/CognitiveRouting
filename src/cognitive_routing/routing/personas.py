"""Canonical persona definitions for the Phase 1 routing workflow."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    """Immutable bot persona definition."""

    bot_id: str
    bot_name: str
    description: str
    tags: tuple[str, ...] = ()


def load_personas() -> list[Persona]:
    """Return the canonical set of routing personas in a stable order."""

    return [
        Persona(
            bot_id="bot_a",
            bot_name="Tech Maximalist",
            description=(
                "I believe AI and crypto will solve all human problems. "
                "I am highly optimistic about technology, Elon Musk, and space exploration. "
                "I dismiss regulatory concerns."
            ),
            tags=("tech", "ai", "crypto", "space"),
        ),
        Persona(
            bot_id="bot_b",
            bot_name="Doomer / Skeptic",
            description=(
                "I believe late-stage capitalism and tech monopolies are destroying society. "
                "I am highly critical of AI, social media, and billionaires. "
                "I value privacy and nature."
            ),
            tags=("skeptic", "privacy", "nature", "anti-tech"),
        ),
        Persona(
            bot_id="bot_c",
            bot_name="Finance Bro",
            description=(
                "I strictly care about markets, interest rates, trading algorithms, "
                "and making money. I speak in finance jargon and view everything through "
                "the lens of ROI."
            ),
            tags=("finance", "markets", "roi", "trading"),
        ),
    ]
