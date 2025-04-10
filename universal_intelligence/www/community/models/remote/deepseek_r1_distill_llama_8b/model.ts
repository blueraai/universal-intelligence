import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "deepseek/deepseek-r1-distill-llama-8b"
const _description: string = "DeepSeek R1 Distill Llama 8B is a distilled large language model based on [Llama-3.1-8B-Instruct](/meta-llama/llama-3.1-8b-instruct), using outputs from [DeepSeek R1](/deepseek/deepseek-r1). The model combines advanced distillation techniques to achieve high performance across multiple benchmarks, including:- AIME 2024 pass@1: 50.4- MATH-500 pass@1: 89.1- CodeForces Rating: 1205 The model leverages fine-tuning from DeepSeek R1's outputs, enabling competitive performance comparable to larger frontier models. Hugging Face: - [Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) - [DeepSeek-R1-Distill-Llama-8B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B)   |"

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