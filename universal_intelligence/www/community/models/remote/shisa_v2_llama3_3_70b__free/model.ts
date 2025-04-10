import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "shisa-ai/shisa-v2-llama3.3-70b:free"
const _description: string = "Shisa V2 Llama 3.3 70B is a bilingual Japanese-English chat model fine-tuned by Shisa.AI on Meta's Llama-3.3-70B-Instruct base. It prioritizes Japanese language performance while retaining strong English capabilities. The model was optimized entirely through post-training, using a refined mix of supervised fine-tuning (SFT) and DPO datasets including regenerated ShareGPT-style data, translation tasks, roleplaying conversations, and instruction-following prompts. Unlike earlier Shisa releases, this version avoids tokenizer modifications or extended pretraining. Shisa V2 70B achieves leading Japanese task performance across a wide range of custom and public benchmarks, including JA MT Bench, ELYZA 100, and Rakuda. It supports a 128K token context length and integrates smoothly with inference frameworks like vLLM and SGLang. While it inherits safety characteristics from its base model, no additional alignment was applied. The model is intended for high-performance bilingual chat, instruction following, and translation tasks across JA/EN."

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