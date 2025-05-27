import google.generativeai as palm
import os
from dotenv import load_dotenv

load_dotenv()
palm_api_key = os.environ.get("PALM_API_KEY")

if not palm_api_key:
    print("Error: PALM_API_KEY is not set. Please check your .env file.")
    exit()

palm.configure(api_key=palm_api_key)

print("--- Listing Available Models and Supported Methods ---")
all_models = list(palm.list_models())
found_suitable_model = False
selected_model_name = None
selected_method = None

for m in all_models:
    print(f"Model Name: {m.name}")
    print(f"  Description: {m.description}")
    print(f"  Supported Methods: {m.supported_generation_methods}")
    print("-" * 30)

    # Prioritize models that support 'generateContent' (for newer Gemini)
    if 'generateContent' in m.supported_generation_methods and "gemini" in m.name:
        if not selected_model_name: # Pick the first suitable Gemini model
            selected_model_name = m.name
            selected_method = 'generateContent'
            found_suitable_model = True
    # Fallback to models that support 'generateText' (for older PaLM 2 models like text-bison)
    elif 'generateText' in m.supported_generation_methods and not selected_model_name:
        selected_model_name = m.name
        selected_method = 'generateText'
        found_suitable_model = True

if found_suitable_model:
    print(f"\n--- Automatically selected model: {selected_model_name} using method: {selected_method} ---")
    model_instance = palm.GenerativeModel(model_name=selected_model_name) # Initialize GenerativeModel for both
else:
    print("\nError: No suitable text generation model found with 'generateContent' or 'generateText'.")
    print("Please check your API key's permissions and available models.")
    exit() # Exit if no model is found

# --- Rest of your code for generate_itinerary ---

def generate_itinerary(source, destination, start_date, end_date, no_of_day):
    print(f"PALM_API_KEY is set: {bool(palm_api_key)}")
    if not model_instance:
        print("Model not initialized. Cannot generate itinerary.")
        return None

    prompt = f"Generate a personalized trip itinerary for a {no_of_day}-day trip from {source} to {destination} on {start_date} to {end_date}, with an optimum budget (Currency:INR). Please provide a detailed day-by-day plan including activities, estimated costs, and accommodation suggestions."

    try:
        if selected_method == 'generateContent':
            response = model_instance.generate_content(prompt)
        elif selected_method == 'generateText':
            # For models initialized with GenerativeModel that support generateText
            # you might need to use palm.generate_text directly if model_instance doesn't expose it
            # The GenerativeModel object typically handles this internally.
            response = model_instance.generate_content(prompt) # GenerativeModel abstracts this
            # If you *must* use palm.generate_text for older models:
            # response = palm.generate_text(model=selected_model_name, prompt=prompt)
        else:
            print(f"Unknown method {selected_method} selected.")
            return None

        print(f"API response received: {response}")

        if response and response.text:
            return response.text
        else:
            print("API response was empty or malformed.")
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'finish_reason'):
                        print(f"Finish Reason: {candidate.finish_reason}")
                    if hasattr(candidate, 'safety_ratings'):
                        print(f"Safety Ratings: {candidate.safety_ratings}")
            return None
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        return None

# Example usage (run this part to test)
if __name__ == "__main__":
    source_city = "Mumbai"
    destination_city = "Goa"
    start = "2025-06-01"
    end = "2025-06-05"
    days = 5

    print("\n--- Attempting to generate itinerary ---")
    itinerary = generate_itinerary(source_city, destination_city, start, end, days)
    if itinerary:
        print("\n--- Generated Itinerary ---")
        print(itinerary)
    else:
        print("\nFailed to generate itinerary.")