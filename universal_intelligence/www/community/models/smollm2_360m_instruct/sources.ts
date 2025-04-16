import { SourcesConfig } from '../__utils__/mixins/text_to_text/types'

const sources: SourcesConfig = {
  model_info: {
    name: 'SmolLM2-360M-Instruct',
    default_quantization: {
      webgpu: 'MLC_8_32'
    }
  },
  quantizations: {
    MLC_8_32: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'SmolLM2-360M-Instruct-q0f16-MLC',
      model_file: undefined,
      model_size: 1.3
    },
    MLC_8: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'SmolLM2-360M-Instruct-q0f16-MLC',
      model_file: undefined,
      model_size: 0.7
    },
    MLC_4_32: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'SmolLM2-360M-Instruct-q4f32_1-MLC',
      model_file: undefined,
      model_size: 0.5
    },
    MLC_4: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'SmolLM2-360M-Instruct-q4f16_1-MLC',
      model_file: undefined,
      model_size: 0.3
    }
  }
}

export default sources
