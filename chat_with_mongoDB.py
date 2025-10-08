from pymongo import MongoClient
import json, re
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from tabulate import tabulate  # ✅ pip install tabulate
# --- MongoDB setup ---
client = MongoClient("mongodb://localhost:27017/")
db = client["chat_with_mongodb"]
collection = db["users"]

# --- Gemini setup ---
genai.configure()  # Uses Application Default Credentials
print("✅ Credentials found! You can now call Gemini APIs.")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_retries=2,
)

# --- Memory setup ---
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# --- Prompt template ---
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are an expert MongoDB engineer. ALWAYS respond with ONLY a valid JSON array (a MongoDB aggregation pipeline). "
        "Do NOT include explanations, comments, or markdown. Return the result in table format so that user can easily read it."
    ),
    HumanMessagePromptTemplate.from_template(
        "Database: chat_with_mongodb, collection: users. Fields: name (str), age (int).\n\n"
        "Conversation so far:\n{history}\n\n"
        "User query: {input}"
    )
])

# --- Conversation chain ---
conversation = ConversationChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    verbose=False
)

# --- JSON cleaning helpers ---
def clean_code_fences(text: str) -> str:
    # Capture only the inner content inside code fences
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.S | re.IGNORECASE)
    if match:
        cleaned = match.group(1).strip()
        return cleaned
    return text.strip()

def extract_first_json_array(text: str):
    text = clean_code_fences(text)
    if not text.strip().startswith("["):
        text = "[" + text + "]"
    try:
        return json.loads(text)
    except Exception:
        fixed = re.sub(r",(\s*[}\]])", r"\1", text)
        return json.loads(fixed)

def clean_and_parse_json(text: str):
    try:
        return json.loads(text)
    except:
        return extract_first_json_array(text)

# --- Query function ---
def query_to_aggregation(user_query):
    response = conversation.predict(input=user_query)
    text = response.strip()

    try:
        pipeline = clean_and_parse_json(text)
    except ValueError as e:
        raise ValueError(f"❌ Failed to parse JSON:\n{text}\nError: {e}")

    if not isinstance(pipeline, list):
        raise ValueError(f"Parsed JSON is not a list. Got: {type(pipeline)}")

    return pipeline

def summarize_results(user_query, results):
    if not results:
        return "No results found."

    # Only summarize small datasets (to avoid long prompts)
    if len(results) <= 10:
        summary_prompt = f"""
        The user asked: "{user_query}"
        Here are the MongoDB query results:
        {json.dumps(results, indent=2)}

        Please summarize or present these results in a human-readable table or bullet list.
        """
        summary = llm.invoke(summary_prompt)
        return summary.content if hasattr(summary, "content") else summary
    else:
        return f"Found {len(results)} results. Displaying raw table below:"


def run_query(user_query):
    pipeline = query_to_aggregation(user_query)
    results = list(collection.aggregate(pipeline))
    for doc in results:
        doc.pop("_id", None)

    print("🧠 Aggregation pipeline generated:", pipeline)

    summary = summarize_results(user_query, results)
    print("\n💬 LLM Summary:\n", summary)
    # fallback display
    if len(results) > 0:
        print("\n📊 Table:\n")
        print(tabulate(results, headers="keys", tablefmt="grid"))
    return results


# --- Example usage ---
print(run_query("Find all users age greather than 25"))
print(run_query("Now show me only their names"))