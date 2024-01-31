import ollama


modelfile = """
FROM llama2
SYSTEM Turn every input into a paragraph of informative blog. Make the English simple and the paragraph extremely short.
"""

ollama.create(model="blog", modelfile=modelfile)


stream = ollama.chat(
    model="blog",
    messages=[{"role": "user", "content": "UX design is hard"}],
    stream=True,
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
