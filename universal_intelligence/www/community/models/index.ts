import { UniversalModel as Gemma2_2b_Instruct } from "./gemma2_2b_instruct/model"
import { UniversalModel as Gemma2_9b_Instruct } from "./gemma2_9b_instruct/model"
import { UniversalModel as Llama3_1_8b_Instruct } from "./llama3_1_8b_instruct/model"
import { UniversalModel as Llama3_2_1b_Instruct } from "./llama3_2_1b_instruct/model"
import { UniversalModel as Llama3_2_3b_Instruct } from "./llama3_2_3b_instruct/model"
import { UniversalModel as Llama3_70b_Instruct } from "./llama3_70b_instruct/model"
import { UniversalModel as Mistral_7b_Instruct_v0d3 } from "./mistral_7b_instruct_v0d3/model"
import { UniversalModel as Qwen2_5_0d5b_Instruct } from "./qwen2_5_0d5b_instruct/model"
import { UniversalModel as Qwen2_5_1d5b_Instruct } from "./qwen2_5_1d5b_instruct/model"
import { UniversalModel as Qwen2_5_3b_Instruct } from "./qwen2_5_3b_instruct/model"
import { UniversalModel as Qwen2_5_7b_Instruct } from "./qwen2_5_7b_instruct/model"
import { UniversalModel as SmolLM2_1_7b_Instruct } from "./smollm2_1d7b_instruct/model"
import { UniversalModel as SmolLM2_360m_Instruct } from "./smollm2_360m_instruct/model"

const models = {
  Qwen2_5_7b_Instruct,
  Qwen2_5_3b_Instruct,
  Qwen2_5_1d5b_Instruct,
  Qwen2_5_0d5b_Instruct,
  Llama3_70b_Instruct,
  Llama3_1_8b_Instruct,
  Llama3_2_3b_Instruct,
  Llama3_2_1b_Instruct,
  Mistral_7b_Instruct_v0d3,
  Gemma2_9b_Instruct,
  Gemma2_2b_Instruct,
  SmolLM2_1_7b_Instruct,
  SmolLM2_360m_Instruct,
  Model: Qwen2_5_3b_Instruct, // default model
}

export default models