import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "all-hands/openhands-lm-32b-v0.1"
const _description: string = "OpenHands LM v0.1 is a 32B open-source coding model fine-tuned from Qwen2.5-Coder-32B-Instruct using reinforcement learning techniques outlined in SWE-Gym. It is optimized for autonomous software development agents and achieves strong performance on SWE-Bench Verified, with a 37.2% resolve rate. The model supports a 128K token context window, making it well-suited for long-horizon code reasoning and large codebase tasks. OpenHands LM is designed for local deployment and runs on consumer-grade GPUs such as a single 3090. It enables fully offline agent workflows without dependency on proprietary APIs. This release is intended as a research preview, and future updates aim to improve generalizability, reduce repetition, and offer smaller variants."

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