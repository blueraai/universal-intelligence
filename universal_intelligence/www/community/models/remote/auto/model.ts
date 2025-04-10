import { Compatibility, Contract } from '../../../../core/types'
import { UniversalModelMixin } from '../../__utils__/mixins/openrouter_text_to_text/interface'
import { generateStandardCompatibility, generateStandardContract } from '../../__utils__/mixins/openrouter_text_to_text/meta'
import { InferenceConfiguration } from '../../__utils__/mixins/openrouter_text_to_text/types'

const _name: string = "openrouter/auto"
const _description: string = "Your prompt will be processed by a meta-model and routed to one of dozens of models (see below), optimizing for the best possible output. To see which model was used, visit [Activity](/activity), or read the `model` attribute of the response. Your response will be priced at the same rate as the routed model. The meta-model is powered by [Not Diamond](https://docs.notdiamond.ai/docs/how-not-diamond-works). Learn more in our [docs](/docs/model-routing). Requests will be routed to the following models:- [openai/gpt-4o-2024-08-06](/openai/gpt-4o-2024-08-06)- [openai/gpt-4o-2024-05-13](/openai/gpt-4o-2024-05-13)- [openai/gpt-4o-mini-2024-07-18](/openai/gpt-4o-mini-2024-07-18)- [openai/chatgpt-4o-latest](/openai/chatgpt-4o-latest)- [openai/o1-preview-2024-09-12](/openai/o1-preview-2024-09-12)- [openai/o1-mini-2024-09-12](/openai/o1-mini-2024-09-12)- [anthropic/claude-3.5-sonnet](/anthropic/claude-3.5-sonnet)- [anthropic/claude-3.5-haiku](/anthropic/claude-3.5-haiku)- [anthropic/claude-3-opus](/anthropic/claude-3-opus)- [anthropic/claude-2.1](/anthropic/claude-2.1)- [google/gemini-pro-1.5](/google/gemini-pro-1.5)- [google/gemini-flash-1.5](/google/gemini-flash-1.5)- [mistralai/mistral-large-2407](/mistralai/mistral-large-2407)- [mistralai/mistral-nemo](/mistralai/mistral-nemo)- [deepseek/deepseek-r1](/deepseek/deepseek-r1)- [meta-llama/llama-3.1-70b-instruct](/meta-llama/llama-3.1-70b-instruct)- [meta-llama/llama-3.1-405b-instruct](/meta-llama/llama-3.1-405b-instruct)- [mistralai/mixtral-8x22b-instruct](/mistralai/mixtral-8x22b-instruct)- [cohere/command-r-plus](/cohere/command-r-plus)- [cohere/command-r](/cohere/command-r)"

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