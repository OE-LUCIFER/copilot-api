from copilot_api import Copilot
from copilot_api.copilot import Conversation

def test_basic_chat():
    print("\n=== Testing Basic Chat ===")
    copilot = Copilot()
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Hello! Tell me a short joke."}
    ]

    for response in copilot.create_completion(
        model="Copilot",
        messages=messages,
        stream=True
    ):
        if isinstance(response, str):
            print(response, end='', flush=True)
    print("\n")


def test_web_search():
    print("\n=== Testing Web Search ===")
    copilot = Copilot()
    messages = [
        {"role": "user", "content": "Tell me about HelpingAI model"}
    ]

    for response in copilot.create_completion(
        model="Copilot",
        messages=messages,
        stream=True,
        web_search=True
    ):
        if isinstance(response, str):
            print(response, end='', flush=True)
    print("\n")

def test_conversation():
    print("\n=== Testing Conversation Management ===")
    copilot = Copilot()
    conversation = None
    
    # First message
    messages = [
        {"role": "user", "content": "Let's talk about space exploration. What's the most interesting recent discovery?"}
    ]

    print("First message:")
    for response in copilot.create_completion(
        model="Copilot",
        messages=messages,
        stream=True,
        return_conversation=True
    ):
        if isinstance(response, Conversation):
            conversation = response
        elif isinstance(response, str):
            print(response, end='', flush=True)
    print("\n")

    # Follow-up message using the same conversation
    if conversation:
        print("\nFollow-up message:")
        follow_up = [
            {"role": "user", "content": "That's interesting! Can you elaborate on the implications of this discovery?"}
        ]
        for response in copilot.create_completion(
            model="Copilot",
            messages=follow_up,
            stream=True,
            conversation=conversation
        ):
            if isinstance(response, str):
                print(response, end='', flush=True)
    print("\n")


def test_proxy():
    print("\n=== Testing Proxy Connection ===")
    copilot = Copilot()
    messages = [
        {"role": "user", "content": "make me a image of a red car"}
    ]

    # Replace with your proxy URL if needed
    proxy = None  # e.g., "http://your-proxy-server:port"
    
    for response in copilot.create_completion(
        model="Copilot",
        messages=messages,
        stream=True,
        proxy=proxy,
        timeout=30  # Custom timeout in seconds
    ):
        if isinstance(response, str):
            print(response, end='', flush=True)
    print("\n")


if __name__ == "__main__":
    print("Starting Copilot API Tests...")
    
    try:
        test_basic_chat()
        test_web_search()
        test_conversation()

        test_proxy()
        
        print("\nAll tests completed!")
        
    except Exception as e:
        print(f"\nError during testing: {str(e)}")