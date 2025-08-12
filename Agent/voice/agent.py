from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

toolbox = ToolboxSyncClient("http://127.0.0.1:5000")
tools = toolbox.load_toolset('query-players')

root_agent = Agent(
    model='gemini-2.0-flash-live-001', # gemini-2.0-flash-001 for text only
    name='Voice Agent',
    description='Find the players and set as either pitcher or hitter and keep a map of the name to the player id',
    instruction='given a request look up player information and run the query.  If the result is more than 1 item, display the results as a pretty table',
    tools=tools,
)
