import openai

openai.api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmODFmYzE1NS1jNGZiLTQ0MWUtYWFmNy0wMTMzYTY1NWVhMmMiLCJhdWQiOlsiZmFzdGFwaS11c2VyczphdXRoIl0sImV4cCI6MTcxNTgxMzA2Nn0.ieC9mfWMV7VmOzc9NssStOSHfUJkWESILtjUJIWaJks'
openai.base_url = "https://ericmichael-openai-playground-utrgv.hf.space/v1"

completion = openai.chat.completions.create(
    model="gpt-3.5",
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
)
print(completion.choices[0].message.content)