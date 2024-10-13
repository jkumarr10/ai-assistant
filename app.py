from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langchain.tools import tool
from langchain_community.tools import TavilySearchResults

from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver


from dotenv import load_dotenv
from pydantic import BaseModel, Field
import streamlit as st



# Load environment variables
load_dotenv()

# LLM setup
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

# Load the PDF and split text
loader = PyPDFLoader("iesc111.pdf")
pages = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)
splits = text_splitter.split_documents(pages)

# Create VectorStore and retriever
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(model='text-embedding-3-small'))
retriever = vectorstore.as_retriever()

# RAG Prompt template
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise."),
    ("user", "context: {context}\n\nquestion: {question}")    
])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG Chain setup
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# Define RAG Tool for Assistant
class RagTool(BaseModel):
    user_query: str = Field(description="The user's input query to use for RAG")

@tool("rag_tool", args_schema=RagTool, return_direct=True)
def rag_tool(user_query: str) -> str:
    ''' Invokes the RAG chain To Provide an Answer to the User's Query'''
    response = rag_chain.invoke(user_query)
    return response

# Define Web Search Tool
class WebSearch(BaseModel):
    user_query: str = Field(description="The user's input query to use for Web Search")
    
@tool("web_search_tool", args_schema= WebSearch, return_direct=True)
def web_search_tool(user_query: str) -> str:
    ''' Runs a web search to provide an answer based on the user's query '''
    search = TavilySearchResults(
        max_results = 5,
        search_depth = "advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=True
    )
    results = search.invoke({"query":user_query})
    return {"messages": results}

# Tool binding
tools = [rag_tool, web_search_tool]
llm_with_tools = llm.bind_tools(tools)

# Create a System Message

sys_msg = SystemMessage(content=
    """You are an AI assistant capable of answering questions using two tools provided to you:
    
        1. **Retrieval-Augmented Generation (RAG) Pipeline Tool**:
        - You have access to a pre-configured RAG pipeline, which is capable of retrieving relevant information about a document containing information on the topic of 'Sound'.
        - If the user's input is related to the topic of 'Sound', trigger the RAG tool.

        2. **Tavily Web Search Tool**:
        - You can use the Tavily web search tool to fetch real-time information from the web for any queries not covered by the RAG pipeline, such as current events, general knowledge, or even topics unrelated to 'Sound'.

    Deciding when to invoke a tool:
    - Use the **RAG Pipeline Tool** if the user's input is related to 'Sound'.
    - Use the **Tavily Web Search Tool** if the user's query is about 'Sound' that the document in RAG pipeline does not cover or requires real-time or broader web-based information.
    
    Do not hallucinate your answer. Use the tools provided to provide the best answer possible to the user's query.

    User Question: "{user_query}"""
)

# Create Assistant Node
def assistant(state: MessagesState):
    response = llm_with_tools.invoke([sys_msg] + state["messages"])
    return {"messages": response}

# Graph
builder = StateGraph(MessagesState)

# Define Nodes
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Add Edges
builder.add_edge(START, "assistant")
builder.add_edge("assistant", "tools")
builder.add_edge("tools", END)

# Compile the graph
graph = builder.compile(checkpointer=MemorySaver())

# Streamlit Integration
def run_streamlit():
    st.title("AI Assistant with Streamlit")

    # Input for user query
    user_input = st.text_input("Enter your question:")

    # Function to invoke the Graph directly
    def ask_question(query):
        if query:
            try:
                # Convert user input into HumanMessage
                user_message = HumanMessage(content=query)

                # Call the graph.invoke function
                response = graph.invoke({"messages": [user_message]}, {"configurable": {"thread_id": "1"}})

                # Extract and return response messages
                response_messages = [message.content for message in response["messages"]]
                
                return response_messages
            
            except Exception as e:
                return f"Error: {str(e)}"
            
        return None
    
    # Button to send the question
    if st.button("Ask AI"):
            if user_input:
                # Show a loading spinner while waiting for the AI's response
                with st.spinner("Processing your question..."):
                    result = ask_question(user_input)
                    
                if result:
                    st.write("Response from AI:")
                    for message in result:
                        st.write(message)
              

# Run the Streamlit app
if __name__ == "__main__":
    run_streamlit()
