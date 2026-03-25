"""Minimal AI agent — asks Claude a question, gets an answer.

This file is instrumented with Assay. When run via `assay run`,
every API call produces a signed, tamper-evident receipt.
"""
from assay.integrations.anthropic import patch; patch()  # assay:patched
from anthropic import Anthropic


def main():
    client = Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": "What are the three laws of thermodynamics? One sentence each.",
        }],
    )
    print(response.content[0].text)


if __name__ == "__main__":
    main()
