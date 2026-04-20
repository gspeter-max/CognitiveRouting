"""Console demo for the Phase 1 persona router."""

from cognitive_routing.routing.personas import load_personas
from cognitive_routing.routing.router import route_post_to_bots
from cognitive_routing.routing.store import get_chroma_client, get_persona_collection, seed_personas
from pprint import pprint 

def main() -> None:
    """Seed the persona store and print the best routing matches for a sample post."""

    client = get_chroma_client()
    collection = get_persona_collection(client)
    seed_personas(collection, load_personas())

    post = "OpenAI just released a new model that might replace junior developers."
    matches = route_post_to_bots(collection, post)

    print(f"Post: {post}")
    print("Matches:")
    pprint(matches, indent=4)
    for match in matches:
        print(f"- {match['bot_id']} | {match['bot_name']} | {match['similarity']}")


if __name__ == "__main__":
    main()
