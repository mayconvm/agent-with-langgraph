import asyncio
import dotenv
from src.tool.tavily import internet_search
from src.tool.agenda import get_agenda_tools
from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from src.prompts.main import PROMPT_MAIN
from langgraph.checkpoint.memory import MemorySaver
from src.skills.all_skills import SKILLS_FILES
import logging


async def main():
    dotenv.load_dotenv()
    logging.getLogger("langchain_google_genai._function_utils").setLevel(logging.ERROR)
    # fs_backend = FilesystemBackend(root_dir=".", virtual_mode=True)

    checkpointer = MemorySaver()

    agenda_tools = await get_agenda_tools()

    agent = create_deep_agent(
        tools=[internet_search] + agenda_tools,
        system_prompt=PROMPT_MAIN,
        model="google_genai:gemini-2.5-flash-lite",
        # model="google_genai:gemini-3-flash-preview",
        # backend=fs_backend,
        backend=(lambda rt: StateBackend(rt)),
        skills=["./src/skills/"],
    )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Quais são as todas as notas que tenho na agenda?",
                }
            ],
            "files": SKILLS_FILES,
        },
        config={"configurable": {"thread_id": "12345"}},
    )

    # Print the agent's response
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
