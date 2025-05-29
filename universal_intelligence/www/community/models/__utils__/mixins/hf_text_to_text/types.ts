// Engine configuration types
export interface EngineConfig {
    name: string;
    model_id: string;
    model_file?: string | null;
    is_default: boolean;
}

export interface QuantizationConfig {
    available_engines: EngineConfig[];
    is_default: boolean;
    memory: number;
    precision: number;
}

export type Sources = {
  webgpu: Record<string, QuantizationConfig>
};

export type ModelConfiguration = {
    [key: string]: {
        [key: string]: any;
    };
};

export type InferenceConfiguration = {
    [key: string]: {
        [key: string]: any;
    };
};

export interface InputProcessorConfig {
    tokenizer?: {
        [key: string]: any;
    };
    chat_template?: {
        [key: string]: any;
    };
}

export interface ProcessorConfig {
    input?: InputProcessorConfig;
    output?: {
        [key: string]: any;
    };
}

export type ProcessorConfiguration = {
    [K in 'webllm']: ProcessorConfig;
};

export interface ChatTemplate {
    system_start: string;
    system_end: string;
    user_start: string;
    user_end: string;
    assistant_start: string;
    assistant_end: string;
    default_system_message: string;
    generation_prompt: string;
}

export type PrecisionType = '2bit' | '3bit' | '4bit' | '5bit' | '6bit' | '8bit' | '16bit' | '32bit';

export interface ModelInfo {
  name: string;
  default_quantization: {
    webgpu?: string;
  };
}

export interface QuantizationInfo {
  engine: string;
  model_id: string;
  model_file?: string;
  model_size: number;
  supported_devices: string[];
}

export interface SourcesConfig{
  model_info: ModelInfo;
  quantizations: Record<string, QuantizationInfo>;
}

// WebGPU type declarations

declare global {
  interface Navigator {
    gpu?: {
      requestAdapter: (options?: { powerPreference?: 'high-performance' }) => GPUAdapter | null;
    };
  }
}

interface GPUAdapter {
  limits: {
    maxBufferSize: number;
    maxStorageBufferBindingSize: number;
  };
}