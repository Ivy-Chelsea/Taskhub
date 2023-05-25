#!/usr/bin/python3
"""A WEB APPLICATION THAT RETURNS 
INFORMATION FROM A RESUME
"""

from flask import Flask
from flask import render_template,make_response

app=Flask(__name__)


@app.route('/',strict_slashes=False)
def index():
    return "<h2>welcome to the homepage<h2>"

@app.errorhandler(404)
"""404 Error Handler"""
def not_found(error):
     return make_response(jsonify({'error': 'Not found try again'}), 404)


if __name__ == '__main__':
    app.run(host="0.0.0",port=5000,debug=True)

