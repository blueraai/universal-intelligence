import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "openai/o4-mini-high"
const _description: string = "OpenAI o4-mini-high is the same model as [o4-mini](/openai/o4-mini) with reasoning_effort set to high.  OpenAI o4-mini is a compact reasoning model in the o-series, optimized for fast, cost-efficient performance while retaining strong multimodal and agentic capabilities. It supports tool use and demonstrates competitive reasoning and coding performance across benchmarks like AIME (99.5% with Python) and SWE-bench, outperforming its predecessor o3-mini and even approaching o3 in some domains. Despite its smaller size, o4-mini exhibits high accuracy in STEM tasks, visual problem solving (e.g., MathVista, MMMU), and code editing. It is especially well-suited for high-throughput scenarios where latency or cost is critical. Thanks to its efficient architecture and refined reinforcement learning training, o4-mini can chain tools, generate structured outputs, and solve multi-step tasks with minimal delay—often in under a minute."

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