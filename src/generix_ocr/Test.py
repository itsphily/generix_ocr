import ollama

try:
    response = ollama.chat(
        model='llama3.2-vision',
        messages=[{
            'role': 'user',
            'content': 'Hello'
        }]
    )
except Exception as e:
    print(f"Error: {str(e)}") 