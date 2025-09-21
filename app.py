import os
import streamlit as st
import PyPDF2
import google.generativeai as genai

# Set up Google Gemini API Key
GEMINI_API_KEY = "AIzaSyDhLlvYbUKdHmVXUHURTbvoXbfU9_qLRBM"
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit UI
st.set_page_config(page_title="AI Personal Finance Analyzer", layout="wide")

# Sidebar with usage info
st.sidebar.title("❓ How to Use This App")
st.sidebar.write("- Upload your Paytm, PhonePe, GPay or Bank Transactions History in the PDF Format.")
st.sidebar.write("- The AI will analyze your transactions and Generates actionable Insights.")
st.sidebar.write("- You will receive financial insights including Total income, expenses, savings, and spending trends.")
st.sidebar.write("- Use this app to plan your finances Carefully.")

st.title('💵 AI-Powered Personal Financial Analyzer')
st.subheader('Upload your Paytm, PhonePe, GPay or Bank Transactions History in PDF Format for Financial Insights')

# Upload PDF File
uploaded_file = st.file_uploader("🗃️ Upload PDF Format File", type=["pdf"], help="Only PDF Format Files are supported")

def extract_text_from_pdf(file_path):
    """Extracts text from the uploaded PDF Format file."""
    text = ""
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def analyze_financial_data(text):
    """Sends extracted text to Google Gemini AI for financial insights."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Analyze the following Paytm, PhonePe, GPay or bank transactions history and generate financial insights:
    {text}
    Provide a detailed breakdown in the Upcoming format:
    **Financial Insights for [User Name]**
    **Key Details:**
    - **Overall Monthly Income & Expenses:**
      - Month: [Month]
      - Income: ₹[Amount]
      - Expenses: ₹[Amount]
    - **Unnecessary Expenses Analysis:**
      - Expense Category: [Category Name]
      - Amount: ₹[Amount]
      - Recommendation: [Suggestion]
    - **Savings Percentage Calculation:**
      - Savings Percentage: [Percentage] %
    - **Expense Trend Analysis:**
      - Notable Trends: [Trend Details]
    - **Cost Control Recommendations:**
      - Suggestion: [Detailed Suggestion]
    - **Category-Wise Spending Breakdown:**
      - Category: [Category Name] - ₹[Amount]
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "⚠️ Error processing financial data."

if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✔️ File uploaded successfully!")

    with st.spinner("📄 Extracting text from document..."):
        extracted_text = extract_text_from_pdf(file_path)

    if not extracted_text:
        st.error("⚠️ Failed to extract text. Ensure the document is not a scanned image PDF.")
    else:
        progress_bar = st.progress(0)
        with st.spinner("☀️ AI is analyzing your financial data..."):
            insights = analyze_financial_data(extracted_text)

        progress_bar.progress(100)

        st.header("📒 Financial Insights Report")
        st.subheader(f'💸 Financial Report for {uploaded_file.name}')

        st.write(insights)

        st.header('🎊 Analysis Completed! Plan your finances Carefully. 🥳')
        st.balloons()

    os.remove(file_path)  # Cleanup