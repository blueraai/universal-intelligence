import { Contract, Requirement, Compatibility, Message } from './types'
import { AbstractUniversalModel } from './UniversalModel'
import { AbstractUniversalTool } from './UniversalTool'

export abstract class AbstractUniversalAgent {
  /**
   * Get the contract for the agent.
   */
  static contract(): Contract {
    throw new Error('Method not implemented')
  };

  /**
   * Get the requirements for the agent.
   */
  static requirements(): Requirement[] {
    throw new Error('Method not implemented')
  };

  /**
   * Get the compatibility for the agent.
   */
  static compatibility(): Compatibility[] {
    throw new Error('Method not implemented')
  };

  /**
   * Get the contract for the instance of the agent.
   */
  abstract contract(): Contract;

  /**
   * Get the requirements for the instance of the agent.
   */
  abstract requirements(): Requirement[];

  /**
   * Get the compatibility for the instance of the agent.
   */
  abstract compatibility(): Compatibility[];

  /**
   * Initialize a Universal Agent.
   * @param payload.credentials - Optional credentials for the agent
   * @param payload.model - The model powering this agent
   * @param payload.expandTools - List of tools to connect to the agent
   * @param payload.expandTeam - List of other agents to connect to this agent
   */
  constructor(payload: {
    credentials?: string | Record<string, any>,
    model?: AbstractUniversalModel,
    expandTools?: AbstractUniversalTool[],
    expandTeam?: AbstractUniversalAgent[],
    configuration?: Record<string, any>,
    verbose?: boolean | string
  } | undefined) {
    if (this.constructor === AbstractUniversalAgent) {
      throw new Error('Abstract class cannot be instantiated')
    }
  }

  /**
   * Process input through the agent.
   * @param input - Input or list of input dictionaries
   * @param payload.context - Optional list of context items (multimodal supported)
   * @param payload.configuration - Optional runtime configuration
   * @param payload.remember - Whether to remember this interaction in history
   * @param payload.stream - Whether to stream output asynchronously
   * @param payload.extraTools - Additional tools for this specific inference
   * @param payload.extraTeam - Additional agents for this specific inference
   * @param payload.keepAlive - Whether to keep the underlaying model loaded for faster consecutive interactions
   * @returns Tuple containing the agent output and processing logs
   */
  abstract process(input: any | Message[], payload: {
    context?: any[],
    configuration?: Record<string, any>,
    remember?: boolean,
    stream?: boolean,
    extraTools?: AbstractUniversalTool[],
    extraTeam?: AbstractUniversalAgent[],
    keepAlive?: boolean
  } | undefined): Promise<[any | null, Record<string, any>]>;

  /**
   * Load agent's model into memory
   */
  abstract load(): Promise<void>;

  /**
   * Unload agent's model from memory
   */
  abstract unload(): Promise<void>;

  /**
   * Reset agent's chat history
   */
  abstract reset(): Promise<void>;

  /**
   * Check if agent's model is loaded
   */
  abstract loaded(): Promise<boolean>;

  /**
   * Connect additional tools and agents.
   * @param payload.universalTools - List of tools to connect
   * @param payload.universalAgents - List of agents to connect
   */
  abstract connect(payload: {
    tools?: AbstractUniversalTool[],
    agents?: AbstractUniversalAgent[]
  }): Promise<void>;

  /**
   * Disconnect tools and agents.
   * @param payload.universalTools - List of tools to disconnect
   * @param payload.universalAgents - List of agents to disconnect
   */
  abstract disconnect(payload: {
    tools?: AbstractUniversalTool[],
    agents?: AbstractUniversalAgent[]
  }): Promise<void>;
} 