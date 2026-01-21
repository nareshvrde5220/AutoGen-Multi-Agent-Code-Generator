import openai
import os

# Initialize OpenAI client
# Get API key from environment variable
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')  # Set your API key as environment variable
)

# Sample user request
response = client.chat.completions.create(
    model='gpt-4o',
    max_completion_tokens=1024,
    messages=[
        {'role': 'user', 'content': 'Write a Python function to check if a number is prime.'}
    ]
)

# Print the response
print(response.choices[0].message.content)