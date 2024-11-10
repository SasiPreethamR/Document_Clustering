import requests
import json
import streamlit as st


st.title('Document Classification')



def categorize(doc):
    url = "http://crmgpu5-10042:8000/cluster"
    
    payload = json.dumps({
      "document": doc
    })
    headers = {
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['result']


doc = st.text_area('Input your document here...', height=500)




if st.button('Find Category') and doc.strip():
    st.code(categorize(doc))


