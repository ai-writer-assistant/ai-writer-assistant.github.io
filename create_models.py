import ollama


modelfile = """
FROM llama2
SYSTEM Rewrite the following into a paragraph of a blog with simple yet formal English.
"""

ollama.create(model="blog", modelfile=modelfile)


stream = ollama.chat(
    model="blog",
    messages=[{"role": "user", "content": "UX design is hard"}],
    stream=True,
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
