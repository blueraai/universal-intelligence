import * as yaml from 'js-yaml'

import { AbstractUniversalModel } from "../../../core/UniversalModel"
import UniversalModel from "../../models/qwen2_5_3b_instruct/model"

import { Logger, LogLevel } from "./../../../community/__utils__/logger"
import { Contract, Compatibility, Requirement, Message } from "./../../../core/types"
import { AbstractUniversalAgent } from "./../../../core/UniversalAgent"
import { AbstractUniversalTool } from "./../../../core/UniversalTool"



const _contract: Contract = {
  name: "Simple Agent",
  description: "A simple generic agent that can use tools and other agents to accomplish tasks",
  methods: [
      {
          name: "process",
          description: "Process text input through the agent, using available tools and team members as needed",
          arguments: [
              {
                  name: "input", 
                  type: "string | Message[]",
                  schema: {
                      nested: [
                          {
                              name: "role",
                              type: "string",
                              schema: {pattern: "^(system|user|assistant)$"},
                              description: "The role of the message sender",
                              required: true,
                          },
                          {
                              name: "content",
                              type: "string",
                              schema: {},
                              description: "The content of the message",
                              required: true,
                          },
                      ]
                  },
                  description: "Input string or list of messages in chat format",
                  required: true,
              },
              {
                  name: "context",
                  type: "any[]",
                  schema: {},
                  description: "Optional context items to prepend as system messages",
                  required: false,
              },
              {
                  name: "configuration",
                  type: "Record<string, any>",
                  schema: {},
                  description: "Optional runtime configuration",
                  required: false,
              },
              {
                  name: "remember",
                  type: "boolean",
                  schema: {},
                  description: "Whether to remember this interaction in history",
                  required: false,
              },
              {
                  name: "stream",
                  type: "boolean",
                  schema: {},
                  description: "Whether to stream output asynchronously",
                  required: false,
              },
              {
                  name: "extraTools",
                  type: "AbstractUniversalTool[]",
                  schema: {},
                  description: "Additional tools for this specific inference",
                  required: false,
              },
              {
                  name: "extraTeam",
                  type: "AbstractUniversalAgent[]",
                  schema: {},
                  description: "Additional agents for this specific inference",
                  required: false,
              },
              {
                  name: "keep_alive",
                  type: "boolean",
                  schema: {},
                  description: "Keep underlaying model loaded for faster consecutive interactions",
                  required: false,
              },
          ],
          outputs: [
              {
                  type: "[any, Record<string, any>]",
                  schema: {
                      nested: [
                          {
                              name: "response",
                              type: "string",
                              schema: {},
                              description: "Generated text response",
                              required: true,
                          },
                          {
                              name: "logs",
                              type: "Record<string, any>",
                              schema: {},
                              description: "Processing logs and metadata",
                              required: true,
                          },
                      ]
                  },
                  description: "Generated response and processing logs",
                  required: true,
              }
          ],
      },
      {
          name: "load",
          description: "Load the agent's model into memory",
          arguments: [],
          outputs: [
              {
                  type: "void",
                  schema: {},
                  description: "No return value",
                  required: true,
              }
          ],
      },
      {
          name: "loaded",
          description: "Check if the agent's model is loaded",
          arguments: [],
          outputs: [
              {
                  type: "boolean",
                  schema: {},
                  description: "True if the model is loaded, False otherwise",
                  required: true,
              }
          ],
      },
      {
          name: "unload",
          description: "Unload the agent's model from memory",
          arguments: [],
          outputs: [
              {
                  type: "void",
                  schema: {},
                  description: "No return value",
                  required: true,
              }
          ],
      },
      {
          name: "reset",
          description: "Reset the agent's chat history",
          arguments: [],
          outputs: [
              {
                  type: "void",
                  schema: {},
                  description: "No return value",
                  required: true,
              }
          ],
      },
      {
          name: "connect",
          description: "Connect additional tools and agents",
          arguments: [
              {
                  name: "universalTools",
                  type: "AbstractUniversalTool[]",
                  schema: {},
                  description: "Additional tools to connect",
                  required: false,
              },
              {
                  name: "universalAgents",
                  type: "AbstractUniversalAgent[]",
                  schema: {},
                  description: "Additional agents to connect",
                  required: false,
              },
          ],
          outputs: [
              {
                  type: "void",
                  schema: {},
                  description: "No return value",
                  required: true,
              }
          ],
      },
      {
          name: "disconnect",
          description: "Disconnect tools and agents",
          arguments: [
              {
                  name: "universalTools",
                  type: "AbstractUniversalTool[]",
                  schema: {},
                  description: "Tools to disconnect",
                  required: false,
              },
              {
                  name: "universalAgents",
                  type: "AbstractUniversalAgent[]",
                  schema: {},
                  description: "Agents to disconnect",
                  required: false,
              },
          ],
          outputs: [
              {
                  type: "void",
                  schema: {},
                  description: "No return value",
                  required: true,
              }
          ],
      },
  ],
}

const _requirements: any[] = [] // No special requirements for this example agent

const _compatibility: Compatibility[] = [
  {
      engine: "any", // Depends on the model used
      quantization: "any", // Depends on the model used
      devices: ["webgpu"],
      memory: 0.0, // Depends on the model used
      dependencies: ["pyyaml"],
      precision: 4, // Depends on the model used
  }
]

export default class UniversalAgent extends AbstractUniversalAgent {
  /** A simple generic agent that can use tools and other agents to accomplish tasks */

  private static _defaultTools: AbstractUniversalTool[] = [] // may include any tools by default
  private static _defaultTeam: AbstractUniversalAgent[] = [] // may include any agents by default
  
  public static contract(): Contract {
    return { ..._contract }
  }

  public static compatibility(): Compatibility[] {
    return [ ..._compatibility ]
  }

  public static requirements(): Requirement[] {
    return [ ..._requirements ]
  }

  contract(): Contract {
    return { ..._contract }
  }

  compatibility(): Compatibility[] {
    return [ ..._compatibility ]
  }

  requirements(): Requirement[] {
    return [ ..._requirements ]
  }

  private model: AbstractUniversalModel
  private tools: AbstractUniversalTool[]
  private team: AbstractUniversalAgent[]
  private _logger: Logger
  constructor(
    payload?: {
      model?: AbstractUniversalModel,
      expandTools?: AbstractUniversalTool[],
      expandTeam?: AbstractUniversalAgent[],
      configuration?: Record<string, any>,
      verbose?: boolean | string
    } | undefined
  ) {
    const { model, expandTools, expandTeam, configuration, verbose } = payload || {}
    super(payload)
    this.model = model ? model : new UniversalModel({ verbose })
    this.tools = UniversalAgent._defaultTools.concat(expandTools ? expandTools : [])
    this.team = UniversalAgent._defaultTeam.concat(expandTeam ? expandTeam : [])
    if (typeof verbose === 'string') {
      this._logger = new Logger(LogLevel[verbose as keyof typeof LogLevel])
    } else if (typeof verbose === 'boolean') {
      this._logger = new Logger(verbose ? LogLevel.DEBUG : LogLevel.NONE)
    } else {
      this._logger = new Logger()
    }
  }
  
  private async _planDependencyCalls(
    query: string,
    extraTools: AbstractUniversalTool[] | null = null,
    extraTeam: AbstractUniversalAgent[] | null = null
  ): Promise<any[]> {
    // Combine permanent and temporary dependencies
    const tools = this.tools.concat(extraTools || [])
    const team = this.team.concat(extraTeam || [])

    // Have the model analyze available tools and team members
    const toolContracts = tools.map(tool => tool.contract())
    const teamContracts = team.map(agent => agent.contract())

    // Create YAML description of available capabilities
    const capabilities = {
      available_tools: toolContracts.map(contract => ({
        name: contract.name,
        description: contract.description,
        methods: contract.methods
      })),
      available_team: teamContracts.map(contract => ({
        name: contract.name,
        description: contract.description,
        methods: contract.methods
      }))
    }

    // Ask model to plan dependency calls
    const planningPrompt = `Given the following user query and available capabilities, analyze if and how the available tools and team members can help satisfy the query.

FIRST, determine if the query actually requires using any avalaible tools:
1. If the query is asking to perform an action (like printing, searching, calling an API, etc.) and tools exists for that, then use appropriate tools
2. If the query requires recent information, past January 1st 2023, and tools exists for that, then use appropriate tools
3. If the query requires specialized information and tools exists for that, then use appropriate tools
4. If the query is just asking for conversation (like "how are you?"), then return an empty list - DO NOT use tools
5. If the query is just asking for generic information prior to January 1st 2023, then return an empty list - DO NOT use tools

When tools ARE needed:
- Use the EXACT names and arguments as specified in the tool contracts
- Tool name must match contract's "name" field
- Method name must match contract's "methods" list and only include the method name, not the class name
- Argument names must match the method's "arguments" list
- The method's "arguments" list always is an array presenting the key/value pairs for the method's first argument, which always is an object

DO NOT invent or use tools that are not listed in the capabilities below.
DO NOT answer the query.
DO NOT explain your reasoning.
ONLY return the list of tools to use in order along with their arguments, in a YAML format.

For example, to print text using the Example Tool:
- dependency_type: tool
  dependency_name: Example Tool  # Exact name from contract
  method_name: example_method    # Exact method name
  arguments:
    text: "example text"        # Exact argument name

User Query: ${query}

Available Capabilities:
${yaml.dump(capabilities, { sortKeys: false })}
`
    this._logger.log("[Agent] Planning tasks to satisfy query..", { ask: { query, capabilities }})
    const [planResponse] = await this.model.process(planningPrompt)
    try {
      // Parse the YAML response into a list of planned calls
      const plannedCalls = yaml.load(planResponse)
      if (!Array.isArray(plannedCalls)) {
        return []
      }

      // Validate and limit number of calls
      this._logger.log("[Agent] Validating and limiting number of planned tasks..", { plannedCalls })
      const validCalls = plannedCalls
        .slice(0, 10) // Limit to 10 calls
        .filter(call => {
          const requiredKeys = [
            "dependency_type",
            "dependency_name", 
            "method_name",
            "arguments"
          ]
          return requiredKeys.every(k => k in call)
        })

      this._logger.log("[Agent] Staging valid tasks for execution..", { validCalls })
      validCalls.map(call => {
        try {
          let methodNameSplits = call["method_name"].split(".")
          call["method_name"] = methodNameSplits[methodNameSplits.length - 1]
        } catch (error) {
          this._logger.warn("[Plan] Task Planning Error: ", error)
        }
        return call
      })

      return validCalls

    } catch (err) {
      return [] // Return empty plan if YAML parsing fails
    }
  }

  private async _executeDependencyCalls(
    plannedCalls: Array<Record<string, any>>,
    extraTools: AbstractUniversalTool[] | null = null,
    extraTeam: AbstractUniversalAgent[] | null = null
  ): Promise<Array<Record<string, any>>> {
    // Combine permanent and temporary dependencies
    const tools = [...this.tools, ...(extraTools || [])]
    const team = [...this.team, ...(extraTeam || [])]

    const results: Array<Record<string, any>> = []

    for (const call of plannedCalls) {
      const dependencyType = call["dependency_type"]
      const dependencyName = call["dependency_name"]
      const methodName = call["method_name"]
      const args = call["arguments"]
      this._logger.log("[Agent] Executing task..", { call })

      // Find the matching dependency
      const dependencies = dependencyType === "tool" ? tools : team
      const dependency = dependencies.find(d => d.contract()["name"] === dependencyName)
      if (dependency) {
        try {
          const method = (dependency as any)[methodName]
          const contract = dependency.contract()

          // Check if method is marked as asynchronous in contract
          const methodContract = contract.methods?.find(m => m.name === methodName)
          const isAsync = methodContract?.asynchronous || false

          // Call method with provided arguments and await if async
          let result
          if (isAsync) {
            [result] = await method.call(dependency, args).catch(error => {
              this._logger.error(`Error calling ${methodName} on ${dependencyName}:`, error)
              return ['Dependency call failed.']
            })
          } else {
            [result] = (() => {
              try {
                return method.call(dependency, args)
              } catch (error) {
                this._logger.error(`Error calling ${methodName} on ${dependencyName}:`, error)
                return ['Dependency call failed.']
              }
            })()
          }

          results.push({
            dependency_type: dependencyType,
            dependency_name: dependencyName,
            method_name: methodName,
            result: result
          })

        } catch (error) {
          if (error instanceof TypeError) {
            continue // Skip failed calls
          }
          throw error
        }
      }
    }

    return results
  }

  async process(
    input: string | Message[], 
    payload?: {
      context?: any[],
      configuration?: Record<string, any>,
      remember?: boolean,
      stream?: boolean,
      extraTools?: AbstractUniversalTool[],
      extraTeam?: AbstractUniversalAgent[],
      keepAlive?: boolean
  } | undefined): Promise<[any, Record<string, any>]> {
    const { context, configuration, remember, stream, extraTools, extraTeam, keepAlive } = payload || {}
    // Convert input to string if it's a message list
    const query = typeof input === 'string' ? input : input[input.length - 1].content

    // Plan dependency calls with extra tools and agents
    const plannedCalls = await this._planDependencyCalls(query, extraTools, extraTeam)

    // Execute planned calls with extra tools and agents
    const callResults = await this._executeDependencyCalls(plannedCalls, extraTools, extraTeam)

    // Format results as YAML for the model
    const resultsYaml = yaml.dump({
      original_query: query,
      dependency_calls: callResults
    }, { sortKeys: false })

    // Have model generate final response using call results
    const finalPrompt = `Given the original query and results from dependency calls, generate a final response.
If dependency calls were made, explain what actions were taken and their results.
If no dependency calls were made, provide a direct response to the query.

For example, if a print tool was used, confirm what was printed to the console.

Execution Results:
${resultsYaml}
`

    this._logger.log("[Agent] Processing tasks results..", { callResults })
    const [response, logs] = await this.model.process(
      finalPrompt,
      {
        context,
        configuration,
        remember,
        keepAlive,
      }
    )

    return [response, {
      model_logs: logs,
      dependency_calls: callResults,
      stream: stream
    }]
  }

  async load(): Promise<void> {
    await this.model.load()
  }

  async loaded(): Promise<boolean> {
    return this.model.loaded()
  }

  async unload(): Promise<void> {
    await this.model.unload()
  }

  async reset(): Promise<void> {
    await this.model.reset()
  }

  async connect(
    payload: {
      universalTools?: AbstractUniversalTool[],
      universalAgents?: AbstractUniversalAgent[]
    }
  ): Promise<void> {
    this._logger.log("[Agent] Connecting additional tools and agents..", payload)
    const { universalTools, universalAgents } = payload || {}
    await this.model.ready()
    if (universalTools) {
      this.tools.push(...universalTools)
    }
    if (universalAgents) {
      this.team.push(...universalAgents)
    }
  }

  async disconnect(
    payload: {
      universalTools?: AbstractUniversalTool[],
      universalAgents?: AbstractUniversalAgent[]
    }
  ): Promise<void> {
    this._logger.log("[Agent] Disconnecting additional tools and agents..", payload)
    const { universalTools, universalAgents } = payload || {}
    await this.model.ready()
    if (universalTools) {
      this.tools = this.tools.filter(t => !universalTools.includes(t))
    }
    if (universalAgents) {
      this.team = this.team.filter(a => !universalAgents.includes(a))
    }
  }
}