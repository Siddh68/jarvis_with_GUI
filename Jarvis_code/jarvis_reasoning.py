# import os
# import asyncio
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.agents import create_agent
# from livekit.agents import function_tool
# from langchain_classic import hub

# # ---- Import your Jarvis Tools ----
# from Jarvis_google_search import google_search, get_current_datetime
# from jarvis_get_whether import get_weather
# from Jarvis_window_CTRL import open_app, close_app, folder_file
# from Jarvis_file_opner import Play_file

# # ---- Load environment variables ----
# load_dotenv()

# # ---- Initialize Gemini Model ----
# model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


# @function_tool(
#     name="thinking_capability",
#     description=(
#         "Main reasoning and action function for Jarvis. "
#         "It can perform Google searches, open or close apps, fetch weather, and access files. "
#         "If the user asks to write something, it can open Notepad automatically."
#     )
# )
# async def thinking_capability(query: str) -> dict:
#     """
#     Main LangChain-powered reasoning tool for Jarvis.
#     Takes a natural language query and executes the correct workflow.
#     """
#     try:
#         prompt = hub.pull("hwchase17/react")

#         tools = [
#             google_search,
#             get_current_datetime,
#             get_weather,
#             open_app,
#             close_app,
#             folder_file,
#             Play_file
#         ]

#         agent = create_agent(
#             model=model,
#             tools=tools,
#             system_prompt=prompt
#         )

#         # Use invoke instead of ainvoke to avoid event loop issues
#         result = agent.invoke({"messages": [{"role": "user", "content": query}]})
        
#         # Extract the final AI message content
#         final_message = result["messages"][-1]
#         return {"result": final_message.content}

#     except Exception as e:
#         return {"error": f"Agent execution failed: {str(e)}"}


# # ---------------- Manual Testing Section ---------------- #
# # This section runs only if you execute this file directly.
# # Remove or comment it out when using from agents.py
# if __name__ == "__main__":
#     async def main():

#         while True:
#             user_input = input("💬 Command: ").strip()
#             if user_input.lower() in ["exit", "quit"]:
#                 print("👋 Goodbye, shutting down Jarvis...")
#                 break

#             try:
#                 response = await thinking_capability(user_input)
#                 print("\n🧠 Response:", response, "\n")
#             except Exception as e:
#                 print("\n⚠️ Error:", str(e), "\n")

#     asyncio.run(main())