import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "scb10x/llama3.1-typhoon2-8b-instruct"
const _description: string = "Llama3.1-Typhoon2-8B-Instruct is a Thai-English instruction-tuned model with 8 billion parameters, built on Llama 3.1. It significantly improves over its base model in Thai reasoning, instruction-following, and function-calling tasks, while maintaining competitive English performance. The model is optimized for bilingual interaction and performs well on Thai-English code-switching, MT-Bench, IFEval, and tool-use benchmarks. Despite its smaller size, it demonstrates strong generalization across math, coding, and multilingual benchmarks, outperforming comparable 8B models across most Thai-specific tasks. Full benchmark results and methodology are available in the [technical report.](https://arxiv.org/abs/2412.13702)"

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