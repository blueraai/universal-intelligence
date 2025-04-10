import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "cognitivecomputations/dolphin3.0-r1-mistral-24b:free"
const _description: string = "Dolphin 3.0 R1 is the next generation of the Dolphin series of instruct-tuned models.  Designed to be the ultimate general purpose local model, enabling coding, math, agentic, function calling, and general use cases. The R1 version has been trained for 3 epochs to reason using 800k reasoning traces from the Dolphin-R1 dataset. Dolphin aims to be a general purpose reasoning instruct model, similar to the models behind ChatGPT, Claude, Gemini. Part of the [Dolphin 3.0 Collection](https://huggingface.co/collections/cognitivecomputations/dolphin-30-677ab47f73d7ff66743979a3) Curated and trained by [Eric Hartford](https://huggingface.co/ehartford), [Ben Gitter](https://huggingface.co/bigstorm), [BlouseJury](https://huggingface.co/BlouseJury) and [Cognitive Computations](https://huggingface.co/cognitivecomputations)"

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