import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "thedrummer/anubis-pro-105b-v1"
const _description: string = "Anubis Pro 105B v1 is an expanded and refined variant of Meta's Llama 3.3 70B, featuring 50% additional layers and further fine-tuning to leverage its increased capacity. Designed for advanced narrative, roleplay, and instructional tasks, it demonstrates enhanced emotional intelligence, creativity, nuanced character portrayal, and superior prompt adherence compared to smaller models. Its larger parameter count allows for deeper contextual understanding and extended reasoning capabilities, optimized for engaging, intelligent, and coherent interactions."

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