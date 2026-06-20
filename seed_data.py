import requests
import time

API_URL = "http://localhost:8000"

test_queries = [
    "What is the limitation of liability?", "What is the governing law of the contract?",
    "How can the agreement be terminated?", "What happens to my data upon termination?",
    "What is the notice period for termination?", "Does AWS guarantee service availability?",
    "What are the payment terms?", "How are taxes handled under this agreement?",
    "What is the definition of Service Offerings?", "Are there any indemnification obligations?",
    "What is the limitation of liability?", "What is the governing law of the contract?",
    "How can the agreement be terminated?", "What are the payment terms?",
    "What happens to my data upon termination?", "What is the notice period for termination?",
    "Does AWS guarantee service availability?", "What is the definition of Service Offerings?",
    "Are there any indemnification obligations?", "What is the limitation of liability?",
    "What is the capital city of France?", "How do I cook a perfect medium-rare steak?",
    "What is the weather like in New York today?", "Can you write a poem about artificial intelligence?",
    "Who won the FIFA World Cup in 2022?", "How do I repair a flat tire on a bicycle?",
    "What is the distance between the Earth and the Moon?", "Can you recommend a good action movie from 2025?",
    "What are the main rules of chess?", "How do I learn how to play guitar?"
]

if __name__ == "__main__":
    print(f"Seeding database with {len(test_queries)} mock requests...")
    for i, q in enumerate(test_queries, start=1):
        try:
            requests.post(f"{API_URL}/ask", json={"query": q})
            print(f"[{i}/30] Sent: {q[:30]}...")
        except Exception:
            print("Backend unreachable. Start the FastAPI application first.")
            break
        time.sleep(0.1)