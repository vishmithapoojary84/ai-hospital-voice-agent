from agent import chat

while True:

    message = input("You: ")

    if message.lower() == "exit":
        break

    response = chat(message)

    print("\nAI:", response)