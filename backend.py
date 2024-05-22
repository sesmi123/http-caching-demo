import hashlib
from flask import Flask, jsonify, make_response, request
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/no-store')
def no_store():
    response = make_response(jsonify({"data": "This response should not be stored", "timestamp": datetime.now()}))
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/private')
def private_cache():
    response = make_response(jsonify({"data": "This response is private and cached for maximum of 60 seconds", "timestamp": datetime.now()}))
    response.headers['Cache-Control'] = 'private, max-age=60'
    return response

@app.route('/no-cache')
def no_cache():
    response = make_response(jsonify({"data": "This response has no cache", "timestamp": datetime.now()}))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/max-age')
def max_age():
    response = make_response(jsonify({"data": "This response is cached for maximum of 30 seconds", "timestamp": datetime.now()}))
    response.headers['Cache-Control'] = 'public, max-age=30'
    return response

@app.route('/immutable')
def immutable():
    response = make_response(jsonify({"data": "This response is immutable and cached for upto 1 year", "timestamp": datetime.now()}))
    response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    return response

def generate_etag(data):
    return hashlib.md5(data.encode('utf-8')).hexdigest()

@app.route('/etag')
def etag_example():
    data = "This response supports ETag"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_data = f"{data} at {timestamp}"
    
    # Generate ETag for the current data
    etag = generate_etag(full_data)
    
    # Check if the client sent the correct ETag
    client_etag = request.headers.get('If-None-Match')
    if client_etag and client_etag == etag:
        return '', 304  # Not Modified
    
    response = make_response(jsonify({"data": full_data}))
    response.headers['ETag'] = etag
    response.headers['Cache-Control'] = 'private, max-age=30'
    return response

@app.route('/vary')
def vary():
    language = request.headers.get('Accept-Language', 'en')
    data = {"data": "This response varies based on language", "lang": language}
    response = make_response(jsonify(data))
    response.headers['Vary'] = 'Accept-Language'
    response.headers['Cache-Control'] = 'private, max-age=30'
    return response

if __name__ == '__main__':
    app.run(debug=True)
