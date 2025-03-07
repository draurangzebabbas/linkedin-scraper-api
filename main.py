from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API is running!"})

@app.route('/linkedin', methods=['GET'])
def scrape_profile():
    profile_url = request.args.get('url')
    if not profile_url:
        return jsonify({"success": False, "message": "URL is required"}), 400

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(profile_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        websites = []
        links = soup.find_all('a', href=True)
        for link in links:
            url = link['href']
            if url.startswith('http'):
                websites.append({"url": url, "category": "OTHER"})

        return jsonify({
            "success": True,
            "statusCode": 200,
            "message": "Data retrieved successfully",
            "data": {
                "emailAddress": None,
                "phoneNumber": None,
                "websites": websites
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
