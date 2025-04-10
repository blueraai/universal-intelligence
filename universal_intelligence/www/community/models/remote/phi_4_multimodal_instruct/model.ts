import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "microsoft/phi-4-multimodal-instruct"
const _description: string = "Phi-4 Multimodal Instruct is a versatile 5.6B parameter foundation model that combines advanced reasoning and instruction-following capabilities across both text and visual inputs, providing accurate text outputs. The unified architecture enables efficient, low-latency inference, suitable for edge and mobile deployments. Phi-4 Multimodal Instruct supports text inputs in multiple languages including Arabic, Chinese, English, French, German, Japanese, Spanish, and more, with visual input optimized primarily for English. It delivers impressive performance on multimodal tasks involving mathematical, scientific, and document reasoning, providing developers and enterprises a powerful yet compact model for sophisticated interactive applications. For more information, see the [Phi-4 Multimodal blog post](https://azure.microsoft.com/en-us/blog/empowering-innovation-the-next-generation-of-the-phi-family/)."

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