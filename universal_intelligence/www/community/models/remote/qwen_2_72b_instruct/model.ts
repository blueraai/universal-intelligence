import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "qwen/qwen-2-72b-instruct"
const _description: string = "Qwen2 72B is a transformer-based model that excels in language understanding, multilingual capabilities, coding, mathematics, and reasoning. It features SwiGLU activation, attention QKV bias, and group query attention. It is pretrained on extensive data with supervised finetuning and direct preference optimization. For more details, see this [blog post](https://qwenlm.github.io/blog/qwen2/) and [GitHub repo](https://github.com/QwenLM/Qwen2). Usage of this model is subject to [Tongyi Qianwen LICENSE AGREEMENT](https://huggingface.co/Qwen/Qwen1.5-110B-Chat/blob/main/LICENSE)."

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