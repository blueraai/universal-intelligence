import { Compatibility, Contract } from '../../../../../core/types'

export function generateStandardContract(name: string, description: string): Contract {
    return {
        name,
        description,
        methods: [
            {
                name: "__init__",
                description: `Initialize ${name} model with specified engine and configuration`,
                arguments: [
                    {
                        name: "credentials",
                        type: "string | Record<string, any>",
                        schema: {},
                        description: "OpenRouter API credentials",
                        required: true,
                    },
                    {
                        name: "verbose",
                        type: "boolean | string",
                        schema: {
                            oneOf: [
                                "DEFAULT",
                                "NONE",
                                "INFO",
                                "DEBUG",
                            ]
                        },
                        description: "Verbose output",
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
                name: "process",
                description: "Process input through the model",
                arguments: [
                    {
                        name: "input",
                        type: "string | Message[]",
                        schema: {
                            nested: [
                                {
                                    name: "role",
                                    type: "string",
                                    schema: { pattern: "^(system|user|assistant)$" },
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
                        schema: {
                            nested: [
                                {
                                    name: "max_new_tokens",
                                    type: "number",
                                    schema: { maxLength: 2048 },
                                    description: "Maximum number of tokens to generate",
                                    required: false,
                                },
                                {
                                    name: "temperature",
                                    type: "number",
                                    schema: { pattern: "^[0-9]+(.[0-9]+)?$" },
                                    description: "Sampling temperature (higher = more random)",
                                    required: false,
                                },
                                {
                                    name: "top_p",
                                    type: "number",
                                    schema: { pattern: "^[0-9]+(.[0-9]+)?$" },
                                    description: "Nucleus sampling probability threshold",
                                    required: false,
                                },
                                {
                                    name: "top_k",
                                    type: "number",
                                    schema: { pattern: "^[0-9]+$" },
                                    description: "Top-k sampling threshold",
                                    required: false,
                                },
                                {
                                    name: "do_sample",
                                    type: "boolean",
                                    schema: {},
                                    description: "Whether to use sampling (False = greedy)",
                                    required: false,
                                },
                                {
                                    name: "repetition_penalty",
                                    type: "number",
                                    schema: { pattern: "^[0-9]+(.[0-9]+)?$" },
                                    description: "Penalty for repeating tokens",
                                    required: false,
                                },
                            ]
                        },
                        description: "Optional generation configuration parameters",
                        required: false,
                    },
                    {
                        name: "remember",
                        type: "boolean",
                        schema: {},
                        description: "Whether to remember this interaction in history",
                        required: false,
                    },
                ],
                outputs: [
                    {
                        type: "[string, Record<string, any>]",
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
                                    schema: {
                                        nested: [
                                            {
                                                name: "engine",
                                                type: "string",
                                                schema: { pattern: "^(transformers|llama\\.cpp)$" },
                                                description: "Engine used for generation",
                                                required: true,
                                            },
                                        ]
                                    },
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
                description: "Load model into memory based on engine type",
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
                name: "unload",
                description: "Unload model from memory and free resources",
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
                description: "Check if model is loaded",
                arguments: [],
                outputs: [
                    {
                        type: "boolean",
                        schema: {},
                        description: "True if model is loaded, False otherwise",
                        required: true,
                    }
                ],
            },
            {
                name: "configuration",
                description: "Get a copy of the model's configuration",
                arguments: [],
                outputs: [
                    {
                        type: "Record<string, any>",
                        schema: {},
                        description: "A copy of the model's configuration",
                        required: true,
                    }
                ],
            },
            {
                name: "reset",
                description: "Reset model chat history",
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
                name: "contract",
                description: "Get a copy of the model's contract specification, which describes its capabilities, methods, and interfaces. This is useful for programmatically understanding the model's features and requirements.",
                arguments: [],
                outputs: [
                    {
                        type: "Contract",
                        schema: {},
                        description: "A copy of the model's contract specification",
                        required: true,
                    }
                ],
            },
            {
                name: "compatibility",
                description: "Get a copy of the model's compatibility specifications, detailing supported engines, quantization methods, devices, memory requirements, and dependencies. This helps determine if the model can run in a given environment.",
                arguments: [],
                outputs: [
                    {
                        type: "Compatibility[]",
                        schema: {},
                        description: "A list of the model's compatibility specifications",
                        required: true,
                    }
                ],
            },
        ],
    }
}

export function generateStandardCompatibility(): Compatibility[] {
    return [{
        engine: "openrouter",
        quantization: "none",
        devices: ["cloud"],
        memory: 0.0,
        dependencies: [],
        precision: 32
    }]
}
