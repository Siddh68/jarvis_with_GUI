from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, ChatContext, ChatMessage
from livekit.plugins import google, noise_cancellation

# Import your custom modules
from Jarvis_prompts import instructions_prompt, Reply_prompts
from memory_loop import MemoryExtractor
from mcp_client.server import MCPServerSse
from mcp_client.agent_tools import MCPToolsIntegration
import os
load_dotenv()


class Assistant(Agent):
    def __init__(self,) -> None:
        super().__init__(
                        instructions=instructions_prompt,
                        llm=google.beta.realtime.RealtimeModel(voice="Charon"),
                                )

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        preemptive_generation=True
    )
    
    #getting the current memory chat
    current_ctx = session.history.items
    
    mcp_server = MCPServerSse(
        params={"url": os.environ.get("N8N_MCP_SERVER_URL")},
        cache_tools_list=True,
        name="SSE MCP Server"
    )

    agent = await MCPToolsIntegration.create_agent_with_tools(
        agent_class=Assistant,
        mcp_servers=[mcp_server]
    )

    await session.start(
        room=ctx.room,
        agent=agent , #sending currenet chat to llm in realtime
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )
    await session.generate_reply(
        instructions=Reply_prompts
    )
    conv_ctx = MemoryExtractor()
    await conv_ctx.run(current_ctx)
    


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

    