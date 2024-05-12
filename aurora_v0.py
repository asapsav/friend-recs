from flask import Flask, request, render_template, jsonify
import os
from exa_py import Exa
from groq import Groq
import dotenv
dotenv.load_dotenv()

app = Flask(__name__)

exa = Exa(api_key=os.environ["EXA_API_KEY"])

def get_tweet_recommendation(query):
    result = exa.search(
        query,
        type="neural",
        num_results=5,
        category="tweet",
        start_published_date="2024-04-11T23:56:52.888Z",
        end_published_date="2024-05-11T23:56:52.888Z"
    )
    urls = [item.url for item in result.results]
    return urls

def get_topics(chunk):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"extract topics from this conversation: {chunk}"}
        ],
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    content = request.json['text']
    topics = get_topics(content)
    recommendations = get_tweet_recommendation(topics)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
