import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "nvidia/llama-3.3-nemotron-super-49b-v1:free"
const _description: string = "Llama-3.3-Nemotron-Super-49B-v1 is a large language model (LLM) optimized for advanced reasoning, conversational interactions, retrieval-augmented generation (RAG), and tool-calling tasks. Derived from Meta's Llama-3.3-70B-Instruct, it employs a Neural Architecture Search (NAS) approach, significantly enhancing efficiency and reducing memory requirements. This allows the model to support a context length of up to 128K tokens and fit efficiently on single high-performance GPUs, such as NVIDIA H200. Note: you must include `detailed thinking on` in the system prompt to enable reasoning. Please see [Usage Recommendations](https://huggingface.co/nvidia/Llama-3_1-Nemotron-Ultra-253B-v1#quick-start-and-usage-recommendations) for more."

const _inferenceConfiguration: InferenceConfiguration = {
    openrouter: { maxNewTokens: 2500, temperature: 0.1 }
}

class UniversalModel extends UniversalModelMixin {
    constructor(payload?) {
      super({
        name: _name,
        inference_configuration: _inferenceConfiguration,
      }, payload)
    }

    static contract(): Contract {
        return generateStandardContract(_name, _description)
    }

    static compatibility(): Compatibility[] {
        return generateStandardCompatibility()
    }

    contract(): Contract {
      return generateStandardContract(_name, _description)
    }
  
    compatibility(): Compatibility[] {
      return generateStandardCompatibility()
    }
} 

export { UniversalModel }
export default UniversalModel