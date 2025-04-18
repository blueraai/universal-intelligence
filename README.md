![Universal Intelligence](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//universal-intelligence-banner-rsm.png)

<p align="center">
    <a href="https://github.com/blueraai/universal-intelligence/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/blueraai/universal-intelligence.svg?color=blue"></a>
    <a href="https://github.com/blueraai/universal-intelligence/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/blueraai/universal-intelligence.svg"></a>
</p>

> ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-python-16.png) This page aims to document **Python** protocols and usage (e.g. cloud, desktop).
>
> Looking for [**Javascript/Typescript instructions**](https://github.com/blueraai/universal-intelligence/blob/main/README_WEB.md)?

## Overview

`Universal Intelligence` standardizes, simplifies and modularizes the distribution and usage of artifical intelligence.

It provides three specifications: `Universal Model`, `Universal Tool`, and `Universal Agent`.

This project also provides ready-to-use **community-built components**, implementing the `Universal Intelligence` specification.

![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-python-16.png) ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-javascript-16.png) `Universal Intelligence` protocols and components can be used across **all platforms** (cloud, desktop, web, mobile).

> 🧩 AI Components as Building Blocks.
>
> [Bluera Inc.](https://bluera.ai)

## Get Started

Get familiar with the composable building blocks, using the default **community components**.

```sh
# Choose relevant install for your device
pip install "universal-intelligence[community,mps]" # Apple
pip install "universal-intelligence[community,cuda]" # NVIDIA

# Log into Hugging Face CLI so you can download models
huggingface-cli login
```

#### 🧠 Simple model

```python
from universal_intelligence import Model

model = Model()
result, logs = model.process("Hello, how are you?")
```

#### 🔧 Simple tool

```python
from universal_intelligence import Tool

tool = Tool()
result, logs = tool.print_text("This needs to be printed")
```

#### 🤖 Simple agent (🧠 + 🔧)

```python
from universal_intelligence import Model, Tool, Agent, OtherAgent

agent = Agent(
  # model=Model(),                  # customize or share 🧠 across [🤖,🤖,🤖,..]
  # expand_tools=[Tool()],          # expand 🔧 set
  # expand_team=[OtherAgent()]      # expand 🤖 team
)
result, logs = agent.process("Please print 'Hello World' to the console", extra_tools=[Tool()])
```

### Playground

A ready-made playground is available to help familiarize yourself with the protocols and components.

```sh
python -m playground.example 
```


## Specification

### Universal Model

A `⚪ Universal Model` is a standardized, self-contained and configurable interface able to run a given model, irrespective of the consumer hardware and without requiring domain expertise.

It embeddeds a model (i.e. hosted, fetched, or local), one or more engines (e.g. [transformers](https://huggingface.co/docs/transformers/index), [lama.cpp](https://llama-cpp-python.readthedocs.io/en/latest/api-reference/), [mlx-lm](https://github.com/ml-explore/mlx-lm), [web-llm](https://webllm.mlc.ai)), runtime dependencies for each device type (e.g. CUDA, MPS), and exposes a standard interface.

While configurable, every aspect is preset for the user, based on *automatic device detection and dynamic model precision*, in order to abstract complexity and provide a simplified and portable interface.

> *Providers*: In the intent of preseting a `Universal Model` for non-technical mass adoption, we recommend defaulting to 4 bit quantization.

### Universal Tool

A `⚪ Universal Tool` is a standardized tool interface, usable by any `Universal Agent`.

Tools allow interacting with other systems (e.g. API, database) or performing scripted tasks.

> When `Universal Tools` require accessing remote services, we recommend standardizing those remote interfaces as well using [MCP Servers](https://modelcontextprotocol.io/introduction), for greater portability. Many MCP servers have already been shared with the community and are ready to use, see [available MCP servers](https://github.com/modelcontextprotocol/servers) for details.

### Universal Agent

A `⚪ Universal Agent` is a standardized, configurable and ***composable*** agent, powered by a `Universal Model`, `Universal Tools` and other `Universal Agents`.

While configurable, every aspect is preset for the user, in order to abstract complexity and provide a simplified and portable interface.

Through standardization, `Universal Agent` can seemlessly and dynamically integrate with other `Universal Intelligence` components to achieve any task, and/or share hardware recources (i.e. sharing a common `Universal Model`) —allowing it to ***generalize and scale at virtually no cost***.

> When `Universal Agents` require accessing remote agents, we recommend leveraging Google's [A2A Protocols](https://github.com/google/A2A/tree/main), for greater compatibility.

In simple terms:

> Universal Model = 🧠
>
> Universal Tool = 🔧
>
> Universal Agent = 🤖
>
> 🤖 = 🧠 + [🔧, 🔧,..] + [🤖, 🤖,..]

### Usage

#### Universal Model

```python
from <provider> import UniversalModel as Model

model = Model()
output, logs = model.process('How are you today?') # 'Feeling great! How about you?'
```

> Automatically optimized for any supported device 🔥

##### Customization Options

Simple does not mean limited. Most advanted `configuration` options remain available.

Those are defined by and specific to the *universal model provider*.

> We encourage providers to use industry standard [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) specifications, irrespective of the backend internally used for the detected device and translated accordingly, allowing for greater portability and adoption.

###### Optional Parameters

```python
from <provider> import UniversalModel as Model

model = Model(
  engine='transformers', # (or) ordered by priority ['transformers', 'llama.cpp']
  quantization='BNB_4', # (or) ordered by priority ['Q4_K_M', 'Q8_0'] (or) auto in range {'default': 'Q4_K_M', 'min_precision': '4bit', 'max_precision': '8bit'}
  max_memory_allocation=0.8, # maximum allowed memory allocation in percentage
  configuration={
    # (example)
    # "processor": {
    #     e.g. Tokenizer https://huggingface.co/docs/transformers/fast_tokenizers
    #     
    #     model_max_length: 4096,
    #     model_input_names: ['token_type_ids', 'attention_mask']
    #     ...
    # },
    # "model": {
    #     e.g. AutoModel https://huggingface.co/docs/transformers/models
    #    
    #     torch_dtype: "auto"
    #     device_map: "auto"
    #     ...
    # }
  }
)


output, logs = model.process(
  input=[
    {
      "role": "system",
      "content": "You are a helpful model to recall schedules."
    },
    {
      "role": "user",
      "content": "What did I do in May?"
    },
  ], # multimodal
  context=["May: Went to the Cinema", "June: Listened to Music"],  # multimodal
  configuration={
    # (example)
    # e.g. AutoModel Generate https://huggingface.co/docs/transformers/llm_tutorial
    # 
    # max_new_tokens: 2000, 
    # use_cache: True,
    # temperature: 1.0
    # ...
  },
  remember=True, # remember this interaction
  stream=False, # stream output asynchronously
  keep_alive=True # keep model loaded after processing the request
) # 'In May, you went to the Cinema.'
```

###### Optional Methods

```python
from <provider> import UniversalModel as Model
model = Model()

# Optional 
model.load() # loads the model in memory (otherwise automatically loaded/unloaded on execution of `.process()`)
model.loaded() # checks if model is loaded
model.unload() # unloads the model from memory (otherwise automatically loaded/unloaded on execution of `.process()`)
model.reset() # resets remembered chat history
model.configuration() # gets current model configuration

# Class Optional
Model.contract()  # Contract 
Model.compatibility()  # Compatibility 
```

#### Universal Tool 

```python
from <provider> import UniversalTool as Tool

tool = Tool(configuration={ "any": "configuration" })
result, logs = tool.example_task(example_argument='hello') # "hello"
```

###### Optional Methods

```python
from <provider> import UniversalTool as Tool

# Class Optional
Tool.contract()  # Contract 
Tool.requirements()  # Configuration Requirements 
```

#### Universal Agent 

```python
from <provider> import UniversalAgent as Agent

agent = Agent(
  # (optionally composable)
  #
  # model=Model(),
  # expand_tools=[Tool()],
  # expand_team=[OtherAgent()]
)
output, logs = agent.process('What happened on Friday?') # > (tool call) > 'Friday was your birthday!'
```

> Modular, and automatically optimized for any supported device 🔥

##### Customization Options

Most advanted `configuration` options remain available.

Those are defined by and specific to the *universal model provider*.

> We encourage providers to use industry standard [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) specifications, irrespective of the backend internally used for the detected device and translated accordingly, allowing for greater portability and adoption.

###### Optional Parameters

```python
from <provider.agent> import UniversalAgent as Agent
from <provider.other_agent> import UniversalAgent as OtherAgent
from <provider.model> import UniversalModel as Model
from <provider.tool> import UniversalTool as Tool # e.g. API, database

# This is where the magic happens ✨
# Standardization of all layers make agents composable and generalized.
# They can now utilize any 3rd party tools or agents on the fly to achieve any tasks.
# Additionally, the models powering each agent can now be hot-swapped so that 
# a team of agents shares the same intelligence(s), thus removing hardware overhead, 
# and scaling at virtually no cost.
agent = Agent(
  model=Model(), # see Universal Model API for customizations
  expand_tools=[Tool()], # see Universal Tool API for customizations
  expand_team=[OtherAgent()]  # see Universal Agent API for customizations
)

output, logs = agent.process(
  input=[
    {
      "role": "system",
      "content": "You are a helpful model to recall schedules and set events."
    },
    {
      "role": "user",
      "content": "Can you schedule what we did in May again for the next month?"
    },
  ], # multimodal
  context=['May: Went to the Cinema', 'June: Listened to Music'],  # multimodal
  configuration={
    # (example)
    # e.g. AutoModel Generate https://huggingface.co/docs/transformers/llm_tutorial
    # 
    # max_new_tokens: 2000, 
    # use_cache: True,
    # temperature: 1.0
    # ...
  },
  remember=True, # remember this interaction
  stream=False, # stream output asynchronously
  extra_tools=[Tool()], # extra tools available for this inference; call `agent.connect()` link during initiation to persist them
  extra_team=[OtherAgent()],  # extra agents available for this inference; call `agent.connect()` link during initiation to persist them
  keep_alive=True # keep model loaded after processing the request
) 
# > "In May, you went to the Cinema. Let me check the location for you." 
# > (tool call: database) 
# > "It was in Hollywood. Let me schedule a reminder for next month."
# > (agent call: scheduler)
# > "Alright you are all set! Hollywood cinema is now scheduled again in July."
```

###### Optional Methods

```python
from <provider.agent> import UniversalAgent as Agent
from <provider.other_agent> import UniversalAgent as OtherAgent
from <provider.model> import UniversalModel as Model
from <provider.tool> import UniversalTool as Tool # e.g. API, database
agent = Agent()
other_agent = OtherAgent()
tool = Tool()

# Optional 
agent.load() # loads the agent's model in memory (otherwise automatically loaded/unloaded on execution of `.process()`)
agent.loaded() # checks if agent is loaded
agent.unload() # unloads the agent's model from memory (otherwise automatically loaded/unloaded on execution of `.process()`)
agent.reset() # resets remembered chat history
agent.connect(universal_tools=[tool], universal_agents=[other_agent]) # connects additionnal tools/agents
agent.disconnect(universal_tools=[tool], universal_agents=[other_agent]) # disconnects tools/agents

# Class Optional
Agent.contract()  # Contract 
Agent.requirements()  # Configuration Requirements 
Agent.compatibility()  # Compatibility 
```

### API

#### Universal Model

A self-contained environment for running AI models with standardized interfaces.

| Method | Parameters | Return Type | Description |
|--------|------------|-------------|-------------|
| `__init__` | • `engine: str \| List[str] = None`: Engine used (e.g., 'transformers', 'llama.cpp', (or) ordered by priority *['transformers', 'llama.cpp']*). Prefer setting quantizations over engines for broader portability.<br>• `quantization: str \| List[str] \| QuantizationSettings = None`: Quantization specification (e.g., *'Q4_K_M'*, (or) ordered by priority *['Q4_K_M', 'Q8_0']* (or) auto in range *{'default': 'Q4_K_M', 'min_precision': '4bit', 'max_precision': '8bit'}*)<br>• `max_memory_allocation: float = None`: Maximum allowed memory allocation in percentage<br>• `configuration: Dict = None`: Configuration for model and processor settings | `None` | Initialize a Universal Model |
| `process` | • `input: Any \| List[Message]`: Input or input messages<br>• `context: List[Any] = None`: Context items (multimodal supported)<br>• `configuration: Dict = None`: Runtime configuration<br>• `remember: bool = False`: Whether to remember this interaction. Please be mindful of the available context length of the underlaying model.<br>• `stream: bool = False`: Stream output asynchronously<br>• `keep_alive: bool = None`: Keep model loaded for faster consecutive interactions | `Tuple[Any, Dict]` | Process input through the model and return output and logs. The output is typically the model's response and the logs contain processing metadata |
| `load` | None | `None` | Load model into memory |
| `loaded` | None | `bool` | Check if model is currently loaded in memory |
| `unload` | None | `None` | Unload model from memory |
| `reset` | None | `None` | Reset model chat history |
| `configuration` | None | `Dict` | Get current model configuration |
| `(class).contract` | None | `Contract` | Model description and interface specification |
| `(class).compatibility` | None | `List[Compatibility]` | Model compatibility specification |

#### Universal Tool

A standardized interface for tools that can be used by models and agents.

| Method | Parameters | Return Type | Description |
|--------|------------|-------------|-------------|
| `__init__` | • `configuration: Dict = None`: Tool configuration including credentials | `None` | Initialize a Universal Tool |
| `(class).contract` | None | `Contract` | Tool description and interface specification |
| `(class).requirements` | None | `List[Requirement]` | Tool configuration requirements |

Additional methods are defined by the specific tool implementation and documented in the tool's contract.

Any tool specific method _must return_ a `tuple[Any, dict]`, respectively `(result, logs)`.

#### Universal Agent

An AI agent powered by Universal Models and Tools with standardized interfaces.

| Method | Parameters | Return Type | Description |
|--------|------------|-------------|-------------|
| `__init__` | • `model: UniversalModel = None`: Model powering this agent<br>• `expand_tools: List[UniversalTool] = None`: Tools to connect<br>• `expand_team: List[UniversalAgent] = None`: Other agents to connect | `None` | Initialize a Universal Agent |
| `process` | • `input: Any \| List[Message]`: Input or input messages<br>• `context: List[Any] = None`: Context items (multimodal)<br>• `configuration: Dict = None`: Runtime configuration<br>• `remember: bool = False`: Remember this interaction. Please be mindful of the available context length of the underlaying model.<br>• `stream: bool = False`: Stream output asynchronously<br>• `extra_tools: List[UniversalTool] = None`: Additional tools<br>• `extra_team: List[UniversalAgent] = None`: Additional agents<br>• `keep_alive: bool = None`: Keep underlaying model loaded for faster consecutive interactions | `Tuple[Any, Dict]` | Process input through the agent and return output and logs. The output is typically the agent's response and the logs contain processing metadata including tool/agent calls |
| `load` | None | `None` | Load agent's model into memory |
| `loaded` | None | `bool` | Check if the agent's model is currently loaded in memory |
| `unload` | None | `None` | Unload agent's model from memory |
| `reset` | None | `None` | Reset agent's chat history |
| `connect` | • `universal_tools: List[UniversalTool] = None`: Tools to connect<br>• `universal_agents: List[UniversalAgent] = None`: Agents to connect | `None` | Connect additional tools and agents |
| `disconnect` | • `universal_tools: List[UniversalTool] = None`: Tools to disconnect<br>• `universal_agents: List[UniversalAgent] = None`: Agents to disconnect | `None` | Disconnect tools and agents |
| `(class).contract` | None | `Contract` | Agent description and interface specification |
| `(class).requirements` | None | `List[Requirement]` | Agent configuration requirements |
| `(class).compatibility` | None | `List[Compatibility]` | Agent compatibility specification |

#### Data Structures

##### Message

| Field | Type | Description |
|-------|------|-------------|
| `role` | `str` | The role of the message sender (e.g., "system", "user") |
| `content` | `Any` | The content of the message (multimodal supported) |

##### Schema

| Field | Type | Description |
|-------|------|-------------|
| `maxLength` | `Optional[int]` | Maximum length constraint |
| `minLength` | `Optional[int]` | Maximum length constraint |
| `pattern` | `Optional[str]` | Pattern constraint |
| `nested` | `Optional[List[Argument]]` | Nested argument definitions for complex types |
| `properties` | `Optional[Dict[str, Schema]]` | Property definitions for object types |
| `items` | `Optional[Schema]` | Schema for array items |

> Expandable as needed

##### Argument

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Name of the argument |
| `type` | `str` | Type of the argument |
| `schema` | `Optional[Schema]` | Schema constraints |
| `description` | `str` | Description of the argument |
| `required` | `bool` | Whether the argument is required |

##### Output

| Field | Type | Description |
|-------|------|-------------|
| `type` | `str` | Type of the output |
| `description` | `str` | Description of the output |
| `required` | `bool` | Whether the output is required |

##### Method

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Name of the method |
| `description` | `str` | Description of the method |
| `arguments` | `List[Argument]` | List of method arguments |
| `outputs` | `List[Output]` | List of method outputs |
| `asynchronous` | `Optional[bool]` | Whether the method is asynchronous (default: False) |

##### Contract

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Name of the contract |
| `description` | `str` | Description of the contract |
| `methods` | `List[Method]` | List of available methods |

> When describing a Universal Model, we encourage providers to document core information such as parameter counts and context sizes.

##### Requirement

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Name of the requirement |
| `type` | `str` | Type of the requirement |
| `schema` | `Schema` | Schema constraints |
| `description` | `str` | Description of the requirement |
| `required` | `bool` | Whether the requirement is required |

##### Compatibility

| Field | Type | Description |
|-------|------|-------------|
| `engine` | `str` | Supported engine |
| `quantization` | `str` | Supported quantization |
| `devices` | `List[str]` | List of supported devices |
| `memory` | `float` | Required memory in GB |
| `dependencies` | `List[str]` | Required software dependencies |
| `precision` | `int` | Precision in bits |

##### QuantizationSettings

| Field | Type | Description |
|-------|------|-------------|
| `default` | `Optional[str]` | Default quantization to use (e.g., 'Q4_K_M'), otherwise using defaults set in `sources.yaml` |
| `min_precision` | `Optional[str]` | Minimum precision requirement (e.g., '4bit'). Default: Lowest between 4 bit and the default's precision if explicitly provided. |
| `max_precision` | `Optional[str]` | Maximum precision requirement (e.g., '8bit'). Default: 8 bit or the default's precision if explicitly provided.  |

> Expandable as needed

### Development

Abstract classes and types for `Universal Intelligence` components are made available by the package if you wish to develop and publish your own.

```sh
# Install abstracts
pip install universal-intelligence
```

```python
from universal_intelligence.core import AbstractUniversalModel, AbstractUniversalTool, AbstractUniversalAgent, types

class UniversalModel(AbstractUniversalModel):
  # ...
  pass

class UniversalTool(AbstractUniversalTool):
  # ...
  pass

class UniversalAgent(AbstractUniversalAgent):
  # ...
  pass
```

If you wish to contribute to community based components, [mixins](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/__utils__/mixins) are made available to allow quickly bootstrapping new `Universal Models`.

> See *Community>Development* section below for additional information.

## Community Components

The `universal-intelligence` package provides several community-built models, agents, and tools that you can use out of the box.

### Installation

```sh
# Install with device optimizations
pip install "universal-intelligence[community,mps]" # Apple
pip install "universal-intelligence[community,cuda]" # NVIDIA
```

Some components may require additional dependencies. These can be installed on demand.

```sh
# Install MCP specific dependencies
pip install "universal-intelligence[community,mps,mcp]" # Apple
pip install "universal-intelligence[community,cuda,mcp]" # NVIDIA
```

> Some of the community components interface with gated models, in which case you may have to accept the model's terms on [Hugging Face](https://huggingface.co/docs/hub/en/models-gated) and log into that approved account. 
> 
> You may do so in your terminal using `huggingface-cli login`
> 
> or in your code: 
> ```python
> from huggingface_hub import login
> login()
> ```

### Playground

You can get familiar with the library using our ready-made playground

```sh
python -m playground.example 
```

### Usage

```python
from universal_intelligence.community.models.default import UniversalModel as Model

model = Model()
output, logs = model.process("How are you doing today?")

# or configure as needed

# model = Model(
#   engine='transformers', 
#   quantization={
#     'default': 'BNB_4', 
#     'min_precision': '4bit', # any of 2bit, 3bit, 4bit (default), 5bit, 6bit, 8bit, 16bit, 32bit
#     'max_precision': '16bit', # any of 2bit, 3bit, 4bit, 5bit, 6bit, 8bit (default), 16bit, 32bit
#     'max_memory_allocation': 0.8  # percentage 0 to 1 (default 80%)
#   }, # or 'BNB_4' # or ['BNB_4', 'AWQ_4']
#   max_memory_allocation=0.8,
#   configuration={
#     "processor": {
#       "input": {
#         "tokenizer": {
#           "trust_remote_code": True,
#           "padding": True,
#           "truncation": True,
#           "return_attention_mask": True
#         },
#         "chat_template": {
#           "add_generation_prompt": True
#         }
#       },
#       "output": {
#         "skip_special_tokens": True,
#         "clean_up_tokenization_spaces": True
#       }
#     },
#     "model": {
#       "device_map": "auto",
#       "torch_dtype": "auto"
#     }
#   }
# )


# output, logs = model.process(
#   input=[
#     {
#       "role": "system",
#       "content": "You are a helpful model to recall schedules."
#     },
#     {
#       "role": "user",
#       "content": "What did I do in May?"
#     },
#   ],
#   context=["May: Went to the Cinema", "June: Listened to Music"],
#   configuration={
#     "max_new_tokens": 2500,
#     "temperature": 0.1,
#     "top_p": 0.9,
#     "top_k": 30
#   },
#   remember=True,
#   keep_alive=True
# ) # 'In May, you went to the Cinema.'
```

#### Supported Components

##### Models

| I/O | Name | Import Path | Description | Supported Configurations |
|------|------|------|-------------|-----------|
| Text/Text | `Qwen2.5-7B-Instruct` (default)| `universal_intelligence.community.models.default`<br> or `universal_intelligence.community.models.qwen2_5_7b_instruct` | Small powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_7b_instruct/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `Qwen2.5-32B-Instruct` | `universal_intelligence.community.models.qwen2_5_32b_instruct` | Large powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_32b_instruct/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `Qwen2.5-14B-Instruct` | `universal_intelligence.community.models.qwen2_5_14b_instruct` | Medium powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_14b_instruct/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `Qwen2.5-14B-Instruct-1M` | `universal_intelligence.community.models.qwen2_5_14b_instruct_1m` | Medium powerful model with 1M context by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_14b_instruct_1m/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `Qwen2.5-7B-Instruct-1M` | `universal_intelligence.community.models.qwen2_5_7b_instruct_1m` | Small powerful model with 1M context by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_7b_instruct_1m/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `Qwen2.5-3B-Instruct` | `universal_intelligence.community.models.qwen2_5_3b_instruct` | Compact powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_3b_instruct/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `Qwen2.5-1.5B-Instruct` | `universal_intelligence.community.models.qwen2_5_1d5b_instruct` | Ultra-compact powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_1d5b_instruct/sources.yaml)<br><br>Default:<br>`cuda:bfloat16:transformers`<br>`mps:MLX_8:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `gemma-3-27b-it` | `universal_intelligence.community.models.gemma3_27b_it` | Large powerful model by Google |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/gemma3_27b_it/sources.yaml)<br><br>Default:<br>`cuda:Q4_K_M:llama.cpp`<br>`mps:Q4_K_M:llama.cpp`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `gemma-3-12b-it` | `universal_intelligence.community.models.gemma3_12b_it` | Medium powerful model by Google |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/gemma3_12b_it/sources.yaml)<br><br>Default:<br>`cuda:Q4_K_M:llama.cpp`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `gemma-3-4b-it` | `universal_intelligence.community.models.gemma3_4b_it` | Small powerful model by Google |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/gemma3_4b_it/sources.yaml)<br><br>Default:<br>`cuda:Q4_K_M:llama.cpp`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `gemma-3-1b-it` | `universal_intelligence.community.models.gemma3_1b_it` | Ultra-compact powerful model by Google |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/gemma3_1b_it/sources.yaml)<br><br>Default:<br>`cuda:bfloat16:transformers`<br>`mps:bfloat16:transformers`<br>`cpu:bfloat16:transformers` |
| Text/Text | `falcon-3-10b-instruct` | `universal_intelligence.community.models.falcon3_10b_instruct` | Medium powerful model by TII |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/falcon3_10b_instruct/sources.yaml)<br><br>Default:<br>`cuda:AWQ_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `falcon-3-7b-instruct` | `universal_intelligence.community.models.falcon3_7b_instruct` | Small powerful model by TII |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/falcon3_7b_instruct/sources.yaml)<br><br>Default:<br>`cuda:Q4_K_M:llama.cpp`<br>`mps:Q4_K_M:llama.cpp`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `falcon-3-3b-instruct` | `universal_intelligence.community.models.falcon3_3b_instruct` | Compact powerful model by TII |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/falcon3_3b_instruct/sources.yaml)<br><br>Default:<br>`cuda:bfloat16:transformers`<br>`mps:bfloat16:transformers`<br>`cpu:bfloat16:transformers` |
| Text/Text | `Llama-3.3-70B-Instruct` | `universal_intelligence.community.models.llama3_3_70b_instruct` | Large powerful model by Meta |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/llama3_3_70b_instruct/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `Llama-3.1-8B-Instruct` | `universal_intelligence.community.models.llama3_1_8b_instruct` | Small powerful model by Meta |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/llama3_1_8b_instruct/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `Llama-3.2-3B-Instruct` | `universal_intelligence.community.models.llama3_2_3b_instruct` | Compact powerful model by Meta |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/llama3_2_3b_instruct/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `Llama-3.2-1B-Instruct` | `universal_intelligence.community.models.llama3_2_1b_instruct` | Ultra-compact powerful model by Meta |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/llama3_2_1b_instruct/sources.yaml)<br><br>Default:<br>`cuda:bfloat16:transformers`<br>`mps:bfloat16:transformers`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `phi-4` | `universal_intelligence.community.models.phi4` | Small powerful model by Microsoft |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/phi4/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `phi-4-mini-instruct` | `universal_intelligence.community.models.phi4_mini_instruct` | Compact powerful model by Microsoft |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/phi4_mini_instruct/sources.yaml)<br><br>Default:<br>`cuda:Q4_K_M:llama.cpp`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `smollm2-1.7b-instruct` | `universal_intelligence.community.models.smollm2_1d7b_instruct` | Small powerful model by SmolLM |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/smollm2_1d7b_instruct/sources.yaml)<br><br>Default:<br>`cuda:bfloat16:transformers`<br>`mps:MLX_8:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `smollm2-360m-instruct` | `universal_intelligence.community.models.smollm2_360m_instruct` | Ultra-compact powerful model by SmolLM |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/smollm2_360m_instruct/sources.yaml)<br><br>Default:<br>`cuda:bfloat16:transformers`<br>`mps:MLX_8:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `smollm2-135m-instruct` | `universal_intelligence.community.models.smollm2_135m_instruct` | Ultra-compact powerful model by SmolLM |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/smollm2_135m_instruct/sources.yaml)<br><br>Default:<br>`cuda:bfloat16:transformers`<br>`mps:MLX_8:mlx`<br>`cpu:bfloat16:transformers` |
| Text/Text | `mistral-7b-instruct-v0.3` | `universal_intelligence.community.models.mistral_7b_instruct_v0d3` | Small powerful model by Mistral |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/mistral_7b_instruct_v0d3/sources.yaml)<br><br>Default:<br>`cuda:Q4_K_M:llama.cpp`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `mistral-nemo-instruct-2407` | `universal_intelligence.community.models.mistral_nemo_instruct_2407` | Small powerful model by Mistral |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/mistral_nemo_instruct_2407/sources.yaml)<br><br>Default:<br>`cuda:AWQ_4:transformers`<br>`mps:MLX_3:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `OpenR1-Qwen-7B` | `universal_intelligence.community.models.openr1_qwen_7b` | Medium powerful model by Open R1 |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/openr1_qwen_7b/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | `QwQ-32B` | `universal_intelligence.community.models.qwq_32b` | Large powerful model by Qwen |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwq_32b/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |

##### Tools

| Name | Import Path | Description | Configuration Requirements |
|------|------|-------------|-----------|
| `Simple Printer` | `universal_intelligence.community.tools.simple_printer` | Prints a given text to the console | `prefix: Optional[str]`: Optional prefix for log messages |
| `Simple Error Generator` | `universal_intelligence.community.tools.simple_error_generator` | Raises an error with optional custom message | `prefix: Optional[str]`: Optional prefix for error messages |
| `MCP Client` | `universal_intelligence.community.tools.mcp_client` | Calls tools on a remote MCP server and manages server communication | `server_command: str`: Command to execute the MCP server<br>`server_args: Optional[List[str]]`: Command line arguments for the MCP server<br>`server_env: Optional[Dict[str, str]]`: Environment variables for the MCP server |
| `API Caller` | `universal_intelligence.community.tools.api_caller` | Makes HTTP requests to configured API endpoints | `base_url: str`: Base URL for the API<br>`default_headers: Optional[Dict[str, str]]`: Default headers to include in every request<br>`timeout: Optional[int]`: Request timeout in seconds |

##### Agents

| I/O | Name | Import Path | Description | Default Model | Default Tools | Default Team |
|------|------|------|-------------|-----------|-----------|-----------|
| Text/Text | `Simple Agent` (default)| `universal_intelligence.community.agents.default`<br> or `universal_intelligence.community.agents.simple_agent` | Simple Agent which can use provided Tools and Agents to complete a task |  `Qwen2.5-7B-Instruct`<br><br>`cuda:Q4_K_M:llama.cpp`<br>`mps:Q4_K_M:llama.cpp`<br>`cpu:Q4_K_M:llama.cpp` | None | None |

### Development

You are welcome to contribute to community components. Please find some introductory information below.

#### Project Structure

```txt
universal-intelligence/
├── playground/           # Playground code directory
│   ├── web/              # Example web playground
│   └── example.py               # Example playground
├── universal_intelligence/      # Source code directory
│   ├── core/             # Core library for the Universal Intelligence specification
│   │   ├── universal_model.py   # Universal Model base implementation
│   │   ├── universal_agent.py   # Universal Agent base implementation
│   │   ├── universal_tool.py    # Universal Tool base implementation
│   │   └── utils/              # Utility functions and helpers
│   ├── community/       # Community components
│   │   ├── models/        # Community-contributed models
│   │   ├── agents/        # Community-contributed agents
│   │   └── tools/         # Community-contributed tools
│   └── www/         # Web Implementation
│       ├── core/               # Core library for the Universal Intelligence web specification
│       │   ├── universalModel.ts   # Universal Model web base implementation
│       │   ├── universalAgent.ts   # Universal Agent web base implementation
│       │   ├── universalTool.ts    # Universal Tool web base implementation
│       │   └── types.ts             # Universal Intelligence web types
│       └── community/       # Web community components
│           ├── models/         # Web community-contributed models
│           ├── agents/         # Web community-contributed agents
│           └── tools/          # Web community-contributed tools
├── requirements*.txt             # Project dependencies
├── *.{yaml,toml,json,*rc,ts}     # Project configuration
├── CODE_OF_CONDUCT.md     # Community rules information
├── SECURITY.md            # Vulnerability report information
├── LICENSE             # License information
├── README_WEB.md       # Project web documentation
└── README.md           # Project documentation
```

#### Creating New Components

For faster deployment and easier maintenance, we recommend using/enhancing *shared* mixins to bootstrap new `Universal Intelligence` components. Those are made available at `./universal_intelligence/community/<component>/__utils__/mixins`. Mixins let components provide their own configurations and while levering a shared implementation. You can find an example here: [./universal_intelligence/community/models/qwen2_5_7b_instruct/model.py](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_7b_instruct/model.py).

> Model weights can be found here: https://huggingface.co 

#### Testing

Each `Universal Intelligence` component comes with its own test suite.

#### Running Tests

Installation:

```sh
# (optional) Create dedicated python environment using miniconda
conda init zsh
conda create -n universal-intelligence python=3.10.16 -y
conda activate universal-intelligence

# Install base dependencies
pip install -r requirements.txt

# Install community components dependencies
pip install -r requirements-community.txt

# Install optimizations for your currect device
pip install -r requirements-mps.txt # Apple devices
pip install -r requirements-cuda.txt # NVIDIA devices

# Install development dependencies
pip install -r requirements-dev.txt

# Install commit hook
pre-commit install

# (optional) if using the MCP tool, install dedicated MCP specific dependencies
pip install -r requirements-mcp.txt
```

> Some of the community components interface with gated models, in which case you may have to accept the model's terms on [Hugging Face](https://huggingface.co/docs/hub/en/models-gated) and log into that approved account. 
> 
> You may do so in your terminal using `huggingface-cli login`
> 
> or in your code: 
> ```python
> from huggingface_hub import login
> login()
> ```

Testing:

```bash
# python -m universal_intelligence.community.<component>.<name>.test

# examples
python -m universal_intelligence.community.models.default.test
python -m universal_intelligence.community.tools.default.test
python -m universal_intelligence.community.agents.default.test
```

> Please note that running tests may require downloading multiple configurations of the same components, and temporarily use storage space.
> Tests will be automatically filtered based on hardware requirements.

Clear downloaded models from storage:

```sh
# pip install huggingface_hub["cli"] # Install CLI
huggingface-cli delete-cache # Clear cache
```

#### Writing Tests

Test utilities provide shared test suites for each component type.

Model test examples:

- Test Suite: [`universal_intelligence/community/models/__utils__/test.py`](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/__utils__/test.py)
- Usage: [`universal_intelligence/community/models/qwen2_5_7b_instruct/test.py`](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_7b_instruct/test.py)

Agent test examples:

- Test Suite: [`universal_intelligence/community/agents/__utils__/test.py`](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/agents/__utils__/test.py)
- Usage: [`universal_intelligence/community/agents/simple_agent/test.py`](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/agents/simple_agent/test.py)

Tool test examples:

- Test Suite: [`universal_intelligence/community/tools/__utils__/test.py`](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/tools/__utils__/test.py)
- Usage: [`universal_intelligence/community/tools/simple_printer/test.py`](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/tools/simple_printer/test.py)

#### Linting

Linting will run as part of the pre-commit hook, however you may also run it manully using `pre-commit run --all-files`

## Cross-Platform Support

![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-python-16.png) ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-javascript-16.png) `Universal Intelligence` protocols and components can be used across **all platforms** (cloud, desktop, web, mobile).

- ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-python-16.png) [How to use natively with `python` (cloud, desktop)](https://github.com/blueraai/universal-intelligence/blob/main/README.md)
- ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-javascript-16.png) [How to use on the web, or in web-native apps, with `javascript/typescript` (cloud, desktop, web, mobile)](https://github.com/blueraai/universal-intelligence/blob/main/README_WEB.md)

## Thanks

Thanks for our friends at [Hugging Face](https://huggingface.co) for making open source AI a reality. ✨

This project is powered by these fantastic engines: [transformers](https://github.com/huggingface/transformersllama), [llama.cpp](https://github.com/ggml-org/llama.cpp), [mlx-lm](https://github.com/ml-explore/mlx-lm), [web-llm](https://github.com/mlc-ai/web-llm).

## Support

This software is open source, free for everyone, and lives on thanks to the community's support ☕

If you'd like to support to `universal-intelligence` here are a few ways to do so:

- ⭐ Consider leaving a star on this repository to support our team & help with visibility
- 👽 Tell your friends and collegues
- 📰 Support this project on social medias (e.g. LinkedIn, Youtube, Medium, Reddit)
- ✅ Adopt the `⚪ Universal Intelligence` specification
- 💪 Use the [Community Components](https://pypi.org/project/universal-intelligence/)
- 💡 Help surfacing/resolving issues
- 💭 Help shape the `⚪ Universal Intelligence` specification
- 🔧 Help maintain, test, enhance and create [Community Components](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/)
- ✉️ Email us security concerns
- ❤️ Sponsor this project on Github
- 🤝 [Partner with Bluera](mailto:contact@bluera.ai)


## License

Apache 2.0 License - [Bluera Inc.](https://bluera.ai)