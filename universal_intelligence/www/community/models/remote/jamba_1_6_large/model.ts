import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "ai21/jamba-1.6-large"
const _description: string = "AI21 Jamba Large 1.6 is a high-performance hybrid foundation model combining State Space Models (Mamba) with Transformer attention mechanisms. Developed by AI21, it excels in extremely long-context handling (256K tokens), demonstrates superior inference efficiency (up to 2.5x faster than comparable models), and supports structured JSON output and tool-use capabilities. It has 94 billion active parameters (398 billion total), optimized quantization support (ExpertsInt8), and multilingual proficiency in languages such as English, Spanish, French, Portuguese, Italian, Dutch, German, Arabic, and Hebrew. Usage of this model is subject to the [Jamba Open Model License](https://www.ai21.com/licenses/jamba-open-model-license)."

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