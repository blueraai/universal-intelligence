# Universal Intelligence Core Architecture

This document details the core interfaces and abstractions of the Universal Intelligence framework. These components provide the foundation upon which the entire system is built.

## Core Abstractions

The Universal Intelligence framework is built around three primary abstractions, each defined by an abstract base class:

1. **AbstractUniversalModel** - The interface for AI models
2. **AbstractUniversalTool** - The interface for tools
3. **AbstractUniversalAgent** - The interface for agents

These abstractions establish a consistent interface and contract for all implementations, enabling composability and interoperability.

## AbstractUniversalModel

The `AbstractUniversalModel` class defines the interface for all model implementations.

### Interface Definition

```python
class AbstractUniversalModel(ABC):
    @classmethod
    @abstractmethod
    def contract(cls) -> Contract:
        """Get the contract for the model."""
        pass

    @classmethod
    @abstractmethod
    def compatibility(cls) -> list[Compatibility]:
        """Get the compatibility for the model."""
        pass

    @abstractmethod
    def __init__(
        self,
        engine: str | list[str] | None = None,
        quantization: str | list[str] | QuantizationSettings | None = None,
        max_memory_allocation: float | None = None,
        configuration: dict | None = None,
    ) -> None:
        """Initialize a Universal Model."""
        pass

    @abstractmethod
    def process(
        self,
        input: Any | list[Message],
        context: list[Any] | None = None,
        configuration: dict | None = None,
        remember: bool = False,
        keep_alive: bool = False
    ) -> tuple[Any, dict]:
        """Process input through the model."""
        pass

    @abstractmethod
    def load(self) -> None:
        """Load model into memory"""
        pass

    @abstractmethod
    def unload(self) -> None:
        """Unload model from memory"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset model chat history"""
        pass

    @abstractmethod
    def loaded(self) -> bool:
        """Check if model is loaded"""
        pass

    @abstractmethod
    def configuration(self) -> dict:
        """Get model configuration"""
        pass
```

### Key Methods

- **contract()** - Returns the contract that describes the model's capabilities
- **compatibility()** - Returns information about hardware and software compatibility
- **process()** - Core method that processes input and returns model output
- **load()** - Loads the model into memory
- **unload()** - Unloads the model from memory
- **reset()** - Clears the model's conversation history
- **loaded()** - Checks if the model is currently loaded
- **configuration()** - Returns the model's current configuration

### Key Concepts

#### Contract

The contract system specifies what a model can do, including its methods, inputs, and outputs, ensuring consistent behavior across implementations.

#### Compatibility

The compatibility system describes what hardware and software the model works with, including memory requirements and device types.

#### Process Method

The `process` method is the core function that handles input processing and response generation. It can:

- Process raw text input or structured messages
- Include contextual information
- Apply runtime configuration
- Manage memory by loading/unloading
- Remember conversation history

## AbstractUniversalTool

The `AbstractUniversalTool` class defines the interface for all tool implementations.

### Interface Definition

```python
class AbstractUniversalTool(ABC):
    @classmethod
    @abstractmethod
    def contract(cls) -> Contract:
        """Get the contract for the tool."""
        pass

    @classmethod
    @abstractmethod
    def requirements(cls) -> list[Requirement]:
        """Get the requirements for the tool."""
        pass

    @abstractmethod
    def __init__(self, configuration: dict | None = None) -> None:
        """Initialize a Universal Tool."""
        pass

    # Note: Additional methods are defined by the specific tool implementation
    # and documented in the tool's contract
```

### Key Methods

- **contract()** - Returns the contract that describes the tool's capabilities
- **requirements()** - Returns the configuration requirements for the tool
- **Additional tool-specific methods** - Each tool implements its own set of methods based on its functionality

### Key Concepts

#### Tool Contract

The tool contract specifies what methods a tool provides, along with their inputs and outputs. This allows agents to discover and use tools dynamically.

#### Tool Requirements

The requirements specify what configuration the tool needs to function (like API keys or endpoints).

## AbstractUniversalAgent

The `AbstractUniversalAgent` class defines the interface for all agent implementations.

### Interface Definition

```python
class AbstractUniversalAgent(ABC):
    @classmethod
    @abstractmethod
    def contract(cls) -> Contract:
        """Get the contract for the agent."""
        pass

    @classmethod
    @abstractmethod
    def requirements(cls) -> list[Requirement]:
        """Get the requirements for the agent."""
        pass

    @classmethod
    @abstractmethod
    def compatibility(cls) -> list[Compatibility]:
        """Get the compatibility for the agent."""
        pass

    @abstractmethod
    def __init__(
        self,
        universal_model: AbstractUniversalModel | None = None,
        expand_tools: list[AbstractUniversalTool] | None = None,
        expand_team: list["AbstractUniversalAgent"] | None = None,
    ) -> None:
        """Initialize a Universal Agent."""
        pass

    @abstractmethod
    def process(
        self,
        input: Any | list[Message] | None = None,
        context: list[Any] | None = None,
        configuration: dict | None = None,
        remember: bool = False,
        stream: bool = False,
        extra_tools: list[AbstractUniversalTool] | None = None,
        extra_team: list["AbstractUniversalAgent"] | None = None,
        keep_alive: bool = False,
    ) -> tuple[Any, dict]:
        """Process input through the agent."""
        pass

    @abstractmethod
    def load(self) -> None:
        """Load agent's model into memory"""
        pass

    @abstractmethod
    def unload(self) -> None:
        """Unload agent's model from memory"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset agent's chat history"""
        pass

    @abstractmethod
    def loaded(self) -> bool:
        """Check if agent's model is loaded"""
        pass

    @abstractmethod
    def connect(
        self,
        universal_tools: list[AbstractUniversalTool] | None = None,
        universal_agents: list["AbstractUniversalAgent"] | None = None,
    ) -> None:
        """Connect additional tools and agents."""
        pass

    @abstractmethod
    def disconnect(
        self,
        universal_tools: list[AbstractUniversalTool] | None = None,
        universal_agents: list["AbstractUniversalAgent"] | None = None,
    ) -> None:
        """Disconnect tools and agents."""
        pass
```

### Key Methods

- **contract()** - Returns the contract that describes the agent's capabilities
- **requirements()** - Returns the agent's configuration requirements
- **compatibility()** - Returns the agent's hardware and software compatibility
- **process()** - Processes input and coordinates between models, tools, and other agents
- **connect()** - Connects additional tools and agents to the agent
- **disconnect()** - Disconnects tools and agents from the agent
- **load()/unload()/loaded()/reset()** - Manages the agent's model and state

### Key Concepts

#### Agent Composition

Agents are inherently composable, allowing them to:

- Use a model for intelligence
- Use tools for extended capabilities
- Collaborate with other agents for complex tasks

#### Dynamic Connection

The `connect` and `disconnect` methods allow for runtime modification of the agent's capabilities, enabling dynamic extension of functionality.

## Supporting Types

The core architecture is supported by several important data types that enable standardization and type safety:

### Message

```python
class Message(TypedDict):
    role: str
    content: Any
```

Represents a structured message with a role (e.g., "system", "user", "assistant") and content.

### Contract

```python
class Contract(TypedDict):
    name: str
    description: str
    methods: list[Method]
```

Defines the capabilities of a component, including its methods and their signatures.

### Compatibility

```python
class Compatibility(TypedDict):
    engine: str
    quantization: str
    devices: list[str]
    memory: float
    dependencies: list[str]
    precision: int
```

Specifies the hardware and software compatibility of a component.

### Requirement

```python
class Requirement(TypedDict):
    name: str
    type: str
    schema: Schema
    description: str
    required: bool
```

Defines configuration requirements for components.

### QuantizationSettings

```python
class QuantizationSettings(TypedDict):
    default: str | None
    min_precision: str | None
    max_precision: str | None
```

Specifies settings for model quantization.

## Architecture Principles

The core architecture adheres to several key principles:

### Interface-Driven Design

All components are defined through interfaces (abstract base classes), ensuring consistent behavior and allowing for multiple implementations.

### Composition over Inheritance

The architecture favors composition (e.g., agents using models and tools) over deep inheritance hierarchies, promoting flexibility and reusability.

### Contract-Based Interoperability

The contract system allows components to declare their capabilities in a standardized way, enabling dynamic discovery and integration.

### Clear Responsibilities

Each component has a well-defined responsibility:
- Models process inputs and generate outputs
- Tools perform specific tasks
- Agents coordinate between models, tools, and other agents

### Configuration over Code

The architecture emphasizes configuration (via dictionaries and settings objects) over coding, reducing the need for custom code and making components more portable and reusable.

## Extensibility Mechanisms

The core architecture provides several mechanisms for extension:

### Implementation of Abstractions

New components can be created by implementing the abstract base classes.

### Configuration Customization

Existing components can be customized through configuration dictionaries.

### Runtime Composition

Components can be combined at runtime through agent composition.

### Plugin System

The architecture effectively functions as a plugin system, allowing third parties to create compatible components.

## Implementation Best Practices

When implementing the core abstractions, several best practices should be followed:

1. **Robust Error Handling** - Components should handle errors gracefully and provide informative error messages.
2. **Memory Management** - Components should manage memory efficiently, especially for large models.
3. **Sensible Defaults** - Provide reasonable defaults for all parameters.
4. **Clear Documentation** - Document all methods, parameters, and behaviors.
5. **Type Safety** - Utilize Python's type hints for better IDE support and code quality.
6. **Performance Optimization** - Optimize for the target hardware when possible.
7. **Testing** - Write comprehensive tests for each component.
8. **Compatibility** - Clearly document compatibility requirements and limitations.
