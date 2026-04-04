from google import genai
import os
from dotenv import load_dotenv

load_dotenv()


def ask_gemini(text):
    # This client will auto fetch the gemini api key named GEMINI_API_KEY from environment
    client = genai.Client()
    # uploading the file to the gemini, this is the rule book.
    # uploaded_file = client.files.upload(file=file_path)
    prompt = f"""{text}"""
    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=[prompt])
    print(response.text)
    return response.text

# ask_gemini("give me the structured data if there is query for expense."
#            "aaloo 490"
#            "pyaj 239"
#            "baigan 29"
#            'give me in the [{"type":"expense", "things":"aallo", amount:money}, {same for pyaj}]')
