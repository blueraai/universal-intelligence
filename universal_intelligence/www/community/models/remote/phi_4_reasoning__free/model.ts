import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "microsoft/phi-4-reasoning:free"
const _description: string = "Phi-4-reasoning is a 14B parameter dense decoder-only transformer developed by Microsoft, fine-tuned from Phi-4 to enhance complex reasoning capabilities. It uses a combination of supervised fine-tuning on chain-of-thought traces and reinforcement learning, targeting math, science, and code reasoning tasks. With a 32k context window and high inference efficiency, it is optimized for structured responses in a two-part format: reasoning trace followed by a final solution. The model achieves strong results on specialized benchmarks such as AIME, OmniMath, and LiveCodeBench, outperforming many larger models in structured reasoning tasks. It is released under the MIT license and intended for use in latency-constrained, English-only environments requiring reliable step-by-step logic. Recommended usage includes ChatML prompts and structured reasoning format for best results."

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