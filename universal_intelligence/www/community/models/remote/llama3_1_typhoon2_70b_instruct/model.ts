import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "scb10x/llama3.1-typhoon2-70b-instruct"
const _description: string = "Llama3.1-Typhoon2-70B-Instruct is a Thai-English instruction-tuned language model with 70 billion parameters, built on Llama 3.1. It demonstrates strong performance across general instruction-following, math, coding, and tool-use tasks, with state-of-the-art results in Thai-specific benchmarks such as IFEval, MT-Bench, and Thai-English code-switching. The model excels in bilingual reasoning and function-calling scenarios, offering high accuracy across diverse domains. Comparative evaluations show consistent improvements over prior Thai LLMs and other Llama-based baselines. Full results and methodology are available in the [technical report.](https://arxiv.org/abs/2412.13702)"

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