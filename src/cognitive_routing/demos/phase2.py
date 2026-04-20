"""Console demo for the Phase 2 autonomous content engine."""

from cognitive_routing.content_engine.graph import generate_original_post
from cognitive_routing.routing.personas import load_personas


def main() -> None:
    """Generate one original post for the first canonical persona."""

    persona = load_personas()[0]
    result = generate_original_post(persona.bot_id, persona.description)
    print("Phase 2 result:")
    print(result)


if __name__ == "__main__":
    main()
