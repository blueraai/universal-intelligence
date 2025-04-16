import { Contract, Requirement } from './types'

export abstract class AbstractUniversalTool {
  /**
   * Get the contract for the tool.
   */
  static contract(): Contract {
    throw new Error('Method not implemented')
  };

  /**
   * Get the requirements for the tool.
   */
  static requirements(): Requirement[] {
    throw new Error('Method not implemented')
  };

  /**
   * Get the contract for the instance of the tool.
   */
  abstract contract(): Contract;

  /**
   * Get the requirements for the instance of the tool.
   */
  abstract requirements(): Requirement[];

  /**
   * Initialize a Universal Tool.
   * @param configuration - Tool configuration including required credentials
   */
  constructor(configuration?: Record<string, any> | undefined) {
    if (this.constructor === AbstractUniversalTool) {
      throw new Error('Abstract class cannot be instantiated')
    }
  }

  // Note: Additional methods are defined by the specific tool implementation
  // and documented in the tool's contract
} 