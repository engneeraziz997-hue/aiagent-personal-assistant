import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from tools import search_knowledge_base

checkpointer = MemorySaver()

system_prompt = (
    "You are a helpful AI assistant with access to a knowledge base. "
    "When users ask questions, search the knowledge base using the available tools to find relevant information. "
    "Be concise and accurate."
)

def run_agent(message: str, session_id: str = "default") -> dict:
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY")

        model = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            api_key=api_key
        )

        agent_app = create_react_agent(
            model=model,
            tools=[search_knowledge_base],
            prompt=system_prompt,
            checkpointer=checkpointer
        )

        print(f'🤖 Running agent for: "{message}"')

        config = {"configurable": {"thread_id": session_id}}
        response = agent_app.invoke(
            {"messages": [("user", message)]},
            config=config
        )

        last_message = response["messages"][-1]
        output = str(last_message.content) if last_message else ""

        print(f"✅ Agent response: {output[:100]}...")

        return {"output": output}
    except Exception as error:
        print("❌ Error in run_agent:", error)
        raise error
