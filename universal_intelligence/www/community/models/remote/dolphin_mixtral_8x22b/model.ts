import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "cognitivecomputations/dolphin-mixtral-8x22b"
const _description: string = "Dolphin 2.9 is designed for instruction following, conversational, and coding. This model is a finetune of [Mixtral 8x22B Instruct](/models/mistralai/mixtral-8x22b-instruct). It features a 64k context length and was fine-tuned with a 16k sequence length using ChatML templates. This model is a successor to [Dolphin Mixtral 8x7B](/models/cognitivecomputations/dolphin-mixtral-8x7b). The model is uncensored and is stripped of alignment and bias. It requires an external alignment layer for ethical use. Users are cautioned to use this highly compliant model responsibly, as detailed in a blog post about uncensored models at [erichartford.com/uncensored-models](https://erichartford.com/uncensored-models).#moe #uncensored"

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