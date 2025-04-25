import { Contract, Compatibility, Message, QuantizationSettings } from './types'

export abstract class AbstractUniversalModel {
  /**
   * Get the contract for the model. Describes the model's description, interface, and capabilities.
   */
  static contract(): Contract {
    throw new Error('Method not implemented')
  }

  /**
   * Get the compatibility for the model.
   */
  static compatibility(): Compatibility[] {
    throw new Error('Method not implemented')
  };

  /**
   * Get the contract for the instance of the model.
   */
  abstract contract(): Contract;

  /**
   * Get the compatibility for the instance of the model.
   */
  abstract compatibility(): Compatibility[];

  /**
   * Initialize a Universal Model.
   * @param payload.engine - Optional engine specification (e.g., 'transformers', 'llama.cpp', -or- ordered by priority ['transformers', 'llama.cpp'])
   * @param payload.quantization - Optional quantization specification
   * @param payload.maxMemoryAllocation - Optional maximum memory allocation in percentage
   * @param payload.configuration - Optional configuration dictionary for model and processor settings
   */
  constructor(payload: {
    engine?: string | string[],
    quantization?: string | string[] | QuantizationSettings,
    maxMemoryAllocation?: number,
    configuration?: Record<string, any>,
    verbose?: boolean | string
  } | undefined) {
    if (this.constructor === AbstractUniversalModel) {
      throw new Error('Abstract class cannot be instantiated')
    }
  }

  /**
   * Wait for the model to be ready.
   */
  abstract ready(): Promise<void>;

  /**
   * Process input through the model.
   * @param input - Input to process
   * @param payload.context - Optional context for the model
   * @param payload.configuration - Optional configuration for processing
   * @param payload.remember - Whether to remember the interaction in history
   * @param payload.keepAlive - Whether to keep the model loaded for faster consecutive interactions
   * @param payload.stream - Whether to stream the output
   * @returns Tuple of (output, metadata)
   */
  abstract process(input: any | Message[], payload?: {
    context?: any[],
    configuration?: Record<string, any>,
    remember?: boolean,
    keepAlive?: boolean,
    stream?: boolean
  } | undefined): Promise<[any | null, Record<string, any>]>;

  /**
   * Load model into memory
   */
  abstract load(): Promise<void>;

  /**
   * Unload model from memory
   */
  abstract unload(): Promise<void>;

  /**
   * Reset model chat history
   */
  abstract reset(): Promise<void>;

  /**
   * Check if model is loaded
   */
  abstract loaded(): Promise<boolean>;

  /**
   * Get model configuration
   */
  abstract configuration(): Promise<Record<string, any>>;
} 