import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "mistral/ministral-8b"
const _description: string = "Ministral 8B is a state-of-the-art language model optimized for on-device and edge computing. Designed for efficiency in knowledge-intensive tasks, commonsense reasoning, and function-calling, it features a specialized interleaved sliding-window attention mechanism, enabling faster and more memory-efficient inference. Ministral 8B excels in local, low-latency applications such as offline translation, smart assistants, autonomous robotics, and local analytics. The model supports up to 128k context length and can function as a performant intermediary in multi-step agentic workflows, efficiently handling tasks like input parsing, API calls, and task routing. It consistently outperforms comparable models like Mistral 7B across benchmarks, making it particularly suitable for compute-efficient, privacy-focused scenarios."

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