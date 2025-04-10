import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "arcee-ai/arcee-blitz"
const _description: string = "Arcee Blitz is a 24 B‑parameter dense model distilled from DeepSeek and built on Mistral architecture for 'everyday' chat. The distillation‑plus‑refinement pipeline trims compute while keeping DeepSeek‑style reasoning, so Blitz punches above its weight on MMLU, GSM‑8K and BBH compared with other mid‑size open models. With a default 128 k context window and competitive throughput, it serves as a cost‑efficient workhorse for summarization, brainstorming and light code help. Internally, Arcee uses Blitz as the default writer in Conductor pipelines when the heavier Virtuoso line is not required. Users therefore get near‑70 B quality at ~⅓ the latency and price. "

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