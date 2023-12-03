import openai
import os
import sys

def main():
    openai.api_key = os.environ.get('OPENAI_API_KEY', '')

    # Get the diff from the command line arguments
    diff = sys.argv[1]

    # Split the diff into individual files
    files = diff.split('\n')

    # Example: Use the OpenAI API to generate review comments for each file in the diff
    for file in files:
        if file:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=f"Please check if there are any confusions or irregularities in the following code diff:\n\n{file}\n\nFeedback:",
                max_tokens=100000,
                temperature=1,
            )

            review_comments = response['choices'][0]['text']
            print(f"### File: {file}\n{review_comments}\n\n")

if __name__ == "__main__":
    main()
