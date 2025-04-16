import { SourcesConfig } from '../__utils__/mixins/text_to_text/types'

const sources: SourcesConfig = {
  model_info: {
    name: 'gemma2-2b-it',
    default_quantization: {
      webgpu: 'MLC_4_32'
    }
  },
  quantizations: {
    MLC_4_32: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'gemma-2-2b-it-q4f32_1-MLC',
      model_file: undefined,
      model_size: 3.0
    },
    MLC_4: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'gemma-2-2b-it-q4f16_1-MLC',
      model_file: undefined,
      model_size: 1.6
    }
  }
}

export default sources
