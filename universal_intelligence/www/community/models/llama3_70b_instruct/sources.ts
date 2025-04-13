import { SourcesConfig } from '../__utils__/mixins/text_to_text/types'

const sources: SourcesConfig = {
  model_info: {
    name: 'Llama-3-70B-Instruct',
    default_quantization: {
      webgpu: 'MLC_3'
    }
  },
  quantizations: {
    MLC_3: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Llama-3-70B-Instruct-q3f16_1-MLC',
      model_file: undefined,
      model_size: 22.5
    },
  }
}

export default sources
