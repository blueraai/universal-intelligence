import { SourcesConfig } from '../__utils__/mixins/text_to_text/types'

const sources: SourcesConfig = {
  model_info: {
    name: 'LLama3.2-1B-Instruct',
    default_quantization: {
      webgpu: 'MLC_8_32'
    }
  },
  quantizations: {
    MLC_8_32: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Llama-3.2-1B-Instruct-q0f32-MLC',
      model_file: undefined,
      model_size: 3.0
    },
    MLC_8: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Llama-3.2-1B-Instruct-q0f16-MLC',
      model_file: undefined,
      model_size: 2.2
    },
    MLC_4_32: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Llama-3.2-1B-Instruct-q4f32_1-MLC',
      model_file: undefined,
      model_size: 1.6
    },
    MLC_4: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Llama-3.2-1B-Instruct-q4f16_1-MLC',
      model_file: undefined,
      model_size: 0.7
    }
  }
}

export default sources
