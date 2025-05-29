import universalIntelligence, { Model, Tool, Agent } from "./../../distweb/index.js";
const { APICaller } = universalIntelligence.community.tools;
const { Qwen2_5_1d5b_Instruct } = universalIntelligence.community.models.local;

// ⚪ Universal Intelligence - Available Imports
console.warn("⚪ Universal Intelligence \n\n", universalIntelligence);


// ------------------------------------------------------------------------------------------------
// 🧠 Simple model - Using smaller 1.5B model for better WebGPU compatibility
// Note: WebGPU spec baseline maxBufferSize is 2GB (see https://github.com/gpuweb/gpuweb/issues/1371)
// The 1.5B model with 4-bit quantization uses only 0.8GB, fitting within this limit.
// Larger models would require requesting higher limits via requestDevice(), which web-llm doesn't currently support.
const model = new Qwen2_5_1d5b_Instruct();
const [modelResult, modelLogs] = await model.process("Hello, how are you?", {
  keepAlive: true
});

console.warn("🧠 Model \n\n", modelResult, modelLogs);

// ------------------------------------------------------------------------------------------------
// 🔧 Simple tool
const tool = new Tool();
const [toolResult, toolLogs] = await tool.printText({ text: "This needs to be printed" });

console.warn("🔧 Tool \n\n", toolResult, toolLogs);

// ------------------------------------------------------------------------------------------------
// 🤖 Simple agent (🧠 + 🔧)
// Use the same smaller model for the agent
const agent = new Agent({ model: model });
const [agentResult, agentLogs] = await agent.process("Please print 'Hello World' to the console", { 
  extraTools: [tool],
  keepAlive: true
});

console.warn("🤖 Simple Agent \n\n", agentResult, agentLogs);

// ------------------------------------------------------------------------------------------------
// 🤖 Simple agent calling API (shared 🧠 + 🔧)
// Also use the smaller model for the API agent
const apiTool = new APICaller();
const otherAgent = new Agent({ model: model, expandTools: [apiTool] });
const [otherAgentResult, otherAgentLogs] = await otherAgent.process("Please fetch the latest space news articles by calling the following API endpoint: GET https://api.spaceflightnewsapi.net/v4/articles", {
  keepAlive: true
});

console.warn("🤖 API Agent \n\n", otherAgentResult, otherAgentLogs);

// ------------------------------------------------------------------------------------------------


