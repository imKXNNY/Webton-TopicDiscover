from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import re
from pytrends.request import TrendReq
import pandas as pd
import time

app = Flask(__name__)
CORS(app)

# Base keywords for testing
BASE_KEYWORDS = ["python programming", "java development", "network security", "web development", "data science"]

# Utility function: Fetch autocomplete suggestions
def get_autocomplete_suggestions(keyword):
    url = "http://suggestqueries.google.com/complete/search"
    params = {"client": "firefox", "hl": "en", "q": keyword}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()[1]
        else:
            return []
    except Exception as e:
        print(f"Error fetching autocomplete for {keyword}: {e}")
        return []

# Utility function: Remove duplicates
def remove_duplicates(keywords):
    seen = set()
    unique_keywords = []
    for keyword in keywords:
        normalized = " ".join(keyword.split())
        if normalized not in seen:
            seen.add(normalized)
            unique_keywords.append(keyword)
    return unique_keywords

# Utility function: Split keywords into chunks of 5 for pytrends
def chunk_keywords(keywords, chunk_size=5):
    for i in range(0, len(keywords), chunk_size):
        yield keywords[i:i + chunk_size]

# Utility function: Analyze trends with Google Trends
def analyze_trends(keywords):
    pytrends = TrendReq(hl='en-US', tz=360)
    trends_data = pd.DataFrame()
    for chunk in chunk_keywords(keywords):
        try:
            pytrends.build_payload(kw_list=chunk, timeframe='today 12-m', geo='', gprop='')
            chunk_data = pytrends.interest_over_time()
            if not chunk_data.empty:
                trends_data = pd.concat([trends_data, chunk_data], axis=1)
            time.sleep(2)  # Rate-limit friendly delay
        except Exception as e:
            print(f"Error analyzing chunk {chunk}: {e}")
    return trends_data if not trends_data.empty else None

# Endpoint: Generate How-To keywords from autocomplete suggestions
@app.route('/generate-keywords', methods=['GET'])
def generate_keywords():
    base = request.args.get('base', "")
    base_keywords = [kw.strip() for kw in base.split(',') if kw.strip()]
    if not base_keywords:
        return jsonify({'error': 'No valid base keywords provided'}), 400
    
    howto_keywords = []
    for keyword in base_keywords:
        suggestions = get_autocomplete_suggestions(f"how to {keyword}")
        howto_keywords.extend(suggestions)
    
    unique_keywords = remove_duplicates(howto_keywords)
    return jsonify({'base_keywords': base_keywords, 'howto_keywords': unique_keywords})

# Endpoint: Analyze trends for given keywords
@app.route('/analyze-trends', methods=['POST'])
def analyze_keywords():
    keywords = request.json.get('keywords', [])
    if not keywords:
        return jsonify({'error': 'No keywords provided'}), 400

    trends_data = analyze_trends(keywords)
    if trends_data is not None:
        trends_json = trends_data.reset_index().to_dict(orient='records')
        return jsonify({'trends': trends_json})
    else:
        return jsonify({'error': 'No trends data available'})

if __name__ == '__main__':
    app.run(debug=True)
