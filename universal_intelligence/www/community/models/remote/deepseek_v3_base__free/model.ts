import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "deepseek/deepseek-v3-base:free"
const _description: string = "Note that this is a base model mostly meant for testing, you need to provide detailed prompts for the model to return useful responses.  DeepSeek-V3 Base is a 671B parameter open Mixture-of-Experts (MoE) language model with 37B active parameters per forward pass and a context length of 128K tokens. Trained on 14.8T tokens using FP8 mixed precision, it achieves high training efficiency and stability, with strong performance across language, reasoning, math, and coding tasks.  DeepSeek-V3 Base is the pre-trained model behind [DeepSeek V3](/deepseek/deepseek-chat-v3)"

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