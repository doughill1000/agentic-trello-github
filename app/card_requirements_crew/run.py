import os
from app.card_requirements_crew.crew import CardRequirementsCrew

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run(inputs):
    """
    Run the research crew.
    """

    print("Kickoff")
    print(inputs)

    # Create and run the crew
    try:
        result = CardRequirementsCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")

    return result