"""
Generates the context for the simulation.
"""

def generate_context():
    """
    Generates a context dictionary with industry and location.

    For now, this returns a static context. In the future, this can be expanded
    to generate dynamic contexts.
    """
    return {
        "industry": "Industria Ganadera",
        "location": "Venezuela"
    }


if __name__ == "__main__":
    import argparse
    import json
    import os

    parser = argparse.ArgumentParser(description="Stage 1: Generate simulation context")
    parser.add_argument("--output", default="data/outputs/context_output.json",
                        help="Path to write the output JSON (default: data/outputs/context_output.json)")
    args = parser.parse_args()

    result = generate_context()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n✓ Output saved to {args.output}")
