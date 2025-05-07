import UniversalModelMixin from "../__utils__/mixins/hf_text_to_text/interface"
import { ModelConfiguration, InferenceConfiguration, ProcessorConfiguration } from "../__utils__/mixins/hf_text_to_text/types"

import { Compatibility, Contract } from "./../../../core/types"
import { generateStandardContract, generateStandardCompatibility, generateSourcesFromConfig } from "./../__utils__/mixins/hf_text_to_text/meta"
import SOURCES from "./sources"

const _name: string = "SmolLM2-1.7B-Instruct"
const _description: string = "A powerful 1.7B parameter language model from Hugging Face, optimized for instruction following and general language tasks"
const _model_configuration: ModelConfiguration = {
    "webllm": {}
}
const _inference_configuration: InferenceConfiguration = {
  "webllm": {"max_new_tokens": 2500, "temperature": 0.1},
}
const _processor_configuration: ProcessorConfiguration = {
    "webllm": {
        "input": {},
        "output": {},
    }
}

class UniversalModel extends UniversalModelMixin {
  constructor(payload?) {
    super({
      name: _name,
      sources: generateSourcesFromConfig(SOURCES),
      model_configuration: _model_configuration,
      inference_configuration: _inference_configuration,
      processor_configuration: _processor_configuration,
    }, payload)
  }

  static contract(): Contract {
    return generateStandardContract(_name, _description)
  }

  static compatibility(): Compatibility[] {
    return generateStandardCompatibility(generateSourcesFromConfig(SOURCES))
  }

  contract(): Contract {
    return generateStandardContract(_name, _description)
  }

  compatibility(): Compatibility[] {
    return generateStandardCompatibility(generateSourcesFromConfig(SOURCES))
  }
}

export { UniversalModel }
export default UniversalModel