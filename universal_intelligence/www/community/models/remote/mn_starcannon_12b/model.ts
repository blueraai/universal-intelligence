import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "aetherwiing/mn-starcannon-12b"
const _description: string = "Starcannon 12B v2 is a creative roleplay and story writing model, based on Mistral Nemo, using [nothingiisreal/mn-celeste-12b](/nothingiisreal/mn-celeste-12b) as a base, with [intervitens/mini-magnum-12b-v1.1](https://huggingface.co/intervitens/mini-magnum-12b-v1.1) merged in using the [TIES](https://arxiv.org/abs/2306.01708) method. Although more similar to Magnum overall, the model remains very creative, with a pleasant writing style. It is recommended for people wanting more variety than Magnum, and yet more verbose prose than Celeste."

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