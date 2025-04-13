import { Contract, Compatibility, Output } from '../../../../../core/types'

import { SourcesConfig, Sources, EngineConfig, QuantizationConfig } from './types'

export function extractPrecisionFromDescriptor(precisionDescriptor: string): number {
  if (!precisionDescriptor.endsWith('bit')) {
    throw new Error("Precision descriptor must end with 'bit'")
  }
  return parseInt(precisionDescriptor.replace('bit', ''))
}

export function generateSourcesFromConfig(data: SourcesConfig): Sources {
  const validDevices = new Set(['webgpu'])

  if (!data.model_info) {
    throw new Error('sources.yaml must contain a model_info section')
  }

  if (!data.quantizations) {
    throw new Error('sources.yaml must contain a quantizations section')
  }

  // Initialize sources structure
  const sources: Sources = {
    webgpu: {},
  }

  // Get default quantization for each device type
  const defaultQuantizations = data.model_info.default_quantization || {}

  // Validate default quantizations
  for (const [device, quant] of Object.entries(defaultQuantizations)) {
    if (!validDevices.has(device)) {
      throw new Error(`Invalid device type in default_quantization: ${device}`)
    }
    if (!data.quantizations[quant]) {
      throw new Error(`Default quantization ${quant} for ${device} not found in quantizations`)
    }
  }

  // Process each quantization
  for (const [quantName, quantInfo] of Object.entries(data.quantizations)) {
    // Validate required fields
    const requiredFields = ['engine', 'model_id', 'model_size', 'supported_devices']
    const missingFields = requiredFields.filter(field => !(field in quantInfo))
    if (missingFields.length > 0) {
      throw new Error(`Quantization ${quantName} is missing required fields: ${missingFields.join(', ')}`)
    }

    // Get and validate supported devices
    const supportedDevices = quantInfo.supported_devices || []
    if (supportedDevices.length === 0) {
      throw new Error(`Quantization ${quantName} must support at least one device type`)
    }

    const invalidDevices = supportedDevices.filter(device => !validDevices.has(device))
    if (invalidDevices.length > 0) {
      throw new Error(`Quantization ${quantName} contains invalid device types: ${invalidDevices.join(', ')}`)
    }

    // Create engine config
    const engineConfig: EngineConfig = {
      name: quantInfo.engine,
      model_id: quantInfo.model_id,
      is_default: true,
    }

    if (quantInfo.model_file) {
      engineConfig.model_file = quantInfo.model_file
    }

    // Create quantization config
    const quantConfig: QuantizationConfig = {
      available_engines: [engineConfig],
      is_default: false,
      memory: quantInfo.model_size,
      precision: parseInt(quantName.match(/\d+/)?.toString() || '32'),
    }

    // Add to each supported device
    for (const device of supportedDevices) {
      // If quantization already exists for this device, append engine
      if (quantName in sources[device as keyof Sources]) {
        // New engine is not default since we already have engines
        const engineConfigCopy = { ...engineConfig, is_default: false }
        sources[device as keyof Sources][quantName].available_engines.push(engineConfigCopy)
      } else {
        // First engine for this quantization
        sources[device as keyof Sources][quantName] = { ...quantConfig }
        // Set as default if it matches device's default quantization
        if (device in defaultQuantizations && defaultQuantizations[device as keyof typeof defaultQuantizations] === quantName) {
          sources[device as keyof Sources][quantName].is_default = true
        }
      }
    }
  }

  // Validate exactly one default quantization per device type
  for (const device of validDevices) {
    const defaultCount = Object.values(sources[device as keyof Sources]).filter(
      quant => quant.is_default
    ).length
    if (defaultCount === 0) {
      throw new Error(`No default quantization specified for device type: ${device}`)
    } else if (defaultCount > 1) {
      throw new Error(`Multiple default quantizations specified for device type: ${device}`)
    }
  }

  return sources
}

export function generateStandardContract(name: string, description: string): Contract {
  return {
    name,
    description,
    methods: [
      {
        name: '__init__',
        description: `Initialize ${name} model with specified engine and configuration`,
        arguments: [
          {
            name: 'engine',
            type: 'string | string[]',
            schema: {},
            description: 'Name of the engine to use (e.g. transformers, mlx-lm, llama.cpp) or list of engines in order of priority',
            required: false,
          },
          {
            name: 'quantization',
            type: 'string | string[] | object',
            schema: {
              nested: [
                {
                  name: 'default',
                  type: 'string',
                  schema: {},
                  description: 'Default quantization method',
                  required: false,
                },
                {
                  name: 'minPrecision',
                  type: 'string',
                  schema: {},
                  description: 'Minimum precision requirement (e.g. "4bit")',
                  required: false,
                },
                {
                  name: 'maxPrecision',
                  type: 'string',
                  schema: {},
                  description: 'Maximum precision requirement (e.g. "8bit")',
                  required: false,
                },
                {
                  name: 'max_memory_allocation',
                  type: 'number',
                  schema: {},
                  description: 'Maximum memory allocation as fraction of available memory',
                  required: false,
                },
              ],
            },
            description: 'Quantization method to use (e.g. bfloat16, Q4_K_M, MLX_4) or list of methods in order of priority, or dictionary of quantization settings',
            required: false,
          },
          {
            name: 'max_memory_allocation',
            type: 'number',
            schema: {},
            description: 'Maximum memory allocation as fraction of available memory',
            required: false,
          },
          {
            name: 'configuration',
            type: 'object',
            schema: {
              nested: [
                {
                  name: 'model',
                  type: 'object',
                  schema: {},
                  description: 'Model-specific configuration parameters',
                  required: false,
                },
                {
                  name: 'processor',
                  type: 'object',
                  schema: {
                    nested: [
                      {
                        name: 'input',
                        type: 'object',
                        schema: {},
                        description: 'Input processor configuration',
                        required: false,
                      },
                      {
                        name: 'output',
                        type: 'object',
                        schema: {},
                        description: 'Output processor configuration',
                        required: false,
                      },
                    ],
                  },
                  description: 'Processor configuration parameters',
                  required: false,
                },
              ],
            },
            description: 'Optional configuration dictionary for model, processor, and other settings',
            required: false,
          },
        ],
        outputs: [
          {
            type: 'void',
            description: 'No return value',
            required: true,
          } as Output,
        ],
      },
      {
        name: 'process',
        description: 'Process input through the model',
        arguments: [
          {
            name: 'input',
            type: 'string | Message[]',
            schema: {
              nested: [
                {
                  name: 'role',
                  type: 'string',
                  schema: { pattern: '^(system|user|assistant)$' },
                  description: 'The role of the message sender',
                  required: true,
                },
                {
                  name: 'content',
                  type: 'string',
                  schema: {},
                  description: 'The content of the message',
                  required: true,
                },
              ],
            },
            description: 'Input string or list of messages in chat format',
            required: true,
          },
          {
            name: 'context',
            type: 'any[]',
            schema: {},
            description: 'Optional context items to prepend as system messages',
            required: false,
          },
          {
            name: 'configuration',
            type: 'object',
            schema: {
              nested: [
                {
                  name: 'max_new_tokens',
                  type: 'number',
                  schema: { maxLength: 2048 },
                  description: 'Maximum number of tokens to generate',
                  required: false,
                },
                {
                  name: 'temperature',
                  type: 'number',
                  schema: { pattern: '^[0-9]+(.[0-9]+)?$' },
                  description: 'Sampling temperature (higher = more random)',
                  required: false,
                },
                {
                  name: 'top_p',
                  type: 'number',
                  schema: { pattern: '^[0-9]+(.[0-9]+)?$' },
                  description: 'Nucleus sampling probability threshold',
                  required: false,
                },
                {
                  name: 'top_k',
                  type: 'number',
                  schema: { pattern: '^[0-9]+$' },
                  description: 'Top-k sampling threshold',
                  required: false,
                },
                {
                  name: 'do_sample',
                  type: 'boolean',
                  schema: {},
                  description: 'Whether to use sampling (false = greedy)',
                  required: false,
                },
                {
                  name: 'repetition_penalty',
                  type: 'number',
                  schema: { pattern: '^[0-9]+(.[0-9]+)?$' },
                  description: 'Penalty for repeating tokens',
                  required: false,
                },
              ],
            },
            description: 'Optional generation configuration parameters',
            required: false,
          },
          {
            name: 'remember',
            type: 'boolean',
            schema: {},
            description: 'Whether to remember this interaction in history',
            required: false,
          },
          {
            name: 'keep_alive',
            type: 'boolean',
            schema: {},
            description: 'Keep model loaded for faster consecutive interactions',
            required: false,
          },
        ],
        outputs: [
          {
            type: '[string, object]',
            description: 'Generated response and processing logs',
            required: true,
          } as Output,
        ],
      },
      {
        name: 'load',
        description: 'Load model into memory based on engine type',
        arguments: [],
        outputs: [
          {
            type: 'void',
            description: 'No return value',
            required: true,
          } as Output,
        ],
      },
      {
        name: 'unload',
        description: 'Unload model from memory and free resources',
        arguments: [],
        outputs: [
          {
            type: 'void',
            description: 'No return value',
            required: true,
          } as Output,
        ],
      },
      {
        name: 'loaded',
        description: 'Check if model is loaded',
        arguments: [],
        outputs: [
          {
            type: 'boolean',
            description: 'True if model is loaded, false otherwise',
            required: true,
          } as Output,
        ],
      },
      {
        name: 'configuration',
        description: 'Get a copy of the model\'s configuration',
        arguments: [],
        outputs: [
          {
            type: 'object',
            description: 'A copy of the model\'s configuration',
            required: true,
          } as Output,
        ],
      },
      {
        name: 'reset',
        description: 'Reset model chat history',
        arguments: [],
        outputs: [
          {
            type: 'void',
            description: 'No return value',
            required: true,
          } as Output,
        ],
      },
      {
        name: 'contract',
        description: 'Get a copy of the model\'s contract specification, which describes its capabilities, methods, and interfaces. This is useful for programmatically understanding the model\'s features and requirements.',
        arguments: [],
        outputs: [
          {
            type: 'Contract',
            description: 'A copy of the model\'s contract specification',
            required: true,
          } as Output,
        ],
      },
      {
        name: 'compatibility',
        description: 'Get a copy of the model\'s compatibility specifications, detailing supported engines, quantization methods, devices, memory requirements, and dependencies. This helps determine if the model can run in a given environment.',
        arguments: [],
        outputs: [
          {
            type: 'Compatibility[]',
            description: 'A list of the model\'s compatibility specifications',
            required: true,
          } as Output,
        ],
      },
    ],
  }
}

export function generateStandardCompatibility(sources: Sources): Compatibility[] {
  const compatibilities: Compatibility[] = []

  // Process each device type (e.g. webgpu)
  for (const [deviceType, deviceSources] of Object.entries(sources)) {
    // Process each quantization method for this device
    for (const [quantization, quantConfig] of Object.entries(deviceSources)) {
      // Get available engines for this quantization
      const engines = quantConfig.available_engines

      // Process each engine
      for (const engineConfig of engines) {
        const engine = engineConfig.name

        // Create base compatibility entry
        const compatibility: Compatibility = {
          engine,
          quantization,
          devices: [deviceType],
          memory: quantConfig.memory,
          dependencies: [],
          precision: quantConfig.precision,
        }

        // Set dependencies based on engine type
        if (engine === 'webgpu') {
          compatibility.dependencies = [
            'web-llm',
          ]
        }
        compatibilities.push(compatibility)
      }
    }
  }

  return compatibilities
}
