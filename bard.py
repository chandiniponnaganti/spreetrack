import google.generativeai as palm
import os
from dotenv import load_dotenv
    
# Load the environment variables
load_dotenv()
palm_api_key = os.environ.get("PALM_API_KEY")


# Create a config.
palm.configure(api_key=palm_api_key)
model = palm.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
models = list(palm.list_models())
for m in models:
    print(m)


# Generate some text.
def generate_itinerary(source, destination, start_date, end_date, no_of_day):
    print(f"PALM_API_KEY is set: {bool(palm_api_key)}")
    prompt = f"Generate a personalized trip itinerary for a {no_of_day}-day trip from {source} to {destination} on {start_date} to {end_date}, with an optimum budget (Currency:INR)."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        return None
