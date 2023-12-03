import openai
import sys
import os

def generate_comment(api_key, file_path):
    # Set the OpenAI API key
    openai.api_key = api_key

    # Load the code from the changed file
    with open(file_path, "r") as file:
        code = file.read()

    # Generate code review comment using ChatGPT
    prompt = f"Review the following code:\n\n{code}\n\nComments:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150,
        n=1,
    )

    # Extract the generated comment from the response
    comment = response.choices[0].text.strip()

    return comment

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_comment.py <api_key> <file_path>")
        sys.exit(1)

    api_key = sys.argv[1]
    file_path = sys.argv[2]

    comment = generate_comment(api_key, file_path)
    print(comment)
