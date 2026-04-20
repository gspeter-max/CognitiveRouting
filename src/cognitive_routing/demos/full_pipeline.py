"""Console demo for the full Phase 1 -> Phase 2 pipeline."""

from cognitive_routing.pipeline.full_pipeline import run_full_pipeline
from pprint import pprint 

def main() -> None:
    """Route one input post to a persona and generate the final structured result."""

    post = "OpenAI just released a new model that might replace junior developers."
    result = run_full_pipeline(post)
    print("Full pipeline result:")
    pprint(result, indent=4)


if __name__ == "__main__":
    main()
