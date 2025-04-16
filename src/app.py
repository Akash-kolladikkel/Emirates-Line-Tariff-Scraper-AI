from langchain_experimental.agents import create_csv_agent
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import os
import streamlit as st

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def initialize_session_state():
    """Initialize session state for message history"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Emirates Line Tariff Assistant. Ask me anything about the Demmuarge data!"}
        ]

def main():
    st.set_page_config(page_title="CSV-Agent")
    initialize_session_state()
    
    # Sidebar configuration
    with st.sidebar:
        st.success("🙏 Welcome")
        st.markdown("---")
        
        with st.expander("ℹ️ How to Use"):
            st.markdown("""
            **Sample Questions:**
            - Total countries in the file
            - What are the charges for Bucket 2 (11-15 days) for 20-Dry containers at the port of Alexandria, Egypt?
            - What are the charges for 20-Dry and 40-Dry containers at the port of Beijiao, China?
            """)
            
    # Main page layout
    st.header("Emirates Line - AI Assistant 🚢📊")
    st.markdown("💬 Chat with Your Tariff Data")
    
    # Initialize LLM and agent
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    instruction = """When answering questions:
    1. Always use the FULL CSV data loaded as 'df'.
    2. The bucket columns (like 'Bucket 1 (6-10)', 'Bucket 2 (11-15)') represent charges with their corresponding currency shown in the 'Currency' column.
    3. Use the python_repl_ast tool with format:
    Action: python_repl_ast
    Action Input: <your code>
    4. Provide final answer with analysis"""

    agent = create_csv_agent(
        llm=llm,
        path="Final.csv",
        verbose=True,
        prefix=instruction,
        allow_dangerous_code=True,
        agent_executor_kwargs={"handle_parsing_errors": True}
    )

    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Eg: List the ports in Vietnam"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response
        with st.chat_message("assistant"):
            try:
                with st.spinner("Analyzing tariffs..."):
                    response = agent.invoke(user_input)
                    answer = response.get("output", "Could not retrieve answer")
            except Exception as e:
                answer = f"Error processing request: {str(e)}"
            
            st.markdown(answer)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
