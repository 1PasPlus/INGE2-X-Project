import requests

API_TOKEN = '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'
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()
    except Exception as e:
        print(f"Error making API call: {e}")
        return None

def summarize_in_tweet(text_input):
  inference = "Summarize this text in a powerful tweet (280 characters max) : "
  text = text_input + '\n' + inference

  output = query({
      "inputs": text,
      "parameters": {"return_full_text": False,}
  })

  if output is None:
      print("Error calling the API. Could not summarize the text.")
      return

  if isinstance(output, list):
      # Assuming the first element in the list contains the summarized text
      rewritten_text = output[0].get('generated_text')
      # Try different key names if 'generated_text' is missing
      if not rewritten_text:
          rewritten_text = output[0].get('summary')  # Try 'summary'
          if not rewritten_text:
              rewritten_text = output[0].get('summarized_content')  # Try 'summarized_content'

      # Check character count and loop with control (max 3 attempts)
      loop_count = 0
      while len(rewritten_text) > 280 and loop_count < 3:
          print(f"Summary too long ({len(rewritten_text)} characters). Requesting shorter version...")
          # You can optionally modify the inference prompt here.
          inference = "Summarize this text in an even shorter tweet (280 characters max) : "
          text = text_input + '\n' + inference
          output = query({
              "inputs": text,
              "parameters": {"return_full_text": False,}
          })
          if output is None:
              print("Error calling the API. Skipping further attempts.")
              break
          rewritten_text = output[0].get('generated_text')
          loop_count += 1

      if rewritten_text:
          print(rewritten_text, "Le nombre de est de : ",len(rewritten_text))
      else:
          print("Could not extract summarized text after retries. Check API response format.")
  else:
      print("Unexpected response format. Could not extract summarized text.")

text_input = "Bitcoin is a decentralized digital currency, created in 2009 by a developer or group of developers under the pseudonym Satoshi Nakamoto. It is a peer-to-peer payment system that operates without a central bank or intermediary. Bitcoin is a promising technology with the potential to revolutionize the global financial system. However, it is important to understand its advantages and disadvantages before using it."

summarize_in_tweet(text_input)
