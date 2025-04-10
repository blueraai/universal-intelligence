import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "ai21/jamba-1.6-mini"
const _description: string = "AI21 Jamba Mini 1.6 is a hybrid foundation model combining State Space Models (Mamba) with Transformer attention mechanisms. With 12 billion active parameters (52 billion total), this model excels in extremely long-context tasks (up to 256K tokens) and achieves superior inference efficiency, outperforming comparable open models on tasks such as retrieval-augmented generation (RAG) and grounded question answering. Jamba Mini 1.6 supports multilingual tasks across English, Spanish, French, Portuguese, Italian, Dutch, German, Arabic, and Hebrew, along with structured JSON output and tool-use capabilities. Usage of this model is subject to the [Jamba Open Model License](https://www.ai21.com/licenses/jamba-open-model-license)."

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