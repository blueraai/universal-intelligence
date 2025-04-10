from playground.__utils__ import formatted_print
from src.community.agents.default import UniversalAgent
from src.community.models.default import UniversalModel
from src.community.tools.api_caller import UniversalTool as APITool
from src.community.tools.simple_printer import UniversalTool as SimplePrinterTool

# 🧠 Simple model
model = UniversalModel()
result, logs = model.process("Hello, how are you?")

formatted_print("Model", result, logs)

# 🔧 Simple tool
tool = SimplePrinterTool()
result = tool.print_text("This needs to be printed")

formatted_print("Tool", result)

# 🤖 Simple agent (🧠 + 🔧)
agent = UniversalAgent()
result, logs = agent.process("Please print 'Hello World' to the console", extra_tools=[tool])

formatted_print("Simple Agent", result, logs)

# 🤖 Simple agent calling API (shared 🧠 + 🔧)
tool = APITool()
agent = UniversalAgent(universal_model=model)
result, logs = agent.process("Please fetch the latest space news articles by calling the following API endpoint: GET https://api.spaceflightnewsapi.net/v4/articles", extra_tools=[tool])

formatted_print("API Agent", result, logs)
