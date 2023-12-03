import openai
import requests
import os

def generate_code_review(pr_number):
    # Get the PR diff using GitHub API
    response = requests.get(
        f"https://api.github.com/repos/{os.environ.get('GITHUB_REPOSITORY')}/pulls/{pr_number}",
        headers={"Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN')}"}
    )
    diff = response.json().get('diff')

    # Generate code review using OpenAI
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=diff,
        max_tokens=200,
        temperature=0.7,
        n=1,
        stop=None
    )

    code_review = response.choices[0].text.strip()
    return code_review

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--pr-number', type=str, required=True)
    args = parser.parse_args()

    code_review = generate_code_review(args.pr_number)
    print(code_review)
