import os
import requests
import streamlit as st

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found.")
    st.stop()

client = genai.Client(api_key=api_key)



st.title("AI Web Scraper")

url = st.text_input("Enter a website URL:")


if st.button("Scrape"):

    if not url:
        st.warning("Please enter a URL.")
        st.stop()

    try:

        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(" ", strip=True)


        text = text[:10000]

        st.write("Webpage scraped successfully!")

        prompt = f"""
        Summarize this webpage in simple words.
        
        Webpage:
        {text}
        """

        result = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        st.subheader("AI Summary")
        st.write(result.text)

    except Exception as e:
        st.error(f"Something went wrong: {e}")