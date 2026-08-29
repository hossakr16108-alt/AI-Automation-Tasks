import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def test_ollama():
    prompt = "Explain what a website is in one short sentence."

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        print("=" * 50)
        print("OLLAMA CONNECTION TEST")
        print("=" * 50)
        print()

        print("Ollama response:")
        print(result["response"])

        print()
        print("Connection successful!")
        print("=" * 50)

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to Ollama.")
        print("Make sure Ollama is running.")

    except requests.exceptions.Timeout:
        print("ERROR: Ollama took too long to respond.")

    except requests.exceptions.RequestException as error:
        print(f"ERROR: Request failed: {error}")

    except KeyError:
        print("ERROR: Ollama returned an unexpected response.")


if __name__ == "__main__":
    test_ollama()