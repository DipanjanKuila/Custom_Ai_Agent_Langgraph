#from graph import create_graph, compile_workflow
from langgraph_module.graph import create_graph, compile_workflow
from dotenv import load_dotenv
import os
from PIL import Image as PILImage
import streamlit as st

load_dotenv()
server = 'give your llm model like-azureopenai,gemini.....'
model = "Give your model name"
model_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")



iterations = 40


st.title("AI Research Workflow with Multi-Agent Collaboration")
st.markdown("### Powered by LLM Models, Streamlit, and Advanced Agents for Seamless Research Automation")



st.sidebar.header("Settings")
verbose = st.sidebar.checkbox("Verbose Output", value=False)
recursion_limit = st.sidebar.slider("Recursion Limit", min_value=1, max_value=100, value=iterations)

# Workflow Initialization
st.write("### Workflow Initialization")
with st.spinner("Creating graph and compiling workflow..."):
    try:
        # Create graph and workflow once
        graph = create_graph(server=server, model=model, model_endpoint=model_endpoint)
        workflow = compile_workflow(graph)
        st.success("Graph and workflow created successfully!")
    except Exception as e:
        st.error(f"Error during graph or workflow creation: {e}")
        st.stop()

# LangGraph Visualization
st.sidebar.header("Generate LangGraph Visualization")
if st.sidebar.button("Show LangGraph Image"):
    with st.spinner("Generating LangGraph visualization..."):
        try:
            
            st.image(workflow.get_graph().draw_mermaid_png()) 
            st.markdown("""
                ### LangGraph Visualization
                **Visual representation of the system's workflow, crafted with LangGraph for enhanced clarity.**
                
                This diagram provides an intuitive understanding of the connections and flow within the workflow.
            """)
        except Exception as e:
            st.error(f"Error during LangGraph visualization: {e}")





st.write("### Enter Your Research Question")
query = st.text_input("Research Question:", placeholder="Type your question here...")

if st.button("Run Workflow"):
    if not query.strip():
        st.warning("Please enter a valid research question.")
    else:
        st.write("### Workflow Output")
        dict_inputs = {"research_question": query}
        limit = {"recursion_limit": recursion_limit}
        
        try:
            
            output_container = st.empty()
            for event in workflow.stream(dict_inputs, limit):
                if verbose:
                    output_container.write(f"State Dictionary: {event}")
                else:
                    output_container.write(event)
        except Exception as e:
            st.error(f"Error during workflow execution: {e}")
