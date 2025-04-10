import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "perplexity/sonar-reasoning-pro"
const _description: string = "Note: Sonar Pro pricing includes Perplexity search pricing. See [details here](https://docs.perplexity.ai/guides/pricing#detailed-pricing-breakdown-for-sonar-reasoning-pro-and-sonar-pro) Sonar Reasoning Pro is a premier reasoning model powered by DeepSeek R1 with Chain of Thought (CoT). Designed for advanced use cases, it supports in-depth, multi-step queries with a larger context window and can surface more citations per search, enabling more comprehensive and extensible responses."

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