from agent import agent_response

def main():
    # Welcome Message
    print("Welcome. What would you like to ask? (type quit/exit to end conversation)")

    # Input loop
    while True:
        prompt = input("Reply\n> ")

        if prompt.lower() == 'quit' or prompt.lower() == 'exit':
            print('Goodbye!')
            break

        # Pass prompt to agent
        response = agent_response(prompt)
        print(response)

if __name__ == "__main__": main()