import { Logger, LogLevel } from '../../../../../community/__utils__/logger'
import { Message, Contract, Compatibility } from '../../../../../core/types'
import { AbstractUniversalModel } from '../../../../../core/UniversalModel'

import { InferenceConfiguration } from './types'

export abstract class UniversalModelMixin extends AbstractUniversalModel {
    private _credentials: { api_key: string; http_referrer?: string; x_title?: string }
    private _inferenceConfiguration: InferenceConfiguration
    private _logger: Logger
    public name: string
    public engine: string
    public history: Array<{ role: string; content: string }>

    constructor(
        interfaceConfig: { name: string; inference_configuration: InferenceConfiguration },
        payload?: {
            credentials?: string | { api_key: string; http_referrer?: string; x_title?: string },
            verbose?: boolean | string
        } | undefined
    ) {
        super(payload)
        const { credentials, verbose } = payload || {}
        
        if (typeof verbose === 'string') {
          this._logger = new Logger(LogLevel[verbose as keyof typeof LogLevel])
        } else if (typeof verbose === 'boolean') {
          this._logger = new Logger(verbose ? LogLevel.DEBUG : LogLevel.NONE)
        } else {
          this._logger = new Logger()
        }

        if (!interfaceConfig.name) {
            throw new Error("[UniversalModelMixin:contructor:interfaceConfig] Name is not implemented")
        }
        if (!interfaceConfig.inference_configuration) {
            throw new Error("[UniversalModelMixin:contructor:interfaceConfig] Inference configuration is not implemented")
        }

        this._logger.log(`* Initializing model.. (${interfaceConfig.name}) *`)
        
        // Validate credentials
        this._logger.log("[Credentials] Validating credentials..")
        if (credentials) {
            if (typeof credentials === 'string') {
                this._credentials = { api_key: credentials }
            } else {
                this._credentials = credentials
            }
        } else {
            this._logger.error("[Credentials] No credentials provided. Please provide a valid OpenRouter API key.")
            throw new Error("[UniversalModelMixin:constructor:credentials] Missing credentials. Please provide a valid OpenRouter API key.")
        }
        this._logger.log("[Credentials] Credentials found. Please ensure you have sufficient credits to use the model.")
        
        // Store interface config
        this._logger.log("[Model] Setting up model configuration..")
        this._inferenceConfiguration = interfaceConfig.inference_configuration
        this.name = interfaceConfig.name
        this.engine = "openrouter"
        this.history = []
        
        this._logger.log(`[Model] Initialized remote model: ${this.name}`)
        this._logger.log(`[Model] Device: cloud, Engine: ${this.engine}`)
    }

    private _translateGenerationConfig(configuration?: Record<string, any>): Record<string, any> {
     
        const result = { ...this._inferenceConfiguration[this.engine] }
        
        if (configuration) {
            Object.assign(result, configuration)
        }

        // translate to openrouter format
        const openrouterParams: Record<string, any> = {}
        
        // Map parameters to OpenRouter format
        if ("temperature" in result) openrouterParams.temperature = result.temperature
        if ("max_new_tokens" in result) openrouterParams.max_tokens = result.max_new_tokens
        if ("top_p" in result) openrouterParams.top_p = result.top_p
        if ("top_k" in result) openrouterParams.top_k = result.top_k
        if ("presence_penalty" in result) openrouterParams.presence_penalty = result.presence_penalty
        if ("frequency_penalty" in result) openrouterParams.frequency_penalty = result.frequency_penalty
        if ("repetition_penalty" in result) openrouterParams.repetition_penalty = result.repetition_penalty
        if ("min_p" in result) openrouterParams.min_p = result.min_p
        if ("top_a" in result) openrouterParams.top_a = result.top_a
        if ("seed" in result) openrouterParams.seed = result.seed
        if ("response_format" in result) openrouterParams.response_format = result.response_format
        if ("structured_output" in result) openrouterParams.structured_output = result.structured_output
        if ("stop" in result) openrouterParams.stop = result.stop

        this._logger.debug(`[Generation Config] Engine: ${this.engine}`)
        this._logger.debug(`[Generation Config] Input config:`, configuration)
        this._logger.debug(`[Generation Config] Translated config:`, openrouterParams)

        return openrouterParams
    }

    async process(
        input: string | Message[],
        payload?: {
            context?: any[],
            configuration?: Record<string, any>,
            remember?: boolean
        } | undefined
    ): Promise<[any, Record<string, any>]> {
        const { context, configuration, remember} = payload || {}
        this._logger.log(`* Invoking remote model.. (${this.name}) *`)
        
        if (!input) {
            throw new Error("Input is required")
        }

        this._logger.log("[Model] Translating input..")

        // Convert input to messages format if string
        const messages = Array.isArray(input) ? input : [{ role: "user", content: input }]

        // Add context if provided
        if (context) {
            const contextMessages = context.map(ctx => ({ role: "system", content: String(ctx) }))
            messages.unshift(...contextMessages)
        }

        // Add history to current messages
        if (this.history.length) {
            messages.unshift(...this.history)
        }

        this._logger.debug('[Model] Translated input: ', { input: JSON.stringify(messages) })
        
        // Translate generation configuration
        this._logger.log("[Model] Translating inference configuration..")
        const generationConfig = this._translateGenerationConfig(configuration)

        this._logger.log("[Model] Generating output..")

        // Process input through OpenRouter
        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: 'POST',
            headers: {
                "Authorization": `Bearer ${this._credentials.api_key}`,
                "HTTP-Referer": this._credentials.http_referrer || '',
                "X-Title": this._credentials.x_title || '',
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: this.name,
                messages,
                ...generationConfig
            })
        })
        
        if (response.status >= 400) {
            this._logger.error("[Model] Error generating output.")
            throw new Error("[UniversalModelMixin:process] Error generating output.")
        }
        
        const responseData = await response.json()
        const output = responseData.choices[0].message.content
        
        this._logger.log("[Model] Generation complete")

        // Update history if remember is True
        if (remember) {
            this.history = [...messages, { role: "assistant", content: output }]
        }

        this._logger.debug('[Model] Response: ', { response: JSON.stringify(responseData) })

        return [output, { engine: this.engine }]
    }

    async load(): Promise<void> {
        this._logger.log(`* Loading model.. (${this.name}) *`)
        this._logger.warn("[Model] No local model to load. Model is remote (cloud-based).")
        return Promise.resolve()
    }

    async unload(): Promise<void> {
        this._logger.log(`* Unloading model.. (${this.name}) *`)
        this._logger.warn("[Model] No local model to unload. Model is remote (cloud-based).")
        return Promise.resolve()
    }

    async loaded(): Promise<boolean> {
        return Promise.resolve(this.name !== null)
    }

    async configuration(): Promise<Record<string, any>> {
        const config = {
            engine: this.engine,
            inference_config: this._translateGenerationConfig(),
        }
        return Promise.resolve(config)
    }

    async reset(): Promise<void> {
        this.history = []
        return Promise.resolve()
    }

    async ready(): Promise<void> {
        return Promise.resolve()
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
