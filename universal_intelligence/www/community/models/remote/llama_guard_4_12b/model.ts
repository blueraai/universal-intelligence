import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "meta-llama/llama-guard-4-12b"
const _description: string = "Llama Guard 4 is a Llama 4 Scout-derived multimodal pretrained model, fine-tuned for content safety classification. Similar to previous versions, it can be used to classify content in both LLM inputs (prompt classification) and in LLM responses (response classification). It acts as an LLM—generating text in its output that indicates whether a given prompt or response is safe or unsafe, and if unsafe, it also lists the content categories violated. Llama Guard 4 was aligned to safeguard against the standardized MLCommons hazards taxonomy and designed to support multimodal Llama 4 capabilities. Specifically, it combines features from previous Llama Guard models, providing content moderation for English and multiple supported languages, along with enhanced capabilities to handle mixed text-and-image prompts, including multiple images. Additionally, Llama Guard 4 is integrated into the Llama Moderations API, extending robust safety classification to text and images."

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