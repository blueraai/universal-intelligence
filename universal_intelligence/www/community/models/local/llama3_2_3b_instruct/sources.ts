import { SourcesConfig } from '../../__utils__/mixins/hf_text_to_text/types'

const sources: SourcesConfig = {
  model_info: {
    name: 'LLama3.2-3B-Instruct',
    default_quantization: {
      webgpu: 'MLC_4_32'
    }
  },
  quantizations: {
    MLC_4_32: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Llama-3.2-3B-Instruct-q4f32_1-MLC',
      model_file: undefined,
      model_size: 3.2
    },
    MLC_4: {
      engine: 'webllm',
      supported_devices: ['webgpu'],
      model_id: 'Llama-3.2-3B-Instruct-q4f16_1-MLC',
      model_file: undefined,
      model_size: 1.8
    }
  }
}

export default sources
