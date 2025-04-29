import { SourcesConfig } from '../__utils__/mixins/hf_text_to_text/types'

const sources: SourcesConfig = {
  model_info: {
    name: 'LLama3.1-8B-Instruct',
    default_quantization: {
      webgpu: 'MLC_4'
    }
  },
  quantizations: {
    MLC_4_32: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Llama-3.1-8B-Instruct-q432_1-MLC',
      model_file: undefined,
      model_size: 8.0
    },
    MLC_4: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Llama-3.1-8B-Instruct-q4f16_1-MLC',
      model_file: undefined,
      model_size: 4.5
    }
  }
}

export default sources
