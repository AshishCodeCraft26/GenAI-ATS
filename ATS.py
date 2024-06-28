import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv() ## load all our environment variables

groq_api_key = os.getenv("GROQ_API_KEY")

model = 'llama3-8b-8192'

def get_prompt():

    system = "You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of ATS functionality"

    human = "{text}"
    prompt_template = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    return prompt_template

def generate(model, human_text):

    prompt_template = get_prompt()

    groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name=model,
            temperature=0,
    )
    chain = prompt_template | groq_chat
    output = chain.invoke({"text": f"{human_text}"})

    return output

def preprocess_text(text):
    text = text.content
    # Split the text into sections based on "\n\n"
    sections = text.split("\n\n")
    
    # Format each section
    formatted_sections = []
    for section in sections:
        lines = section.split("\n")
        formatted_lines = [line.strip() for line in lines if line.strip()]
        formatted_sections.append("\n".join(formatted_lines))
    
    # Join the formatted sections with "\n\n" to reconstruct the text
    formatted_text = "\n\n".join(formatted_sections)
    
    return formatted_text


def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

# input_prompt=f"""
# Hey Act Like a skilled or very experience ATS(Application Tracking System)
# with a deep understanding of tech field,software engineering,data science ,data analyst
# and big data engineer. Your task is to evaluate the resume based on the given job description.
# You must consider the job market is very competitive and you should provide 
# best assistance for improving thr resumes. Assign the percentage Matching based 
# on Jd and
# the missing keywords with high accuracy
# resume:{text}
# description:{jd}

# I want the response in one single string having the structure
# {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
# """

st.set_page_config(layout='wide',
                   page_title="ATS")


with st.sidebar:
     
    st.header('How to use :bulb:')
    st.markdown(":one:  Enter the Job Description in the provided text area.")
    st.markdown(":two:  Edit the Job Description as per the requirements :speech_balloon:")
    st.markdown(":three: Upload the resumes 📄")
    st.markdown(f":four:  After uploading the resumes, click Filter Resumes to begin the filtering process. If you need to stop midway, simply press the Reset button.")

    
st.title(":robot_face: AI-Powered ATS")
st.markdown("AI-powered Application Tracking System (ATS)! Harnessed the power of generative AI LLM models, we revolutionize recruitment by seamlessly matching resumes with job descriptions. Say goodbye to manual screening and hello to a smarter, more efficient hiring process. Welcome to the future of talent acquisition.")


for _ in range(1):
    st.write("")

col1, col2 = st.columns([1,1],gap='medium')

with col1:
    jd=st.text_area("Job Description",height=300,)

with col2:
    uploaded_file=st.file_uploader("Upload Resumes",type="pdf",help="Please Upload the resumes in pdf")

for _ in range(1):
    st.write("")
    
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        input_prompt=f"""
        Hey Act Like a skilled or very experience ATS(Application Tracking System)
        with a deep understanding of tech field,software engineering,data science ,data analyst
        and big data engineer. Your task is to evaluate the resume based on the given job description.
        You must consider the job market is very competitive and you should provide 
        best assistance for improving thr resumes. Assign the percentage Matching based 
        on Jd and
        the missing keywords with high accuracy
        resume:{text}
        description:{jd}

        I want the response in one single string having the structure
        {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
        """


        response=preprocess_text(generate(model,input_prompt))
        st.subheader(response)

