![Universal Intelligence](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//universal-intelligence-banner-rsm.png)

<p align="center">
    <a href="https://github.com/blueraai/universal-intelligence/releases"><img alt="GitHub Release" src="https://img.shields.io/github/release/blueraai/universal-intelligence.svg?color=1c4afe"></a>
    <a href="https://github.com/blueraai/universal-intelligence/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/blueraai/universal-intelligence.svg?color=00bf48"></a>
    <a href="https://discord.gg/7g9SrEc5yT"><img alt="Discord" src="https://img.shields.io/badge/Join-Discord-7289DA?logo=discord&logoColor=white&color=4911ff"></a>
</p>

> ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-javascript-16.png) This page aims to document **Javascript/Typescript** protocols and usage (e.g. cloud, desktop, web, mobile).
>
> Looking for [**Python instructions**](https://github.com/blueraai/universal-intelligence/blob/main/README.md)?

## Overview

`Universal Intelligence` (aka `UIN`) aims to **make AI development accessible to everyone** through a **simple interface**, which can *optionally* be *customized* to **grow with you as you learn**, up to production readiness.

It provides both a **standard protocol**, and a **library of components** implementating the protocol for you to get started —on *any platform* ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-python-16.png) ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-javascript-16.png).

> 🧩 AI made simple. [Bluera Inc.](https://bluera.ai)

Learn more by clicking the most appropriate option for you:
<details>

<summary><strong style="display: inline; cursor: pointer; margin: 0; padding: 0;">I'm new to building agentic apps</strong></summary>

<br>

Welcome! Before jumping into what this project is, let's start with the basics.

#### What is an agentic app?

Agentics apps are applications which use AI. They typically use pretrained models, or agents, to interact with the user and/or achieve tasks.

#### What is a model?

Models are artificial brains, or *neural networks* in coding terms. 🧠

They can think, but they can't act without being given the appropriate tools for the job. They are *trained* to produce a specific output, given a specific input. These can be of any type (often called modalities —eg. text, audio, image, video).

#### What is a tool?

Tools are scripted tasks, or *functions* in coding terms. 🔧

They can't think, but they can be used to achieve a pre-defined task (eg. executing a script, making an API call, interacting with a database).

#### What is an agent?

Agents are robots, or simply put, *models and tools connected together*. 🤖

> 🤖 = 🧠 + [🔧, 🔧,..]

They can think *and* act. They typically use a model to decompose a task into a list of actions, and use the appropriate tools to perform these actions.

#### What is `⚪ Universal Intelligence`?

UIN is a protocol aiming to standardize, simplify and modularize these fundamental AI components (ie. models, tools and agents), for them to be accessible by any developers, and distributed on any platform.

It provides three specifications: `Universal Model`, `Universal Tool`, and `Universal Agent`.

UIN also provides a set of **ready-made components and playgrounds** for you to get familiar with the protocol and start building in seconds.

![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-python-16.png) ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-javascript-16.png) `Universal Intelligence` can be used across **all platforms** (cloud, desktop, web, mobile).

</details>

<details>

<summary><strong style="display: inline; cursor: pointer; margin: 0; padding: 0;">I have experience in building agentic apps</strong></summary>

<br>

`Universal Intelligence` standardizes, simplifies and modularizes the usage and distribution of artifical intelligence, for it to be accessible by any developers, and distributed on any platform.

It aims to be a **framework-less agentic protocol**, removing the need for proprietary frameworks (eg. Langchain, Google ADK, Autogen, CrewAI) to build *simple, portable and composable intelligent applications*.

It does so by standardizing the fundamental building blocks used to make an intelligent application (models, tools, agents), which agentic frameworks typically (re)define and build upon —and by ensuring these blocks can communicate and run on any hardware (model, size, and precision dynamically set; agents share resources).

It provides three specifications: `Universal Model`, `Universal Tool`, and `Universal Agent`.

This project also provides a set of **community-built components and playgrounds**, implementing the UIN specification, for you to get familiar with the protocol and start building in seconds.

![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-python-16.png) ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-javascript-16.png) `Universal Intelligence` protocols and components can be used across **all platforms** (cloud, desktop, web, mobile).

#### Agentic Framework vs. Agentic Protocol

> How do they compare?

Agent frameworks (like Langchain, Google ADK, Autogen, CrewAI), each orchestrate their own versions of so-called building blocks. Some of them implement the building blocks themselves, others have them built by the community.

UIN hopes to standardize those building blocks and remove the need for a framework to run/orchestrate them. It also adds a few cool features to these blocks like portability.
For example, UIN models are designed to automatically detect the current hardware (cuda, mps, webgpu), its available memory, and run the appropriate quantization and engine for it (eg. transformers, llama.cpp, mlx, web-llm). It allows developers not to have to implement different stacks to support different devices when running models locally, and (maybe more importantly) not to have to know or care about hardware compatibility, so long as they don't try to run a rocket on a gameboy 🙂

</details>

## Get Started


Get familiar with the composable building blocks, using the default **community components**.

```sh
# Install the UIN package
npm add universalintelligence

# Log into Hugging Face CLI so you can download models
huggingface-cli login
```

#### 🧠 Simple model

```js
import { Model } from "universalintelligence" // (or in the cloud) RemoteModel

const model = new Model() // (or in the cloud) new RemoteModel({ credentials: 'openrouter-api-key' })
const [result, logs] = await model.process("Hello, how are you?")
```

> Models may run locally or in the cloud.
>
> See *Documentation>Community Components>Remote Models* for details.

#### 🔧 Simple tool

```js
import { Tool } from "universalintelligence"

const tool = new Tool()
const [result, logs] = await tool.printText({ text: "This needs to be printed" })
```

#### 🤖 Simple agent (🧠 + 🔧)

```js
import { Model, Tool, Agent, OtherAgent } from "universalintelligence"

const agent = new Agent(
  // {
  //    model: Model(),                 // customize or share 🧠 across [🤖,🤖,🤖,..]
  //    expandTools: [Tool()],          // expand 🔧 set
  //    expandTeam: [OtherAgent()]      // expand 🤖 team
  // }
)
const [result, logs] = await agent.process("Please print 'Hello World' to the console", { extraTools: [Tool()] })
```

### Playground

A ready-made playground is available to help familiarize yourself with the protocols and components.

Start the playground:

```sh
npm install && npm run build && python3 playground/web/server.py  # Ctrl+C to kill
```

Open in Chrome: `http://localhost:8000/playground/web`

## Documentation

<details>
<summary><strong style="display: inline; cursor: pointer; margin: 0; padding: 0;">Protocol Specifications</strong></summary>

## Protocol Specifications

### Universal Model

A `⚪ Universal Model` is a standardized, self-contained and configurable interface able to run a given model, irrespective of the consumer hardware and without requiring domain expertise.

It embeddeds a model (i.e. hosted, fetched, or local), one or more engines (e.g. [transformers](https://huggingface.co/docs/transformers/index), [lama.cpp](https://llama-cpp-python.readthedocs.io/en/latest/api-reference/), [mlx-lm](https://github.com/ml-explore/mlx-lm), [web-llm](https://webllm.mlc.ai)), runtime dependencies for each device type (e.g. CUDA, MPS, WebGPU), and exposes a standard interface.

While configurable, every aspect is preset for the user, based on *automatic device detection and dynamic model precision*, in order to abstract complexity and provide a simplified and portable interface.

> *Providers*: In the intent of preseting a `Universal Model` for non-technical mass adoption, we recommend defaulting to 4/8 bit quantization.

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

```js
import Model from "<provider>"

const model = new Model()
const [result, logs] = await model.process("Hello, how are you?") // 'Feeling great! How about you?'
```

> Automatically optimized for any supported browser / native web container 🔥

##### Customization Options

Simple does not mean limited. Most advanted `configuration` options remain available.

Those are defined by and specific to the *universal model provider*.

> We encourage providers to use industry standard [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) specifications, irrespective of the backend internally used for the detected device and translated accordingly, allowing for greater portability and adoption.

###### Optional Parameters

```js
import Model from "<provider>"

const model = new Model({
  credentials: '<token>', // (or) object containing credentials eg. { id: 'example', passkey: 'example' }
  engine: 'webllm', // (or) ordered by priority ['transformers', 'llama.cpp']
  quantization: 'MLC_4', // (or) ordered by priority ['Q4_K_M', 'Q8_0'] (or) auto in range {'default': 'Q4_K_M', 'minPrecision': '4bit', 'maxPrecision': '8bit'}
  maxMemoryAllocation: 0.8, // maximum allowed memory allocation in percentage
  configuration: {
    // (example)
    // "processor": {
    //     e.g. Tokenizer https://huggingface.co/docs/transformers/fast_tokenizers
    //
    //     model_max_length: 4096,
    //     model_input_names: ['token_type_ids', 'attention_mask']
    //     ...
    // },
    // "model": {
    //     e.g. AutoModel https://huggingface.co/docs/transformers/models
    //
    //     torch_dtype="auto"
    //     device_map="auto"
    //     ...
    // }
  },
  verbose: true // (or) string describing the log level
})


const [result, logs] = await model.process(
  [
    {
      "role": "system",
      "content": "You are a helpful model to recall schedules."
    },
    {
      "role": "user",
      "content": "What did I do in May?"
    },
  ], // multimodal
  {
    context: ["May: Went to the Cinema", "June: Listened to Music"],  // multimodal
    configuration: {
      // (example)
      // e.g. AutoModel Generate https://huggingface.co/docs/transformers/llm_tutorial
      //
      // max_new_tokens=2000,
      // use_cache=true,
      // temperature=1.0
      // ...
    },
    remember: true, // remember this interaction
    stream: false, // stream output asynchronously
    keepAlive: true // keep model loaded after processing the request
  }
) // 'In May, you went to the Cinema.'
```

###### Optional Methods

```js
import Model from "<provider>"
const model = Model()

// Optional
await model.load() // loads the model in memory (otherwise automatically loaded/unloaded on execution of `.process()`)
await model.loaded() // checks if model is loaded
await model.unload() // unloads the model from memory (otherwise automatically loaded/unloaded on execution of `.process()`)
await model.reset() // resets remembered chat history
await model.configuration() // gets current model configuration

// Class Optional
Model.contract()  // Contract
Model.compatibility()  // Compatibility
```

#### Universal Tool

```js
import Tool from "<provider>"

const tool = Tool(
  // { "any": "configuration" }
)
const [result, logs] = tool.exampleTask(data) // (or async)
```

###### Optional Methods

```js
import Tool from "<provider>"

// Class Optional
Tool.contract()  // Contract
Tool.requirements()  // Configuration Requirements
```

#### Universal Agent

```js
import Agent from "<provider>"

const agent = new Agent(
  // {
  //    model: Model(),                 // customize or share 🧠 across [🤖,🤖,🤖,..]
  //    expandTools: [Tool()],          // expand 🔧 set
  //    expandTeam: [OtherAgent()]      // expand 🤖 team
  // }
)
const [result, logs] = await agent.process('What happened on Friday?') // > (tool call) > 'Friday was your birthday!'
```

> Modular, and automatically optimized for any browser / native web container 🔥

##### Customization Options

Most advanted `configuration` options remain available.

Those are defined by and specific to the *universal model provider*.

> We encourage providers to use industry standard [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) specifications, irrespective of the backend internally used for the detected device and translated accordingly, allowing for greater portability and adoption.

###### Optional Parameters

```js
import Agent from "<provider>"
import OtherAgent from "<other_provider>"
import Model from "<provider>"
import Tool from "<provider>"

// This is where the magic happens ✨
// Standardization of all layers make agents composable and generalized.
// They can now utilize any 3rd party tools or agents on the fly to achieve any tasks.
// Additionally, the models powering each agent can now be hot-swapped so that
// a team of agents shares the same intelligence(s), thus removing hardware overhead,
// and scaling at virtually no cost.
const agent = new Agent({
  credentials: '<token>', // (or) object containing credentials eg. { id: 'example', passkey: 'example' }
  model: Model(), // see Universal Model API for customizations
  expandTools: [Tool()], // see Universal Tool API for customizations
  expandTeam:[OtherAgent()],  // see Universal Agent API for customizations
  configuration: {
    // agent configuration (eg. guardrails, behavior, tracing)
  },
  verbose: true // or string describing log level
})

const [result, logs] = await agent.process(
  [
    {
      "role": "system",
      "content": "You are a helpful model to recall schedules and set events."
    },
    {
      "role": "user",
      "content": "Can you schedule what we did in May again for the next month?"
    },
  ], // multimodal
  {
    context: ['May: Went to the Cinema', 'June: Listened to Music'],  // multimodal
    configuration: {
      //  (example)
      //  e.g. AutoModel Generate https://huggingface.co/docs/transformers/llm_tutorial
      //
      //  max_new_tokens=2000,
      //  use_cache=True,
      //  temperature=1.0
      //  ...
    },
    remember: true, // remember this interaction
    stream: false, // stream output asynchronously
    extraTools: [Tool()], // extra tools available for this inference; call `agent.connect()` link during initiation to persist them
    extraTeam: [OtherAgent()],  // extra agents available for this inference; call `agent.connect()` link during initiation to persist them
    keepAlive: true // keep model loaded after processing the request
  }
)
// > "In May, you went to the Cinema. Let me check the location for you."
// > (tool call: database)
// > "It was in Hollywood. Let me schedule a reminder for next month."
// > (agent call: scheduler)
// > "Alright you are all set! Hollywood cinema is now scheduled again in July."
```

###### Optional Methods

```js
import Agent from "<provider>"
import OtherAgent from "<other_provider>"
import Model from "<provider>"
import Tool from "<provider>" // e.g. API, database
const agent = Agent()
const otherAgent = OtherAgent()
const tool = Tool()

// Optional
await agent.load() // loads the agent's model in memory (otherwise automatically loaded/unloaded on execution of `.process()`)
await agent.loaded() // checks if agent is loaded
await agent.unload() // unloads the agent's model from memory (otherwise automatically loaded/unloaded on execution of `.process()`)
await agent.reset() // resets remembered chat history
await agent.connect({ tools: [tool], agents: [otherAgent] }) // connects additionnal tools/agents
await agent.disconnect({ tools: [tool], agents: [otherAgent] }) // disconnects tools/agents

// Class Optional
Agent.contract()  // Contract
Agent.requirements()  // Configuration Requirements
Agent.compatibility()  // Compatibility
```

### API

#### Universal Model

A self-contained environment for running AI models with standardized interfaces.

| Method | Parameters | Return Type | Description |
|--------|------------|-------------|-------------|
| `constructor` | • `payload.credentials?: str \| Record<string, any> = None`: Authentication information (e.g. authentication token (or) object containing credentials such as  *{ id: 'example', passkey: 'example' }*)<br>• `payload.engine?: string \| string[]`: Engine used (e.g., 'transformers', 'llama.cpp', (or) ordered by priority *['transformers', 'llama.cpp']*). Prefer setting quantizations over engines for broader portability.<br>• `payload.quantization?: string \| string[] \| QuantizationSettings`: Quantization specification (e.g., *'Q4_K_M'*, (or) ordered by priority *['Q4_K_M', 'Q8_0']* (or) auto in range *{'default': 'Q4_K_M', 'minPrecision': '4bit', 'maxPrecision': '8bit'}*)<br>• `payload.maxMemoryAllocation?: number`: Maximum allowed memory allocation in percentage<br>• `payload.configuration?: Record<string, any>`: Configuration for model and processor settings<br>• `payload.verbose?: boolean \| string = "DEFAULT"`: Enable/Disable logs, or set a specific log level | `void` | Initialize a Universal Model |
| `process` | • `input: any \| Message[]`: Input or input messages<br>• `payload.context?: any[]`: Context items (multimodal supported)<br>• `payload.configuration?: Record<string, any>`: Runtime configuration<br>• `payload.remember?: boolean`: Whether to remember this interaction. Please be mindful of the available context length of the underlaying model.<br>• `payload.keepAlive?: boolean`: Keep model loaded for faster consecutive interactions<br>• `payload.stream?: boolean`: Stream output asynchronously | `Promise<[any \| null, Record<string, any>]>` | Process input through the model and return output and logs. The output is typically the model's response and the logs contain processing metadata |
| `load` | None | `Promise<void>` | Load model into memory |
| `loaded` | None | `Promise<boolean>` | Check if model is currently loaded in memory |
| `unload` | None | `Promise<void>` | Unload model from memory |
| `reset` | None | `Promise<void>` | Reset model chat history |
| `configuration` | None | `Promise<Record<string, any>>` | Get current model configuration |
| `ready` | None | `Promise<void>` | Wait for the model to be ready |
| `(class).contract` | None | `Contract` | Model description and interface specification |
| `(class).compatibility` | None | `Compatibility[]` | Model compatibility specification |

#### Universal Tool

A standardized interface for tools that can be used by models and agents.

| Method | Parameters | Return Type | Description |
|--------|------------|-------------|-------------|
| `constructor` | • `configuration?: Record<string, any>`: Tool configuration including credentials | `void` | Initialize a Universal Tool |
| `(class).contract` | None | `Contract` | Tool description and interface specification |
| `(class).requirements` | None | `Requirement[]` | Tool configuration requirements |

Additional methods are defined by the specific tool implementation and documented in the tool's contract.

Any tool specific method _must return_ a `Promise<[any, Record<string, any>]>`, respectively `(result, logs)`.

#### Universal Agent

An AI agent powered by Universal Models and Tools with standardized interfaces.

| Method | Parameters | Return Type | Description |
|--------|------------|-------------|-------------|
| `constructor` | • `payload.credentials?: str \| Record<string, any> = None`: Authentication information (e.g. authentication token (or) object containing credentials such as  *{ id: 'example', passkey: 'example' }*)<br>• `payload.model?: AbstractUniversalModel`: Model powering this agent<br>• `payload.expandTools?: AbstractUniversalTool[]`: Tools to connect<br>• `payload.expandTeam?: AbstractUniversalAgent[]`: Other agents to connect<br>• `payload.configuration?: Record<string, any>`: Agent configuration (eg. guardrails, behavior, tracing)<br>• `payload.verbose?: boolean \| string = "DEFAULT"`: Enable/Disable logs, or set a specific log level | `void` | Initialize a Universal Agent |
| `process` | • `input: any \| Message[]`: Input or input messages<br>• `payload.context?: any[]`: Context items (multimodal)<br>• `payload.configuration?: Record<string, any>`: Runtime configuration<br>• `payload.remember?: boolean`: Remember this interaction. Please be mindful of the available context length of the underlaying model.<br>• `payload.stream?: boolean`: Stream output asynchronously<br>• `payload.extraTools?: AbstractUniversalTool[]`: Additional tools<br>• `payload.extraTeam?: AbstractUniversalAgent[]`: Additional agents<br>• `payload.keepAlive?: boolean`: Keep underlaying model loaded for faster consecutive interactions | `Promise<[any \| null, Record<string, any>]>` | Process input through the agent and return output and logs. The output is typically the agent's response and the logs contain processing metadata including tool/agent calls |
| `load` | None | `Promise<void>` | Load agent's model into memory |
| `loaded` | None | `Promise<boolean>` | Check if the agent's model is currently loaded in memory |
| `unload` | None | `Promise<void>` | Unload agent's model from memory |
| `reset` | None | `Promise<void>` | Reset agent's chat history |
| `connect` | • `payload.tools?: AbstractUniversalTool[]`: Tools to connect<br>• `payload.agents?: AbstractUniversalAgent[]`: Agents to connect | `Promise<void>` | Connect additional tools and agents |
| `disconnect` | • `payload.tools?: AbstractUniversalTool[]`: Tools to disconnect<br>• `payload.agents?: AbstractUniversalAgent[]`: Agents to disconnect | `Promise<void>` | Disconnect tools and agents |
| `(class).contract` | None | `Contract` | Agent description and interface specification |
| `(class).requirements` | None | `Requirement[]` | Agent configuration requirements |
| `(class).compatibility` | None | `Compatibility[]` | Agent compatibility specification |

#### Data Structures

##### Message

| Field | Type | Description |
|-------|------|-------------|
| `role` | `string` | The role of the message sender (e.g., "system", "user") |
| `content` | `any` | The content of the message (multimodal supported) |

##### Schema

| Field | Type | Description |
|-------|------|-------------|
| `maxLength` | `number?` | Maximum length constraint |
| `pattern` | `string?` | Pattern constraint |
| `minLength` | `number?` | Minimum length constraint |
| `nested` | `Argument[]?` | Nested argument definitions for complex types |
| `properties` | `Record<string, Schema>?` | Property definitions for object types |
| `items` | `Schema?` | Schema for array items |
| `oneOf` | `any[]?` | One of the specified schemas |

##### Argument

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Name of the argument |
| `type` | `string` | Type of the argument |
| `schema` | `Schema?` | Schema constraints |
| `description` | `string` | Description of the argument |
| `required` | `boolean` | Whether the argument is required |

##### Output

| Field | Type | Description |
|-------|------|-------------|
| `type` | `string` | Type of the output |
| `description` | `string` | Description of the output |
| `required` | `boolean` | Whether the output is required |
| `schema` | `Schema?` | Schema constraints |

##### Method

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Name of the method |
| `description` | `string` | Description of the method |
| `arguments` | `Argument[]` | List of method arguments |
| `outputs` | `Output[]` | List of method outputs |
| `asynchronous` | `boolean?` | Whether the method is asynchronous (default: false) |

##### Contract

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Name of the contract |
| `description` | `string` | Description of the contract |
| `methods` | `Method[]` | List of available methods |

##### Requirement

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Name of the requirement |
| `type` | `string` | Type of the requirement |
| `schema` | `Schema` | Schema constraints |
| `description` | `string` | Description of the requirement |
| `required` | `boolean` | Whether the requirement is required |

##### Compatibility

| Field | Type | Description |
|-------|------|-------------|
| `engine` | `string` | Supported engine |
| `quantization` | `string` | Supported quantization |
| `devices` | `string[]` | List of supported devices |
| `memory` | `number` | Required memory in GB |
| `dependencies` | `string[]` | Required software dependencies |
| `precision` | `number` | Precision in bits |

##### QuantizationSettings

| Field | Type | Description |
|-------|------|-------------|
| `default` | `string?` | Default quantization to use (e.g., 'Q4_K_M') |
| `minPrecision` | `string?` | Minimum precision requirement (e.g., '4bit') |
| `maxPrecision` | `string?` | Maximum precision requirement (e.g., '8bit') |

### Development

Abstract classes and types for `Universal Intelligence` components are made available by the package if you wish to develop and publish your own.

```sh
# Install abstracts
npm install universalintelligence
```

```js
import universalintelligence from "universalintelligence"
const { AbstractUniversalModel, AbstractUniversalTool, AbstractUniversalAgent, UniversalIntelligenceTypes } = universalintelligence

class UniversalModel extends AbstractUniversalModel {
  // ...
}

class UniversalTool extends AbstractUniversalTool {
  // ...
}

class UniversalAgent extends AbstractUniversalAgent {
  // ...
}
```

If you wish to contribute to community based components, [mixins](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/www/community/models/__utils__/mixins) are made available to allow quickly bootstrapping new `Universal Models`.

> See *Community>Development* section below for additional information.

</details>

<details>
<summary><strong style="display: inline; cursor: pointer; margin: 0; padding: 0;">Community Components</strong></summary>


## Community Components

The `universal-intelligence` package provides several community-built models, agents, and tools that you can use out of the box.

### Installation

```sh
npm install universalintelligence
```

> Some of the community components interface with gated models, in which case you may have to accept the model's terms on [Hugging Face](https://huggingface.co/docs/hub/en/models-gated) and log into that approved account.
>
> You may do so in your terminal using `huggingface-cli login`


### Playground

You can get familiar with the library using our ready-made playground

Start the playground:

```sh
npm install && npm run build && python3 playground/web/server.py  # Ctrl+C to kill
```

Open in Chrome: `http://localhost:8000/playground/web`

### Usage

#### Local Models

```javascript
import universalintelligence from "universalintelligence"
const Model = universalintelligence.community.models.local.Model

const model = new Model()
const [result, logs] = await model.process("Hello, how are you?")
```

> View [Universal Intelligence Protocols](https://github.com/blueraai/universal-intelligence/blob/main/README_WEB.md) for additional information.

#### Remote Models

```javascript
import universalintelligence from "universalintelligence"
const Model = universalintelligence.community.models.remote.Model

const model = new Model({ credentials: 'your-openrouter-api-key-here' })
const [result, logs] = await model.process("Hello, how are you?")
```

> View [Universal Intelligence Protocols](https://github.com/blueraai/universal-intelligence/blob/main/README_WEB.md) for additional information.

#### Tools

```javascript
import universalintelligence from "universalintelligence"
const Tool = universalintelligence.community.tools.SimplePrinter

const tool = new Tool()
const [result, logs] = await tool.printText({ text: "This needs to be printed" })
```

> View [Universal Intelligence Protocols](https://github.com/blueraai/universal-intelligence/blob/main/README_WEB.md) for additional information.

#### Agents

```javascript
import universalintelligence from "universalintelligence"
const Agent = universalintelligence.community.agents.Agent

const agent = new Agent(
  // {
  //    model: Model(),                 // customize or share 🧠 across [🤖,🤖,🤖,..]
  //    expandTools: [Tool()],          // expand 🔧 set
  //    expandTeam: [OtherAgent()]      // expand 🤖 team
  // }
)
const [result, logs] = await agent.process("Please print 'Hello World' to the console", { extraTools: [Tool()] })
```

> View [Universal Intelligence Protocols](https://github.com/blueraai/universal-intelligence/blob/main/README_WEB.md) for additional information.

### Supported Components

#### Models

##### Local Models

> Import path: `universalintelligence.community.models.local.<import>`
>
> (eg. *universalintelligence.community.models.local.Model*)

| I/O | Name | Import | Description | Supported Configurations |
|------|------|------|-------------|-----------|
| Text/Text | *Qwen2.5-7B-Instruct* | `Qwen2_5_7b_Instruct` | Small powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/sources.tsblob/main/universal_intelligence/www/community/models/qwen2_5_7b_instruct/sources.ts)<br><br>Default:<br>`webgpu:MLC_4:webllm` |
| Text/Text | *Qwen2.5-3B-Instruct* (default) | `Qwen2_5_3b_Instruct`<br>or `Model` | Compact powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/sources.tsblob/main/universal_intelligence/www/community/models/qwen2_5_3b_instruct/sources.ts)<br><br>Default:<br>`webgpu:MLC_4:webllm` |
| Text/Text | *Qwen2.5-1.5B-Instruct* | `Qwen2_5_1d5b_Instruct` | Ultra-compact powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/sources.tsblob/main/universal_intelligence/www/community/models/qwen2_5_1d5b_instruct/sources.ts)<br><br>Default:<br>`webgpu:MLC_4_32:webllm` |
| Text/Text | *Qwen2.5-0.5B-Instruct* | `Qwen2_5_0d5b_Instruct` | Ultra-compact powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/sources.tsblob/main/universal_intelligence/www/community/models/qwen2_5_0d5b_instruct/sources.ts)<br><br>Default:<br>`webgpu:MLC_8_32:webllm` |

##### Remote Models

> Import path: `universalintelligence.community.models.remote.<import>`
>
> (eg. *universalintelligence.community.models.remote.Model*)

| I/O | Name | Import | Description | Inference |
|------|------|------|-------------|-----------|
| Text/Text | *openrouter/auto* | `default` (default) | Your prompt will be processed by a meta-model and routed to one of dozens of models (see below), optimizing for the best possible output. To see which model was used, visit [Activity](/activity), or read the `model` attribute of the response. Your response will be priced at the same rate as the routed model. The meta-model is powered by [Not Diamond](https://docs.notdiamond.ai/docs/how-not-diamond-works). Learn more in our [docs](/docs/model-routing). Requests will be routed to the following models:- [openai/gpt-4o-2024-08-06](/openai/gpt-4o-2024-08-06)- [openai/gpt-4o-2024-05-13](/openai/gpt-4o-2024-05-13)- [openai/gpt-4o-mini-2024-07-18](/openai/gpt-4o-mini-2024-07-18)- [openai/chatgpt-4o-latest](/openai/chatgpt-4o-latest)- [openai/o1-preview-2024-09-12](/openai/o1-preview-2024-09-12)- [openai/o1-mini-2024-09-12](/openai/o1-mini-2024-09-12)- [anthropic/claude-3.5-sonnet](/anthropic/claude-3.5-sonnet)- [anthropic/claude-3.5-haiku](/anthropic/claude-3.5-haiku)- [anthropic/claude-3-opus](/anthropic/claude-3-opus)- [anthropic/claude-2.1](/anthropic/claude-2.1)- [google/gemini-pro-1.5](/google/gemini-pro-1.5)- [google/gemini-flash-1.5](/google/gemini-flash-1.5)- [mistralai/mistral-large-2407](/mistralai/mistral-large-2407)- [mistralai/mistral-nemo](/mistralai/mistral-nemo)- [deepseek/deepseek-r1](/deepseek/deepseek-r1)- [meta-llama/llama-3.1-70b-instruct](/meta-llama/llama-3.1-70b-instruct)- [meta-llama/llama-3.1-405b-instruct](/meta-llama/llama-3.1-405b-instruct)- [mistralai/mixtral-8x22b-instruct](/mistralai/mixtral-8x22b-instruct)- [cohere/command-r-plus](/cohere/command-r-plus)- [cohere/command-r](/cohere/command-r) |  `openrouter` |

#### Tools

> Import path: `universalintelligence.community.tools.<import>`
>
> (eg. *universalintelligence.community.tools.ApiCaller*)

| Name | Import | Description | Configuration Requirements |
|------|------|-------------|-----------|
| *Simple Printer* | `SimplePrinter` | Prints a given text to the console | `prefix?: string`: Optional prefix for log messages |
| *Simple Error Generator* | `SimpleErrorGenerator` | Raises an error with optional custom message | `prefix?: string`: Optional prefix for error messages |
| *API Caller* | `ApiCaller` | Makes HTTP requests to configured API endpoints | `url: string`: URL for the API<br>`method?: string`: HTTP method (GET, POST, PUT, DELETE, PATCH)<br>`body?: object`: Request body for POST/PUT/PATCH requests<br>`params?: object`: Query parameters<br>`headers?: object`: Additional headers to include<br>`timeout?: number`: Request timeout in seconds |

#### Agents

> Import path: `universalintelligence.community.agents.<import>`
>
> (eg. *universalintelligence.community.agents.Agent*)

| I/O | Name | Import | Description | Default Model | Default Tools | Default Team |
|------|------|------|-------------|-----------|-----------|-----------|
| Text/Text | *Simple Agent* (default) | `Agent`<br> or `SimpleAgent` | Simple Agent which can use provided Tools and Agents to complete a task |  `Qwen2.5-7B-Instruct`<br><br>`webgpu:MLC_4:webllm` | None | None |

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

For faster deployment and easier maintenance, we recommend using/enhancing *shared* mixins to bootstrap new `Universal Intelligence` components. Those are made available at `./universal_intelligence/www/community/<component>/__utils__/mixins`. Mixins let components provide their own configurations and while levering a shared implementation. You can find an example here: [./universal_intelligence/www/community/models/qwen2_5_7b_instruct/model.ts](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/www/community/models/qwen2_5_7b_instruct/model.ts).

> Model weights can be found here: https://huggingface.co

</details>

## Cross-Platform Support

![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-python-16.png) ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-javascript-16.png) `Universal Intelligence` protocols and components can be used across **all platforms** (cloud, desktop, web, mobile).

- ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-python-16.png) [How to use natively with `python` (cloud, desktop)](https://github.com/blueraai/universal-intelligence/blob/main/README.md)
- ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-javascript-16.png) [How to use on the web, or in web-native apps, with `javascript/typescript` (cloud, desktop, web, mobile)](https://github.com/blueraai/universal-intelligence/blob/main/README_WEB.md)
