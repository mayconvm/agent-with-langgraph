import asyncio
import dotenv
from src.tool.tavily import internet_search
from src.tool.agenda import get_agenda_tools
from deepagents import create_deep_agent
from deepagents.backends import (
    StateBackend,
    CompositeBackend,
    StoreBackend,
    FilesystemBackend,
)
from src.prompts.main import PROMPT_MAIN
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from src.skills.all_skills import SKILLS_FILES
import logging, uuid


def make_backend(runtime):
    """Routes /memories/ to filesystem, others to ephemeral state"""
    return CompositeBackend(
        default=StateBackend(runtime),  # Short-term memory
        routes={
            "/memories/": FilesystemBackend(root_dir="./memories/", virtual_mode=True)
        },  # Long-term memory
    )


# Memory
checkpointer = MemorySaver()
store = InMemoryStore()


async def main(user_input: str):
    dotenv.load_dotenv()
    logging.getLogger("langchain_google_genai._function_utils").setLevel(logging.ERROR)

    agenda_tools = await get_agenda_tools()

    agent = create_deep_agent(
        tools=[internet_search] + agenda_tools,
        model="google_genai:gemini-2.5-flash",
        # model="google_genai:gemini-2.5-flash-lite",
        # model="google_genai:gemini-3-flash-preview",
        skills=["./src/skills/"],
        system_prompt=PROMPT_MAIN,
        backend=make_backend,
        checkpointer=checkpointer,
        store=store,
    )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            "files": SKILLS_FILES,
        },
        config={"configurable": {"thread_id": str(uuid.uuid4())}},
    )

    # Print the agent's response
    print(result["messages"][-1].content)


if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        asyncio.run(main(user_input))
