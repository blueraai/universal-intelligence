import { SourcesConfig } from '../../__utils__/mixins/hf_text_to_text/types'

const sources: SourcesConfig = {
  model_info: {
    name: 'gemma2-9b-it',
    default_quantization: {
      webgpu: 'MLC_4'
    }
  },
  quantizations: {
    MLC_4_32: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'gemma-2-9b-it-q4f32_1-MLC',
      model_file: undefined,
      model_size: 7.5
    },
    MLC_4: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'gemma-2-9b-it-q4f16_1-MLC',
      model_file: undefined,
      model_size: 4.5
    }
  }
}

export default sources
