import { MLCEngine } from "@mlc-ai/web-llm"

import { QuantizationSettings , Message, Contract, Compatibility } from '../../../../../core/types'
import { AbstractUniversalModel } from '../../../../../core/UniversalModel'

import { extractPrecisionFromDescriptor } from './meta'
import { InferenceConfiguration, ModelConfiguration, ProcessorConfiguration, Sources, QuantizationConfig } from './types'


export abstract class UniversalModelMixin extends AbstractUniversalModel {
  private _name: string
  private _sources: Sources
  private _modelConfiguration: ModelConfiguration
  private _inferenceConfiguration: InferenceConfiguration
  private _processorConfiguration: ProcessorConfiguration
  private _engine: string
  private _quantization: string
  private _usableMemory: number
  private _config: any
  private _model: MLCEngine | undefined
  private _history: any[]
  private _streamingCallback: ((chunk: string) => void) | null = null
  private _initializationPromise: Promise<void> | null = null
  private _initializationError: Error | null = null

  private async _getAvailableMemory(deviceType: string = 'webgpu'): Promise<number> {
    if (deviceType === 'webgpu') {
      try {
        // Get WebGPU adapter and device
        const adapter = await navigator.gpu?.requestAdapter()
        if (!adapter) {
          console.error('[Unsupported Browser] WebGPU is not supported in this browser, please try a different browser (e.g. Chrome).')
          return 0
        }

        // Get adapter limits
        const limits = adapter.limits
        if (!limits) {
          console.error('[Memory] WebGPU adapter limits are not available')
          return 0
        }

        // For WebGPU, we'll use a combination of:
        // 1. The maximum buffer size limits
        // 2. A conservative estimate based on system memory
        const maxBufferSize = limits.maxBufferSize || 0
        const maxStorageBufferBindingSize = limits.maxStorageBufferBindingSize || 0
        
        if (maxBufferSize === 0 || maxStorageBufferBindingSize === 0) {
          console.error('[Memory] WebGPU memory limits are not properly initialized')
          return 0
        }

        // Calculate base available memory from buffer limits
        const baseAvailableBytes = Math.min(maxBufferSize, maxStorageBufferBindingSize)
        
        // If we have a model loaded, estimate its memory usage
        let modelMemoryUsage = 0
        if (this._model) {
          // Estimate model memory usage based on quantization and configuration
          const deviceSources = this._sources['webgpu']
          if (deviceSources && this._quantization) {
            const quantization = deviceSources[this._quantization]
            if (quantization) {
              // Use the memory requirement from the quantization config
              modelMemoryUsage = quantization.memory * (1024 * 1024 * 1024) // Convert GB to bytes
            }
          }
        }

        // Calculate available memory by subtracting model usage from base available
        const availableMemoryBytes = Math.max(0, baseAvailableBytes - modelMemoryUsage)
        
        // Convert to GB (1 GB = 1024^3 bytes)
        const availableMemoryGB = availableMemoryBytes / (1024 * 1024 * 1024)
        
        return availableMemoryGB
      } catch (error) {
        console.error('[Memory] Error accessing WebGPU adapter limits:', error)
        return 0
      }
    }
    return 0
  }

  constructor(
    interfaceConfig: {
      name: string;
      sources: Sources;
      model_configuration: ModelConfiguration;
      inference_configuration: InferenceConfiguration;
      processor_configuration: ProcessorConfiguration;
    },
    payload?: {
      engine?: string | string[],
      quantization?: string | string[] | QuantizationSettings,
      maxMemoryAllocation?: number,
      configuration?: Record<string, any>
    } | undefined
  ) {
    const { engine, quantization, maxMemoryAllocation, configuration } = payload || {}
    super(payload)

    // Validate interface configuration
    if (!interfaceConfig.name) {
      throw new Error("[UniversalModelMixin:constructor:interface_config] Name is not implemented")
    }
    if (!interfaceConfig.sources) {
      throw new Error("[UniversalModelMixin:constructor:interface_config] Sources are not implemented")
    }
    if (!interfaceConfig.model_configuration) {
      throw new Error("[UniversalModelMixin:constructor:interface_config] Model configuration is not implemented")
    }
    if (!interfaceConfig.inference_configuration) {
      throw new Error("[UniversalModelMixin:constructor:interface_config] Inference configuration is not implemented")
    }
    if (!interfaceConfig.processor_configuration) {
      throw new Error("[UniversalModelMixin:constructor:interface_config] Processor configuration is not implemented")
    }

    // Define the interface configuration
    this._name = interfaceConfig.name
    this._sources = interfaceConfig.sources
    this._modelConfiguration = interfaceConfig.model_configuration
    this._inferenceConfiguration = interfaceConfig.inference_configuration
    this._processorConfiguration = interfaceConfig.processor_configuration

    // Initialize other properties
    this._engine = ''
    this._quantization = ''
    this._usableMemory = 0.85
    this._config = configuration || {}
    this._model = undefined
    this._history = []
    this._streamingCallback = null

    // Start async initialization
    this._initializationPromise = this._initializeAsync(engine, quantization, maxMemoryAllocation)
      .catch(error => {
        this._initializationError = error
        console.error('[Initialization] Error during async initialization:', error)
        throw error
      })
  }

  async ready(): Promise<void> {
    if (this._initializationError) {
      throw this._initializationError
    }
    if (this._initializationPromise) {
      await this._initializationPromise
    }
  }

  private async _initializeAsync(
    engine: string | string[] | null | undefined,
    quantization: string | string[] | QuantizationSettings | null | undefined,
    maxMemoryAllocation: number | null | undefined
  ): Promise<void> {
    // Detect device type
    let deviceType = 'webgpu' // default for now, but prepared for future devices
    let deviceWarning = ''

    // For now we only support WebGPU, but the structure is ready for future devices
    if (!navigator.gpu) {
      deviceWarning += '\n[Warning] WebGPU is not supported in this browser.'
    }

    console.log(`[Device Detection] Using device type: ${deviceType}${deviceWarning}`)

    // Get device-specific sources
    const deviceSources: Record<string, QuantizationConfig> = this._sources[deviceType] || this._sources['webgpu'] // fallback to webgpu if device not found
    console.log(`[Device Sources] Available sources for ${deviceType}: ${Object.keys(deviceSources)}`)

    // Set maximum memory allocation (default: 85% of available memory)
    if (maxMemoryAllocation) {
      if (maxMemoryAllocation >= 0 && maxMemoryAllocation <= 1) {
        this._usableMemory = maxMemoryAllocation
        console.log(`[Memory Allocation] Using custom max memory allocation: ${this._usableMemory * 100}%`)
      } else {
        throw new Error(`Invalid max_memory value: ${maxMemoryAllocation} (percentage must be between 0 and 1 inclusive)`)
      }
    }

    // Set quantization based on device-specific defaults or user input
    if (quantization === null || quantization === undefined) {
      console.log("[Quantization Selection] No quantization specified, using automatic selection")
      // Default case - use current logic but cap minimum precision to 4 bit
      const defaultQuant = Object.entries(deviceSources)
        .find(([_, source]) => source.is_default)?.[0]
      if (!defaultQuant) {
        throw new Error("No default quantization found for device")
      }

      const requiredMemory = deviceSources[defaultQuant].memory
      const availableMemory = await this._getAvailableMemory(deviceType) * this._usableMemory

      console.log(`[Memory Check] Default quantization '${defaultQuant}' requires ${requiredMemory}GB, available: ${availableMemory.toFixed(2)}GB`)

      // If default quantization fits within 80% of available memory, use it
      if (requiredMemory <= availableMemory) {
        this._quantization = defaultQuant
        console.log(`[Decision] Using default quantization '${defaultQuant}' as it fits in available memory`)
      } else {
        console.log("[Incompatibility] Default quantization doesn't fit, searching for alternatives")
        // Otherwise find the largest quantization that fits with minimum 4 bit precision
        const quantizations = Object.entries(deviceSources)
          .sort((a, b) => b[1].memory - a[1].memory)

        for (const [quant, source] of quantizations) {
          if (source.precision >= 4) { // Minimum 4 bit precision
            if (source.memory <= availableMemory) {
              this._quantization = quant
              console.log(`[Decision] Found suitable quantization '${quant}' with ${source.precision}-bit precision requiring ${source.memory}GB`)
              break
            } else {
              console.log(`[Assessment] Quantization '${quant}' does not fit within available memory`)
            }
          } else {
            console.log(`[Assessment] Quantization '${quant}' does not meet minimum 4-bit precision`)
          }
        }

        if (!this._quantization) {
          throw new Error(`No quantization with minimum 4-bit precision found that fits within ${this._usableMemory * 100}% of the available memory (${availableMemory.toFixed(2)}GB)`)
        }
      }
    } else if (typeof quantization === 'string') {
      console.log(`[Quantization Selection] Using specified quantization: ${quantization}`)
      this._quantization = quantization
    } else if (Array.isArray(quantization)) {
      console.log(`[Quantization Selection] Trying quantizations from list: ${quantization}`)
      for (const quant of quantization) {
        if (quant in deviceSources) {
          this._quantization = quant
          console.log(`[Decision] Using quantization '${quant}' from provided list`)
          break
        }
      }
      if (!this._quantization) {
        throw new Error(`No quantization from the provided list ${quantization} is supported for ${deviceType}`)
      }
    } else {
      console.log("[Quantization Selection] Using QuantizationSettings configuration")
      // Get min and max precision from settings
      let minPrecision = 4 // Default minimum
      let maxPrecision = 8 // Default maximum

      if (quantization.minPrecision) {
        minPrecision = extractPrecisionFromDescriptor(quantization.minPrecision)
        console.log(`[Precision] Using custom min precision: ${minPrecision} bits`)
      } else if (quantization.default) {
        const defaultQuant = quantization.default
        if (defaultQuant in deviceSources) {
          minPrecision = Math.min(4, deviceSources[defaultQuant].precision)
          console.log(`[Precision] Using min precision from default quantization '${defaultQuant}': ${minPrecision} bits`)
        }
      }

      if (quantization.maxPrecision) {
        maxPrecision = extractPrecisionFromDescriptor(quantization.maxPrecision)
        console.log(`[Precision] Using custom max precision: ${maxPrecision} bits`)
      } else if (quantization.default) {
        const defaultQuant = quantization.default
        if (defaultQuant in deviceSources) {
          maxPrecision = deviceSources[defaultQuant].precision
          console.log(`[Precision] Using max precision from default quantization '${defaultQuant}': ${maxPrecision} bits`)
        }
      }

      // Find the highest precision quantization that fits within max allowed memory allocation
      const availableMemory = await this._getAvailableMemory(deviceType) * this._usableMemory
      console.log(`[Memory Check] Available memory for quantization: ${availableMemory.toFixed(2)}GB`)

      const quantizations = Object.entries(deviceSources)
        .sort((a, b) => b[1].precision - a[1].precision)

      for (const [quant, source] of quantizations) {
        if (minPrecision <= source.precision && source.precision <= maxPrecision) {
          console.log(`[Checking] Quantization '${quant}' - Precision: ${source.precision} bits, Required memory: ${source.memory}GB`)
          if (source.memory <= availableMemory) {
            this._quantization = quant
            console.log(`[Decision] Selected quantization '${quant}' with ${source.precision}-bit precision requiring ${source.memory}GB`)
            break
          } else {
            console.log(`[Assessment] Quantization '${quant}' does not fit within available memory`)
          }
        } else {
          console.log(`[Assessment] Quantization '${quant}' does not meet precision requirements`)
        }
      }

      if (!this._quantization) {
        throw new Error(`No quantization found with precision between ${minPrecision} and ${maxPrecision} bits that fits within ${this._usableMemory * 100}% of the available memory (${availableMemory.toFixed(2)}GB)`)
      }
    }

    // Validate quantization is supported for this device
    const supportedQuantizations = Object.keys(deviceSources)
    if (!supportedQuantizations.includes(this._quantization)) {
      throw new Error(`Quantization ${this._quantization} not supported for ${deviceType}. Use one of ${supportedQuantizations}`)
    }

    // Get available engines for the selected quantization
    const availableEngines = deviceSources[this._quantization].available_engines
    console.log(`[Engine Selection] Available engines for quantization '${this._quantization}': ${availableEngines.map(e => e.name)}`)

    // Set engine based on user input or default
    if (!engine) {
      // Find the default engine for this quantization
      const defaultEngine = availableEngines.find(e => e.is_default)?.name
      if (!defaultEngine) {
        // If no default is marked, use the first available engine
        this._engine = availableEngines[0].name
      } else {
        this._engine = defaultEngine
      }
      console.log(`[Decision] Using default engine '${this._engine}' for quantization '${this._quantization}'`)
    } else if (typeof engine === 'string') {
      this._engine = engine
    } else if (Array.isArray(engine)) {
      console.log(`[Engine Selection] Trying engines from list: ${engine}`)
      // If engine is a list, try each engine in order until finding a supported one
      const supportedEngines = new Set(availableEngines.map(e => e.name))
      for (const engineName of engine) {
        if (supportedEngines.has(engineName)) {
          this._engine = engineName
          console.log(`[Decision] Using engine '${engineName}' from provided list`)
          break
        }
      }
      if (!this._engine) {
        throw new Error(`No engine from the provided list ${engine} is supported for ${deviceType} device with quantization ${this._quantization}. Use one of ${Array.from(supportedEngines)}`)
      }
    }

    // Validate engine is supported for this device and quantization
    const supportedEngines = new Set(availableEngines.map(e => e.name))
    if (!supportedEngines.has(this._engine)) {
      throw new Error(`Engine ${this._engine} not supported for ${deviceType} device with quantization ${this._quantization}. Use one of ${Array.from(supportedEngines)}`)
    }

    // Store the selected engine configuration for later use
    const engineConfig = availableEngines.find(e => e.name === this._engine)
    if (!engineConfig) {
      throw new Error(`Engine configuration not found for ${this._engine}`)
    }

    console.log(`[Proceeding] Using engine '${this._engine}' with quantization '${this._quantization}' on ${deviceType} device\n`)
    console.log(`[Proceeding] Initializing model: ${this._name}`)
    console.log(`[Proceeding] Device: ${deviceType}, Engine: ${this._engine}, Quantization: ${this._quantization}, Config: ${JSON.stringify(this._config)}`)
  }

  async loaded(): Promise<boolean> {
    // Wait for model to be ready
    await this.ready()
    return !!this._model
  }

  async reset(): Promise<void> {
    // Wait for model to be ready
    await this.ready()
    if (this._engine !== 'webllm') {
      try {
        this._model?.resetChat(this._modelConfiguration[this._engine].model_id)
      } catch (error) {
        console.warn('[Reset] Warning:', error)
      }
    }
    this._history = []
  }

  private _translateModelConfig(config: any = {}): any {
    if (this._engine !== 'webllm') {
      return {}
    }
    return {
      ...(config?.max_new_tokens ? { max_tokens: config.max_new_tokens } : {}),
      ...(config?.temperature ? { temperature: config.temperature } : {}),
      ...(config?.top_p ? { top_p: config.top_p } : {}),
      ...(config?.repetition_penalty ? { repetition_penalty: config.repetition_penalty } : {}),
      ...(config?.stop ? { stop: config.stop } : {}),
      ...(config?.logit_bias ? { logit_bias: config.logit_bias } : {}),
      ...(config?.num_return_sequences ? { n: config.num_return_sequences } : {}),
      ...(config?.ignore_eos !== undefined ? { ignore_eos: config.ignore_eos } : {})
    }
  }

  private _translateInferenceConfig(config: any = {}): any {
    if (this._engine !== 'webllm') {
      return {}
    }
    return {
      ...(config?.max_new_tokens ? { max_tokens: config.max_new_tokens } : {}),
      ...(config?.temperature ? { temperature: config.temperature } : {}),
      ...(config?.top_p ? { top_p: config.top_p } : {}),
      ...(config?.repetition_penalty ? { repetition_penalty: config.repetition_penalty } : {}),
      ...(config?.stop ? { stop: config.stop } : {}),
      ...(config?.logit_bias ? { logit_bias: config.logit_bias } : {}),
      ...(config?.num_return_sequences ? { n: config.num_return_sequences } : {}),
      ...(config?.ignore_eos !== undefined ? { ignore_eos: config.ignore_eos } : {})
    }
  }

  async load(): Promise<void> {
    // Wait for model to be ready
    await this.ready()

    if (this._model) {
      console.log('[Model] Model already loaded')
      return
    }

    if (this._engine !== 'webllm') {
      throw new Error(`Engine ${this._engine} not supported yet`)
    }

    // Get model ID from sources
    const deviceSources = this._sources['webgpu']
    if (!deviceSources) {
      throw new Error('No sources found for webgpu or webllm')
    }

    const quantization = deviceSources[this._quantization]
    if (!quantization) {
      throw new Error(`No quantization ${this._quantization} found in sources`)
    }

    const engineConfig = quantization.available_engines.find(e => e.name === this._engine)
    if (!engineConfig) {
      throw new Error(`No engine configuration found for ${this._engine} in quantization ${this._quantization}`)
    }

    const modelId = engineConfig.model_id
    if (!modelId) {
      throw new Error(`No model_id found for engine ${this._engine} in quantization ${this._quantization}`)
    }

    // Log initial memory state
    const initialMemory = await this._getAvailableMemory('webgpu')
    console.log(`[Memory Pre-Load] Available memory: ${initialMemory.toFixed(2)}GB`)

    try {
      // Initialize with progress callback
      const initProgressCallback = (progress: any) : void => {
        console.debug(`[Model] ${progress?.text}`, { details: progress })
      }

      console.log("[Model] Loading model..")

      // Create MLCEngine instance
      this._model = new MLCEngine({
        initProgressCallback
      })

      // Load the model with generation config
      await this._model.reload(
        modelId,
        this._translateModelConfig({
          ...this._modelConfiguration[this._engine],
          ...this._config?.model
        })
      )

      // Log memory state after loading
      const postLoadMemory = await this._getAvailableMemory('webgpu')
      console.log(`[Memory Post-Load]Available memory: ${postLoadMemory.toFixed(2)}GB`)
      console.log(`[Memory Post-Load] Memory used by model: ${(initialMemory - postLoadMemory).toFixed(2)}GB`)
      console.log('[Model] Model loaded successfully')
    } catch (error) {
      console.error('[Model] Loading Error:', error)
      this._model = undefined
      throw error
    }
  }

  async unload(): Promise<void> {
    // Wait for model to be ready
    await this.ready()

    // Log memory state before unloading
    const preUnloadMemory = await this._getAvailableMemory('webgpu')
    console.log(`[Memory Pre-Unload] Available memory: ${preUnloadMemory.toFixed(2)}GB`)

    if (this._engine !== 'webllm') {
      try {
        await this._model?.unload()
      } catch (error) {
        console.warn('[Model] Unloading Warning:', error)
      }
    }

    this._model = undefined
    this._streamingCallback = null

    // Log memory state after unloading
    const postUnloadMemory = await this._getAvailableMemory('webgpu')
    console.log(`[Memory Post-Unload] Available memory: ${postUnloadMemory.toFixed(2)}GB`)
    console.log(`[Memory Post-Unload] Memory freed: ${(postUnloadMemory - preUnloadMemory).toFixed(2)}GB`)
    console.log('[Model] Model unloaded successfully')
  }

  async process(input: string | Message[], payload? : {
    context?: any[],
    configuration?: Record<string, any>,
    remember?: boolean,
    keepAlive?: boolean,
    stream?: boolean
  }): Promise<[string, any]> {
    const { context, configuration, remember, keepAlive, stream } = payload || {}
    console.log("[Model] Request received..", { ask: { input, optionalPayload: payload }})

    // Wait for model to be ready
    await this.ready()

    // Load model if not loaded
    if (!this._model) {
      await this.load()
    }
    console.log("[Model] Model ready. Continuing..")
    console.log("[Model] Processing input..", { ask: { input, optionalPayload: payload }})

    // Convert input to messages format if string
    const messages = Array.isArray(input) ? input : [{ role: 'user', content: input }]

    // Add context if provided
    if (context) {
      messages.unshift(...context.map(ctx => ({ role: 'system', content: String(ctx) })))
    }

    // Add history to current messages
    if (this._history.length > 0) {
      messages.unshift(...this._history)
    }

    try {
      // Configure streaming
      this._streamingCallback = configuration?.onStream ?? null

      // Create chat completion
      const reply = await this._model?.chat.completions.create({
        messages,
        ...this._translateInferenceConfig({
          ...this._inferenceConfiguration[this._engine],
          ...configuration,
          stream
        })
      })

      // Handle streaming if enabled
      if (stream && this._streamingCallback) {
        let fullReply = ''
        if (!reply) {
          return ['', { engine: this._engine, quantization: this._quantization }]
        }
        const stream = reply as unknown as AsyncIterable<{ choices: Array<{ delta: { content: string } }> }>
        for await (const chunk of stream) {
          const content = chunk.choices[0]?.delta.content || ''
          fullReply += content
          this._streamingCallback(content)
        }
        return [fullReply, { engine: this._engine, quantization: this._quantization }]
      }

      // Handle non-streaming response
      const response = reply?.choices[0].message.content
      
      // Update history if remember is true
      if (remember) {
        this._history = [...messages, { role: 'assistant', content: response }]
      }

      // Unload model if keepAlive is false
      if (!keepAlive) {
        await this.unload()
      }

      console.log("[Model] Processing completed.", { output: { response }})
      return [response ?? '', { engine: this._engine, quantization: this._quantization }]
    } catch (error) {
      console.error('[Process] Error:', error)
      if (!keepAlive) {
        await this.unload()
      }
      throw error
    }
  }

  async configuration(): Promise<any> {
    // Wait for model to be ready
    await this.ready()
    return {
      engine: this._engine,
      quantization: this._quantization,
      model_config: this._translateModelConfig({
        ...this._modelConfiguration[this._engine],
        ...this._config?.model
      }),
      inference_config: this._translateInferenceConfig(this._inferenceConfiguration[this._engine]),
      processor_config: this._processorConfiguration[this._engine]
    }
  }

  static contract(): Contract {
    throw new Error('Method not implemented')
  };

  static compatibility(): Compatibility[] {
    throw new Error('Method not implemented')
  };

  abstract contract(): Contract;

  abstract compatibility(): Compatibility[];
}

export default UniversalModelMixin