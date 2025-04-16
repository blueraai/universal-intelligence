import { UniversalAgent as SimpleAgent } from "./simple_agent"

const agents = {
  SimpleAgent,
  Agent: SimpleAgent, // default agent
}

export default agents