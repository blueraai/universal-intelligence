import universalIntelligence, { Model, Tool, Agent } from "./../../distweb/index.js";
const { APICaller } = universalIntelligence.community.tools;

// ⚪ Universal Intelligence - Available Imports
console.warn("⚪ Universal Intelligence \n\n", universalIntelligence);


// ------------------------------------------------------------------------------------------------
// 🧠 Simple model
const model = new Model();
const [modelResult, modelLogs] = await model.process("Hello, how are you?");

console.warn("🧠 Model \n\n", modelResult, modelLogs);

// ------------------------------------------------------------------------------------------------
// 🔧 Simple tool
const tool = new Tool();
const [toolResult, toolLogs] = await tool.printText({ text: "This needs to be printed" });

console.warn("🔧 Tool \n\n", toolResult, toolLogs);

// ------------------------------------------------------------------------------------------------
// 🤖 Simple agent (🧠 + 🔧)
const agent = new Agent();
const [agentResult, agentLogs] = await agent.process("Please print 'Hello World' to the console", { extraTools: [tool] });

console.warn("🤖 Simple Agent \n\n", agentResult, agentLogs);

// ------------------------------------------------------------------------------------------------
// 🤖 Simple agent calling API (shared 🧠 + 🔧)
const apiTool = new APICaller();
const otherAgent = new Agent({ universalModel: model, expandTools: [apiTool] });
const [otherAgentResult, otherAgentLogs] = await otherAgent.process("Please fetch the latest space news articles by calling the following API endpoint: GET https://api.spaceflightnewsapi.net/v4/articles");

console.warn("🤖 API Agent \n\n", otherAgentResult, otherAgentLogs);

// ------------------------------------------------------------------------------------------------


