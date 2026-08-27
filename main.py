import streamlit as st 
from scraper import get_website_content,urls_filter
from ai_engine import comparison_analysis

st.title('🌐 Ai Competitor Analyzer')
st.write("please Enter your Websites Urls List")
urls_List= st.text_area("Urls are:   ")

if st.button('Analyze'):
  if urls_List:
     urls_List=urls_List.split()
     filtered_urls=urls_filter(urls_List)
     if filtered_urls:
        with st.spinner("Analyzing websites"):
           website_content= get_website_content(filtered_urls)
           ollama_analysis=comparison_analysis(website_content)
           st.markdown(ollama_analysis)
     else: 
         st.error("There are no valid urls")
else :
    st.write("Please enter at least one URL!")     
 
 
 