# 🧠 Chat with MongoDB using Gemini + LangChain

This project allows you to **query your MongoDB database using plain English**.  
It uses **Google Gemini (via LangChain)** to automatically generate MongoDB aggregation pipelines, execute them, and display the results neatly in your terminal.

---

## 🚀 Features

✅ Convert natural language to MongoDB aggregation pipelines  
✅ Use **Google Gemini** for intelligent query generation  
✅ Execute pipelines automatically on MongoDB collections  
✅ Display query results as **formatted tables** using `tabulate`  
✅ Summarize query results in human-readable text  
✅ Clean console output — no verbose debugging logs  
✅ Suppresses deprecated LangChain warnings  

---

## 🧩 Tech Stack

| Component | Description |
|------------|-------------|
| **Python 3.10+** | Programming language |
| **MongoDB** | Database for query execution |
| **LangChain** | LLM framework for chaining components |
| **Google Gemini API** | Large Language Model used for query generation |
| **tabulate** | Displays MongoDB results in tabular format |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/chat-with-mongodb.git
cd chat-with-mongodb
2️⃣ Install Dependencies
## pip install pymongo langchain langchain-google-genai google-generativeai tabulate
3️⃣ Authenticate Google Gemini
Set up Google Cloud authentication for Gemini access:
gcloud auth application-default login
Ensure you have enabled the Generative Language API in your Google Cloud project.
4️⃣ Setup MongoDB
use chat_with_mongodb
<img width="541" height="206" alt="image" src="https://github.com/user-attachments/assets/ae661ece-d806-4f4b-9a90-d11ee79a907f" />
db.users.insertMany([
  { "name": "Alice", "age": 28 },
  { "name": "Bob", "age": 34 },
  { "name": "Charlie", "age": 22 }
])
5️⃣ Run the Script
python chat_with_mongodb.py
Example 1 : Find all users older than 25
🧾 Example Output:
✅ Credentials found! You can now call Gemini APIs.
🧠 Aggregation pipeline generated: [{'$match': {'age': {'$gt': 25}}}]

💬 LLM Summary:
Found 2 users older than 25: Alice and Bob.

📊 Table:

+----------+-------+
| name     | age   |
+----------+-------+
| Alice    | 28    |
| Bob      | 34    |
+----------+-------+

Example 2: Now show me only their names
🧾 Example Output
✅ Credentials found! You can now call Gemini APIs.
🧠 Aggregation pipeline generated: [{'$match': {'age': {'$gt': 25}}}]

💬 LLM Summary:
Found 2 users older than 25: Alice and Bob.

📊 Table:

+----------+-------+
| name     | age   |
+----------+-------+
| Alice    | 28    |
| Bob      | 34    |
+----------+-------+



👨‍💻 Author
Prasanna J
AI & Software Developer | Python • Django • MongoDB • LangChain • LLMs
📧 Email: prasanna@example.com
🌐 LinkedIn: linkedin.com/in/prasannajk8
💼 GitHub: github.com/PrasannaJK8
