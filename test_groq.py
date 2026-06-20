from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os 


load_dotenv()


api_key = os.getenv("GROQ_API_KEY", "")
model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

if not api_key or api_key == "gsk_your-actual-key-here":
    print("ERROR: Set you GROQ_API_KEY in the .env file first!")
    print("Get a free key at: https://console.groq.com/keys")
    exit(1)

print(f"Testing Groq API with model: {model}")
print("=" * 50)


llm = ChatGroq(
    model=model,
    api_key=api_key,
    temperature=0,
)

response = llm.invoke("What is 2 + 2 ? Reply in one word only.")


print(f"Groq says: {response.content}")
print()
print("SUCCESS! Groq is working. you can now run the full project.")