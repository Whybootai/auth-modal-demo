from google_oauth import app  # Import the Flask app from the google_oauth module

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
