import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "moonshotai/moonlight-16b-a3b-instruct:free"
const _description: string = "Moonlight-16B-A3B-Instruct is a 16B-parameter Mixture-of-Experts (MoE) language model developed by Moonshot AI. It is optimized for instruction-following tasks with 3B activated parameters per inference. The model advances the Pareto frontier in performance per FLOP across English, coding, math, and Chinese benchmarks. It outperforms comparable models like Llama3-3B and Deepseek-v2-Lite while maintaining efficient deployment capabilities through Hugging Face integration and compatibility with popular inference engines like vLLM12."

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