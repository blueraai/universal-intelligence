import { SourcesConfig } from '../__utils__/mixins/hf_text_to_text/types'

const sources: SourcesConfig = {
  model_info: {
    name: 'Qwen2.5-7B-Instruct',
    default_quantization: {
      webgpu: 'MLC_4'
    }
  },
  quantizations: {
    MLC_4_32: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Qwen2.5-7B-Instruct-q4f16_1-MLC',
      model_file: undefined,
      model_size: 11.0
    },
    MLC_4: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Qwen2.5-7B-Instruct-q4f32_1-MLC',
      model_file: undefined,
      model_size: 6.0
    },
  }
}

export default sources
