import { SourcesConfig } from '../__utils__/mixins/text_to_text/types'

const sources: SourcesConfig = {
  model_info: {
    name: 'Qwen2.5-1.5B-Instruct',
    default_quantization: {
      webgpu: 'MLC_4_32'
    }
  },
  quantizations: {
    MLC_4_32: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Qwen2.5-1.5B-Instruct-q4f32_1-MLC',
      model_file: undefined,
      model_size: 1.7
    },
    MLC_4: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Qwen2.5-1.5B-Instruct-q4f16_1-MLC',
      model_file: undefined,
      model_size: 0.8
    }
  }
}

export default sources
