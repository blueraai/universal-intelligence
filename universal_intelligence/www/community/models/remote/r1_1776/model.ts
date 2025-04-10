import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "perplexity/r1-1776"
const _description: string = "R1 1776 is a version of DeepSeek-R1 that has been post-trained to remove censorship constraints related to topics restricted by the Chinese government. The model retains its original reasoning capabilities while providing direct responses to a wider range of queries. R1 1776 is an offline chat model that does not use the perplexity search subsystem. The model was tested on a multilingual dataset of over 1,000 examples covering sensitive topics to measure its likelihood of refusal or overly filtered responses. [Evaluation Results](https://cdn-uploads.huggingface.co/production/uploads/675c8332d01f593dc90817f5/GiN2VqC5hawUgAGJ6oHla.png) Its performance on math and reasoning benchmarks remains similar to the base R1 model. [Reasoning Performance](https://cdn-uploads.huggingface.co/production/uploads/675c8332d01f593dc90817f5/n4Z9Byqp2S7sKUvCvI40R.png) Read more on the [Blog Post](https://perplexity.ai/hub/blog/open-sourcing-r1-1776)"

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