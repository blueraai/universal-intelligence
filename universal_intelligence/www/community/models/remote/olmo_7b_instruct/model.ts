import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "allenai/olmo-7b-instruct"
const _description: string = "OLMo 7B Instruct by the Allen Institute for AI is a model finetuned for question answering. It demonstrates **notable performance** across multiple benchmarks including TruthfulQA and ToxiGen.**Open Source**: The model, its code, checkpoints, logs are released under the [Apache 2.0 license](https://choosealicense.com/licenses/apache-2.0).- [Core repo (training, inference, fine-tuning etc.)](https://github.com/allenai/OLMo)- [Evaluation code](https://github.com/allenai/OLMo-Eval)- [Further fine-tuning code](https://github.com/allenai/open-instruct)- [Paper](https://arxiv.org/abs/2402.00838)- [Technical blog post](https://blog.allenai.org/olmo-open-language-model-87ccfc95f580)- [W&B Logs](https://wandb.ai/ai2-llm/OLMo-7B/reports/OLMo-7B--Vmlldzo2NzQyMzk5)"

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