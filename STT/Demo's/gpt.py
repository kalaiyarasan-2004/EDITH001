import openai

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = 'sk-proj-xTcbBLifyZuezaxgRAbVT3BlbkFJZ2IQHISJAdp1K2mIkz8Q'

def get_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']

# Example usage
if __name__ == "__main__":
    user_input = input("You: ")
    response = get_chatgpt_response(user_input)
    print(f"ChatGPT: {response}")
