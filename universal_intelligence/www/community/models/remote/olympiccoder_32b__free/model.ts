import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "open-r1/olympiccoder-32b:free"
const _description: string = "OlympicCoder-32B is a high-performing open-source model fine-tuned using the CodeForces-CoTs dataset, containing approximately 100,000 chain-of-thought programming samples. It excels at complex competitive programming benchmarks, such as IOI 2024 and Codeforces-style challenges, frequently surpassing state-of-the-art closed-source models. OlympicCoder-32B provides advanced reasoning, coherent multi-step problem-solving, and robust code generation capabilities, demonstrating significant potential for olympiad-level competitive programming applications."

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