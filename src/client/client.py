"""
A test script to call the local server using LiteLLM.

NOTE: The litellm libraries support of types is not fully implemented yet,
and as such the type: ignore comments are used to suppress type checking errors.
"""

from litellm import completion  # type: ignore


def run_litellm_non_stream():
    """Calls local server in non-stream mode using LiteLLM."""
    try:
        response = completion(  # type: ignore
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Create a fibonacci function in Python"}
            ],
            stream=False,
        )
        print("Non-streaming response:", response)  # type: ignore
    except Exception as e:
        print("Error in non-stream mode:", e)


def run_litellm_stream():
    """Calls local server in stream mode using LiteLLM."""
    try:
        response_stream = completion(  # type: ignore
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Create a fibonacci function in Python"}
            ],
            stream=True,
        )
        print("Streaming response:")
        for chunk in response_stream:  # type: ignore
            print(chunk, end="", flush=True)  # type: ignore
    except Exception as e:
        print("Error in streaming mode:", e)


if __name__ == "__main__":
    print("Running LiteLLM Client Non-Stream Mode:")
    run_litellm_non_stream()
    print("\nRunning LiteLLM Client Stream Mode:")
    run_litellm_stream()
