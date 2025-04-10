import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "undi95/toppy-m-7b"
const _description: string = "A wild 7B parameter model that merges several models using the new task_arithmetic merge method from mergekit. List of merged models:- NousResearch/Nous-Capybara-7B-V1.9- [HuggingFaceH4/zephyr-7b-beta](/models/huggingfaceh4/zephyr-7b-beta)- lemonilia/AshhLimaRP-Mistral-7B- Vulkane/120-Days-of-Sodom-LoRA-Mistral-7b- Undi95/Mistral-pippa-sharegpt-7b-qlora#merge #uncensored"

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