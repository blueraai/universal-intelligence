# Directory Structure
```
playground/
  web/
    index.html
    index.js
    server.py
    styles.css
  __init__.py
  __utils__.py
  example.py
universal_intelligence/
  community/
    __utils__/
      logger.py
    agents/
      __utils__/
        test.py
      default/
        __init__.py
        test.py
      simple_agent/
        __init__.py
        agent.py
        test.py
    models/
      __utils__/
        mixins/
          hf_text_to_text/
            interface.py
            meta.py
            types.py
          openrouter_text_to_text/
            interface.py
            meta.py
            types.py
        test.py
    tools/
      __utils__/
        test.py
      api_caller/
        __init__.py
        test.py
        tool.py
      default/
        __init__.py
        test.py
      mcp_client/
        __init__.py
        test.py
        tool.py
      simple_error_generator/
        __init__.py
        test.py
        tool.py
      simple_printer/
        __init__.py
        test.py
        tool.py
  core/
    utils/
      types.py
    __init__.py
    universal_agent.py
    universal_model.py
    universal_tool.py
  www/
    community/
      __utils__/
        logger.ts
      agents/
        simple_agent/
          agent.ts
          index.ts
        index.ts
      models/
        __utils__/
          mixins/
            hf_text_to_text/
              interface.ts
              meta.ts
              types.ts
            openrouter_text_to_text/
              interface.ts
              meta.ts
              types.ts
        index.ts
      tools/
        api_caller/
          index.ts
          tool.ts
        simple_error_generator/
          index.ts
          tool.ts
        simple_printer/
          index.ts
          tool.ts
        index.ts
      index.ts
    core/
      index.ts
      types.ts
      UniversalAgent.ts
      UniversalModel.ts
      UniversalTool.ts
    index.ts
  __init__.py
.gitignore
.nvmrc
.pre-commit-config.yaml
eslint.config.js
LICENSE
package.json
pyproject.toml
README_WEB.md
README.md
requirements-community.txt
requirements-cuda.txt
requirements-dev.txt
requirements-mcp.txt
requirements-mps.txt
requirements.txt
tsconfig.json
vite.config.ts
```

# Files

## File: playground/web/index.html
````html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
    <title>Universal Intelligence Playground</title>
</head>
<body>
    <div id="container"><div id="logo"></div><h1>Universal Intelligence</h1></div>
    <h2>Playground</h2>
    <div id="info">
        Open your browser's developer console to see the <a href="https://github.com/blueraai/universal-intelligence/blob/main/playground/web/index.js" target="_blank">playground code</a> in action.
        <br>
        <br>
        <div id="note">
            Note: Safari and Firefox currently only support running AI components in their nightly/beta versions.<br>Try Chrome for full support. See <a href="https://developer.mozilla.org/en-US/docs/Web/API/GPU/requestAdapter#browser_compatibility" target="_blank">browser compatibility</a> for more details.
        </div>
    </div>
    <script type="module" src="./index.js"></script>
</body>
</html>
````

## File: playground/web/index.js
````javascript
console.warn("⚪ Universal Intelligence \n\n", universalIntelligence);
const model = new Model();
const [modelResult, modelLogs] = await model.process("Hello, how are you?");
console.warn("🧠 Model \n\n", modelResult, modelLogs);
const tool = new Tool();
const [toolResult, toolLogs] = await tool.printText({ text: "This needs to be printed" });
console.warn("🔧 Tool \n\n", toolResult, toolLogs);
const agent = new Agent();
const [agentResult, agentLogs] = await agent.process("Please print 'Hello World' to the console", { extraTools: [tool] });
console.warn("🤖 Simple Agent \n\n", agentResult, agentLogs);
const apiTool = new APICaller();
const otherAgent = new Agent({ model: model, expandTools: [apiTool] });
const [otherAgentResult, otherAgentLogs] = await otherAgent.process("Please fetch the latest space news articles by calling the following API endpoint: GET https://api.spaceflightnewsapi.net/v4/articles");
console.warn("🤖 API Agent \n\n", otherAgentResult, otherAgentLogs);
````

## File: playground/web/server.py
````python
class CustomHandler(SimpleHTTPRequestHandler)
⋮----
def end_headers(self)
def guess_type(self, path)
def do_GET(self)
⋮----
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
⋮----
server_address = ("", 8000)
httpd = HTTPServer(server_address, CustomHandler)
````

## File: playground/web/styles.css
````css
:root {
⋮----
#container {
h1 {
⋮----
#logo {
⋮----
html, body {
⋮----
h2 {
#info {
#note {
a {
a:hover {
````

## File: playground/__init__.py
````python

````

## File: playground/__utils__.py
````python
def formatted_print(prefix: str, payload: Any, logs: Any = None)
````

## File: playground/example.py
````python
model = Model()
⋮----
tool = SimplePrinterTool()
⋮----
agent = Agent()
⋮----
tool = APITool()
agent = Agent(model=model)
````

## File: universal_intelligence/community/__utils__/logger.py
````python
class Color(Enum)
⋮----
BLACK = "\033[30m"
GRAY = "\033[90m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
ORANGE = "\033[38;5;208m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"
class LogLevel(Enum)
⋮----
NONE = 0
DEFAULT = 1
DEBUG = 2
class LoggerStream(io.TextIOBase)
⋮----
def __init__(self, logger)
def write(self, text)
def flush(self)
⋮----
@dataclass
class Logger
⋮----
def __init__(self, log_level: LogLevel = LogLevel.DEFAULT)
def __enter__(self)
def __exit__(self, exc_type, exc_val, exc_tb)
def cleanup(self) -> None
def __del__(self)
def set_log_level(self, level: LogLevel) -> None
def print(self, prefix: str | None = None, message: str | None = None, payload: Any | None = None, color: Color | None = None, newline: bool = True, replace_last_line: bool = False, debug: bool = False) -> None
⋮----
output = [" ◉ UIN "]
⋮----
text = " ".join(output)
⋮----
text = f"{color.value}{text}{Color.RESET.value}"
⋮----
def art(self, name: str, color: Color | None = None) -> None
⋮----
art_map = {
art = art_map.get(name, name)
⋮----
art = f"{color.value}{art}{Color.RESET.value}"
⋮----
def separator(self, prefix: str | None = None, message: str | None = None, color: Color | None = None) -> None
````

## File: universal_intelligence/community/agents/__utils__/test.py
````python
class TestStatus(Enum)
⋮----
PENDING = "\033[90m[PENDING]"
SUCCESS = "\033[92m[SUCCESS]"
FAILURE = "\033[91m[FAILURE]"
def test_meta_information(agent_class: AbstractUniversalAgent)
⋮----
contract = agent_class.contract()
requirements = agent_class.requirements()
compatibility = agent_class.compatibility()
⋮----
def test_agent(agent_class: AbstractUniversalAgent, inference_config=None)
⋮----
inference_config = {
⋮----
agent = agent_class()
required_methods = [
⋮----
def run_all_tests(agent_class: AbstractUniversalAgent, inference_config: dict | None = None)
````

## File: universal_intelligence/community/agents/default/__init__.py
````python
__all__ = ["UniversalAgent"]
````

## File: universal_intelligence/community/agents/default/test.py
````python

````

## File: universal_intelligence/community/agents/simple_agent/__init__.py
````python
__all__ = ["UniversalAgent"]
````

## File: universal_intelligence/community/agents/simple_agent/agent.py
````python
class UniversalAgent(AbstractUniversalAgent)
⋮----
_contract: ClassVar[Contract] = {
_requirements: ClassVar[list[Requirement]] = []
_compatibility: ClassVar[list[Compatibility]] = [
_default_tools: ClassVar[list[AbstractUniversalTool]] = []
_default_team: ClassVar[list[AbstractUniversalAgent]] = []
⋮----
@classmethod
    def contract(cls) -> Contract
⋮----
@classmethod
    def compatibility(cls) -> list[Compatibility]
⋮----
@classmethod
    def requirements(cls) -> list[Requirement]
⋮----
tools = self.tools + (extra_tools if extra_tools else [])
team = self.team + (extra_team if extra_team else [])
tool_contracts = [tool.contract() for tool in tools]
team_contracts = [agent.contract() for agent in team]
capabilities = {
planning_prompt = f"""Given the following user query and available capabilities, analyze if and how the available tools and team members can help satisfy the query.
⋮----
planned_calls = yaml.safe_load(plan_response)
⋮----
valid_calls = []
⋮----
results = []
⋮----
dependency_type = call["dependency_type"]
dependency_name = call["dependency_name"]
method_name = call["method_name"]
arguments = call["arguments"]
⋮----
dependencies = tools
⋮----
dependencies = team
dependency = next(
⋮----
method = getattr(dependency, method_name)
contract = dependency.contract()
is_async = False
⋮----
is_async = method_contract.get("asynchronous", False)
⋮----
query = input if isinstance(input, str) else input[-1]["content"]
# Plan dependency calls with extra tools and agents
⋮----
planned_calls = self._plan_dependency_calls(query, extra_tools, extra_team)
⋮----
# Execute planned calls with extra tools and agents
⋮----
call_results = self._execute_dependency_calls(planned_calls, extra_tools, extra_team)
⋮----
# Format results as YAML for the model
results_yaml = yaml.dump({"original_query": query, "dependency_calls": call_results}, sort_keys=False)
# Have model generate final response using call results
final_prompt = f"""Given the original query and results from dependency calls, generate a final response.
# TODO: Add streaming support
⋮----
def load(self) -> None
def loaded(self) -> bool
def unload(self) -> None
def reset(self) -> None
````

## File: universal_intelligence/community/agents/simple_agent/test.py
````python

````

## File: universal_intelligence/community/models/__utils__/mixins/hf_text_to_text/interface.py
````python
class UniversalModelMixin(AbstractUniversalModel)
⋮----
def _get_available_memory(self, device_type: str) -> float
⋮----
total_memory = 0
⋮----
device = torch.cuda.get_device_properties(i)
device_memory = device.total_memory
device_allocated = torch.cuda.memory_allocated(i)
device_cached = torch.cuda.memory_reserved(i)
device_available = device_memory - device_allocated
⋮----
total_available = total_memory / (1024**3)
⋮----
system_memory = psutil.virtual_memory()
driver_memory = torch.mps.driver_allocated_memory()
total_available = (system_memory.available + driver_memory) / (1024**3)
⋮----
message = "Hugging Face login not detected. Some models may require authentication to download.\n"
⋮----
device_type = "cpu"
_device_warning = False
⋮----
device_type = "cuda"
⋮----
device_type = "mps"
⋮----
_device_warning = True
⋮----
device_sources = self._sources.get(device_type, self._sources["cpu"])
⋮----
default_quant = next(quant for quant, source in device_sources.items() if source.get("is_default", False))
required_memory = device_sources[default_quant].get("memory", float("inf"))
available_memory = self._get_available_memory(device_type) * self.usable_memory
⋮----
quantizations = sorted(
⋮----
required_memory = source.get("memory", float("inf"))
⋮----
required_memory = device_sources[self.quantization].get("memory", float("inf"))
⋮----
required_memory = device_sources[quant].get("memory", float("inf"))
⋮----
min_precision = 4
max_precision = 8
⋮----
min_precision = extract_precision_from_descriptor(self.quantization.min_precision)
⋮----
default_quant = self.quantization.default
⋮----
min_precision = min(4, device_sources[default_quant].get("precision", 32))
⋮----
max_precision = extract_precision_from_descriptor(self.quantization.max_precision)
⋮----
max_precision = device_sources[default_quant].get("precision", 32)
⋮----
precision = source.get("precision", 32)
⋮----
supported_quantizations = device_sources.keys()
⋮----
available_engines = device_sources[self.quantization]["available_engines"]
⋮----
default_engine = next(
⋮----
default_engine = available_engines[0]["name"]
⋮----
supported_engines = {engine["name"] for engine in available_engines}
⋮----
def _translate_model_config(self) -> dict
⋮----
config = self._model_configuration[self.engine].copy()
⋮----
param_mapping = {
⋮----
llama_param = param_mapping.get(param)
⋮----
def _format_chat_prompt(self, messages: list[Message], add_generation_prompt: bool = True) -> str
⋮----
prompt = ""
⋮----
role = msg["role"]
content = msg["content"]
⋮----
def _translate_generation_config(self, configuration: dict | None = None) -> dict
⋮----
result = None
⋮----
result = self._inference_configuration[self.engine].copy()
⋮----
result = configuration
⋮----
translated = {}
⋮----
result = translated
⋮----
result = self._inference_configuration["llama.cpp"].copy()
⋮----
def process(self, input: str | list[Message], context: list[Any] | None = None, configuration: dict | None = None, remember: bool = False, keep_alive: bool = False) -> tuple[Any, dict]
⋮----
messages = input if isinstance(input, list) else [{"role": "user", "content": input}]
⋮----
messages = [{"role": "system", "content": str(ctx)} for ctx in context] + messages
⋮----
messages = self.history + messages
⋮----
input_processor_config = self._processor_configuration[self.engine]["input"].copy()
output_processor_config = self._processor_configuration[self.engine]["output"].copy()
⋮----
input_text = self.tokenizer.apply_chat_template(
inputs = self.tokenizer(
gen_config = self._translate_generation_config(configuration)
outputs = self.model.generate(**inputs, **gen_config)
response = self.tokenizer.decode(
⋮----
input_text = "\n".join(msg["content"] for msg in messages)
⋮----
max_tokens = gen_config.get("max_tokens", 2500)
temp = gen_config.get("temp", 0.1)
top_p = gen_config.get("top_p", 0.9)
sampler = make_sampler(temp, top_p=top_p)
generate_kwargs = {
⋮----
response = generate(self.model, self.tokenizer, prompt=input_text, **generate_kwargs)
⋮----
prompt = self._format_chat_prompt(messages)
⋮----
response = self.model(prompt, **gen_config)["choices"][0]["text"].strip()
⋮----
def load(self) -> None
⋮----
model_id = self.engine_config["model_id"]
tokenizer_config = self._processor_configuration[self.engine]["input"]["tokenizer"].copy()
⋮----
special_tokens = tokenizer_config.pop("special_tokens", {})
⋮----
model_config = self._translate_model_config()
⋮----
model_file = self.engine_config["model_file"]
model_path = hf_hub_download(repo_id=model_id, filename=model_file, repo_type="model")
⋮----
def unload(self) -> None
def loaded(self) -> bool
def configuration(self) -> dict
⋮----
config = {
⋮----
def reset(self) -> None
````

## File: universal_intelligence/community/models/__utils__/mixins/hf_text_to_text/meta.py
````python
def extract_precision_from_descriptor(precision_descriptor: str) -> int
def generate_sources_from_yaml(yaml_path: str) -> Sources
⋮----
valid_devices = {"cuda", "mps", "cpu"}
⋮----
data = yaml.safe_load(f)
⋮----
sources: Sources = {"cuda": {}, "mps": {}, "cpu": {}}
default_quantizations = data["model_info"].get("default_quantization", {})
⋮----
required_fields = ["engine", "model_id", "model_size", "supported_devices"]
missing_fields = [field for field in required_fields if field not in quant_info]
⋮----
supported_devices = quant_info.get("supported_devices", [])
⋮----
invalid_devices = set(supported_devices) - valid_devices
⋮----
engine_config = {
⋮----
quant_config = {
⋮----
"precision": int(re.search(r"\d+", quant_name).group() if re.search(r"\d+", quant_name) else "32"),  # Extract first sequence of consecutive digits or default to 32
⋮----
# Add to each supported device
⋮----
# If quantization already exists for this device, append engine
⋮----
# New engine is not default since we already have engines
engine_config_copy = copy.deepcopy(engine_config)
⋮----
# First engine for this quantization
⋮----
# Set as default if it matches device's default quantization
⋮----
default_count = sum(1 for quant in sources[device].values() if quant["is_default"])
⋮----
def generate_standard_contract(name: str, description: str) -> Contract
def generate_standard_compatibility(sources: Sources) -> list[Compatibility]
⋮----
compatibilities = []
⋮----
engines = quant_config["available_engines"]
⋮----
engine = engine_config["name"]
compatibility: Compatibility = {
````

## File: universal_intelligence/community/models/__utils__/mixins/hf_text_to_text/types.py
````python
class EngineConfig(TypedDict)
⋮----
name: str
model_id: str
model_file: str | None
is_default: bool
class QuantizationConfig(TypedDict)
⋮----
available_engines: list[EngineConfig]
⋮----
memory: float
precision: int
Sources = dict[Literal["cuda", "mps", "cpu"], dict[str, QuantizationConfig]]
ModelConfiguration = dict[str, dict[str, Any]]
InferenceConfiguration = dict[str, dict[str, Any]]
class InputProcessorConfig(TypedDict, total=False)
⋮----
tokenizer: dict[str, Any]
chat_template: dict[str, Any]
class ProcessorConfig(TypedDict, total=False)
⋮----
input: InputProcessorConfig
output: dict[str, Any]
ProcessorConfiguration = dict[Literal["transformers", "mlx-lm", "llama.cpp"], ProcessorConfig]
class ChatTemplate(TypedDict)
⋮----
system_start: str
system_end: str
user_start: str
user_end: str
assistant_start: str
assistant_end: str
default_system_message: str
generation_prompt: str
class QuantizationSettings(TypedDict)
⋮----
default: str | None
min_precision: Literal["2bit", "3bit", "4bit", "5bit", "6bit", "8bit", "16bit", "32bit"] | None
max_precision: Literal["2bit", "3bit", "4bit", "5bit", "6bit", "8bit", "16bit", "32bit"] | None
max_memory_allocation: float | None
````

## File: universal_intelligence/community/models/__utils__/mixins/openrouter_text_to_text/interface.py
````python
class UniversalModelMixin(AbstractUniversalModel)
⋮----
credentials = {"api_key": credentials}
⋮----
response = requests.get("https://openrouter.ai/api/v1/credits", headers={"Authorization": f"Bearer {credentials['api_key']}"})
⋮----
def _translate_generation_config(self, configuration: dict | None = None) -> dict
⋮----
result = self._inference_configuration[self.engine].copy()
⋮----
openrouter_params = {}
⋮----
result = openrouter_params
⋮----
def process(self, input: str | list[Message], context: list[Any] | None = None, configuration: dict | None = None, remember: bool = False) -> tuple[Any, dict]
⋮----
messages = input if isinstance(input, list) else [{"role": "user", "content": input}]
⋮----
messages = [{"role": "system", "content": str(ctx)} for ctx in context] + messages
⋮----
messages = self.history + messages
⋮----
generation_config = self._translate_generation_config(configuration)
⋮----
response = requests.post(
⋮----
output = (response.json())["choices"][0]["message"]["content"]
⋮----
def load(self) -> None
def unload(self) -> None
def loaded(self) -> bool
def configuration(self) -> dict
⋮----
config = {
⋮----
def reset(self) -> None
````

## File: universal_intelligence/community/models/__utils__/mixins/openrouter_text_to_text/meta.py
````python
def generate_standard_contract(name: str, description: str) -> Contract
def generate_standard_compatibility() -> list[Compatibility]
````

## File: universal_intelligence/community/models/__utils__/mixins/openrouter_text_to_text/types.py
````python
ModelConfiguration = dict[str, dict[str, Any]]
InferenceConfiguration = dict[str, dict[str, Any]]
class QuantizationSettings(TypedDict)
⋮----
default: str | None
min_precision: Literal["2bit", "3bit", "4bit", "5bit", "6bit", "8bit", "16bit", "32bit"] | None
max_precision: Literal["2bit", "3bit", "4bit", "5bit", "6bit", "8bit", "16bit", "32bit"] | None
max_memory_allocation: float | None
````

## File: universal_intelligence/community/models/__utils__/test.py
````python
class TestStatus(Enum)
⋮----
PENDING = "\033[90m[PENDING]"
SUCCESS = "\033[92m[SUCCESS]"
FAILURE = "\033[91m[FAILURE]"
class ConfigurationTracker
⋮----
def __init__(self)
def add_config(self, config: dict)
⋮----
config_id = f"{config['engine']}/{config['quantization']}"
⋮----
def update_status(self, config: dict, status: TestStatus, elapsed_time: float = 0.0)
def print_status_list(self)
def test_meta_information(model_class: AbstractUniversalModel)
⋮----
contract = model_class.contract()
compatibility = model_class.compatibility()
⋮----
def get_device_info()
⋮----
device_info = {
⋮----
total_memory = sum(torch.cuda.get_device_properties(i).total_memory for i in range(torch.cuda.device_count()))
⋮----
def get_valid_configurations(model_class: AbstractUniversalModel, device_info)
⋮----
compatibilities = model_class.compatibility()
configs_by_engine = {}
seen_pairs = set()
⋮----
config_id = f"{compat['engine']}/{compat['quantization']}"
⋮----
pair = (compat["engine"], compat["quantization"])
⋮----
valid_configs = []
max_configs = max(len(configs) for configs in configs_by_engine.values())
⋮----
memory = next(compat["memory"] for compat in compatibilities if compat["engine"] == config["engine"] and compat["quantization"] == config["quantization"])
⋮----
inference_config = {
⋮----
start_time = time.time()
model = model_class(**universal_model_config) if universal_model_config else model_class()
required_methods = [
⋮----
elapsed_time = time.time() - start_time
⋮----
def run_all_tests(model_class: AbstractUniversalModel, inference_config: dict | None = None)
⋮----
device_info = get_device_info()
⋮----
valid_configs = get_valid_configurations(model_class, device_info)
⋮----
tracker = ConfigurationTracker()
````

## File: universal_intelligence/community/tools/__utils__/test.py
````python
class TestStatus(Enum)
⋮----
PENDING = "\033[90m[PENDING]"
SUCCESS = "\033[92m[SUCCESS]"
FAILURE = "\033[91m[FAILURE]"
EXPECTED_FAILURE = "\033[93m[EXPECTED FAILURE]"
class TestExpectation
⋮----
def __init__(self, should_fail: bool = False, expected_error: str | type | None = None)
class MethodTracker
⋮----
def __init__(self)
def add_method(self, method_name: str, expectation: TestExpectation = None)
def update_status(self, method_name: str, status: TestStatus)
def print_status_list(self)
⋮----
expectation = self.expectations.get(method_name)
expected_str = " (Expected to fail)" if expectation and expectation.should_fail else ""
⋮----
def test_meta_information(tool_class: AbstractUniversalTool)
⋮----
contract = tool_class.contract()
requirements = tool_class.requirements()
⋮----
expectation = tracker.expectations.get(method_name) if tracker else None
⋮----
method = getattr(tool, method_name)
⋮----
def get_test_arguments(method_spec: dict) -> dict
⋮----
test_args = {}
⋮----
tool = tool_class(configuration=tool_config) if tool_config else tool_class()
contract = tool.contract()
methods = [method for method in contract["methods"] if method["name"] not in ["contract", "requirements"]]
⋮----
tracker = MethodTracker()
⋮----
expectation = expected_failures.get(method["name"]) if expected_failures else None
⋮----
test_args = get_test_arguments(method)
````

## File: universal_intelligence/community/tools/api_caller/__init__.py
````python
__all__ = ["UniversalTool"]
````

## File: universal_intelligence/community/tools/api_caller/test.py
````python

````

## File: universal_intelligence/community/tools/api_caller/tool.py
````python
class UniversalTool(AbstractUniversalTool)
⋮----
_contract: ClassVar[Contract] = {
_requirements: ClassVar[list[Requirement]] = []
⋮----
@classmethod
    def contract(cls) -> Contract
⋮----
@classmethod
    def requirements(cls) -> list[Requirement]
def __init__(self, configuration: dict | None = None, verbose: str = "DEFAULT") -> None
⋮----
current_time = time.time()
time_since_last_request = current_time - self._last_request_time
⋮----
request_headers = self._default_headers.copy()
⋮----
response = requests.request(
⋮----
data = response.json() if response.text else None
⋮----
data = {
````

## File: universal_intelligence/community/tools/default/__init__.py
````python
__all__ = ["UniversalTool"]
````

## File: universal_intelligence/community/tools/default/test.py
````python

````

## File: universal_intelligence/community/tools/mcp_client/__init__.py
````python
__all__ = ["UniversalTool"]
````

## File: universal_intelligence/community/tools/mcp_client/test.py
````python

````

## File: universal_intelligence/community/tools/mcp_client/tool.py
````python
class UniversalTool(AbstractUniversalTool)
⋮----
_contract: ClassVar[Contract] = {
_requirements: ClassVar[list[Requirement]] = [
def __init__(self, configuration: dict[str, Any] | None = None, verbose: str = "DEFAULT") -> None
⋮----
@classmethod
    def contract(cls) -> Contract
⋮----
@classmethod
    def requirements(cls) -> list[Requirement]
async def _initialize_session(self)
async def call_tool(self, tool_name: str, arguments: dict[str, Any] | None = None) -> tuple[str, dict]
async def list_prompts(self) -> tuple[list[str], dict]
async def get_prompt(self, prompt_name: str, arguments: dict[str, Any] | None = None) -> tuple[str, dict]
async def list_resources(self) -> tuple[list[str], dict]
async def list_tools(self) -> tuple[list[str], dict]
async def read_resource(self, resource_path: str) -> tuple[tuple[str, str], dict]
async def __aenter__(self)
async def __aexit__(self, exc_type, exc_val, exc_tb)
````

## File: universal_intelligence/community/tools/simple_error_generator/__init__.py
````python
__all__ = ["UniversalTool"]
````

## File: universal_intelligence/community/tools/simple_error_generator/test.py
````python

````

## File: universal_intelligence/community/tools/simple_error_generator/tool.py
````python
class UniversalTool(AbstractUniversalTool)
⋮----
_contract: ClassVar[Contract] = {
_requirements: ClassVar[list[Requirement]] = [
⋮----
@classmethod
    def contract(cls) -> Contract
⋮----
@classmethod
    def requirements(cls) -> list[Requirement]
def __init__(self, configuration: dict | None = None, verbose: str = "DEFAULT") -> None
def raise_error(self, text: str = "Something went wrong") -> tuple[str, dict]
````

## File: universal_intelligence/community/tools/simple_printer/__init__.py
````python
__all__ = ["UniversalTool"]
````

## File: universal_intelligence/community/tools/simple_printer/test.py
````python

````

## File: universal_intelligence/community/tools/simple_printer/tool.py
````python
class UniversalTool(AbstractUniversalTool)
⋮----
_contract: ClassVar[Contract] = {
_requirements: ClassVar[list[Requirement]] = [
⋮----
@classmethod
    def contract(cls) -> Contract
⋮----
@classmethod
    def requirements(cls) -> list[Requirement]
def __init__(self, configuration: dict | None = None, verbose: str = "DEFAULT") -> None
def print_text(self, text: str) -> tuple[str, dict]
````

## File: universal_intelligence/core/utils/types.py
````python
class Message(TypedDict)
⋮----
role: str
content: Any
class Schema(TypedDict, total=False)
⋮----
maxLength: int | None
pattern: str | None
minLength: int | None
nested: list["Argument"] | None
properties: dict[str, "Schema"] | None
items: Optional["Schema"]
class Argument(TypedDict)
⋮----
name: str
type: str
schema: Schema | None
description: str
required: bool
class Output(TypedDict)
class Method(TypedDict)
⋮----
arguments: list[Argument]
outputs: list[Output]
asynchronous: bool | None
class Contract(TypedDict)
⋮----
methods: list[Method]
class Requirement(TypedDict)
⋮----
schema: Schema
⋮----
class Compatibility(TypedDict)
⋮----
engine: str
quantization: str
devices: list[str]
memory: float
dependencies: list[str]
precision: int
class QuantizationSettings(TypedDict)
⋮----
default: str | None
min_precision: str | None
max_precision: str | None
````

## File: universal_intelligence/core/__init__.py
````python
__all__ = [
````

## File: universal_intelligence/core/universal_agent.py
````python
class AbstractUniversalAgent(ABC)
⋮----
@classmethod
@abstractmethod
    def contract(cls) -> Contract
⋮----
@classmethod
@abstractmethod
    def requirements(cls) -> list[Requirement]
⋮----
@classmethod
@abstractmethod
    def compatibility(cls) -> list[Compatibility]
⋮----
@abstractmethod
    def load(self) -> None
⋮----
@abstractmethod
    def unload(self) -> None
⋮----
@abstractmethod
    def reset(self) -> None
⋮----
@abstractmethod
    def loaded(self) -> bool
````

## File: universal_intelligence/core/universal_model.py
````python
class AbstractUniversalModel(ABC)
⋮----
@classmethod
@abstractmethod
    def contract(cls) -> Contract
⋮----
@classmethod
@abstractmethod
    def compatibility(cls) -> list[Compatibility]
⋮----
@abstractmethod
    def process(self, input: Any | list[Message] | None = None, context: list[Any] | None = None, configuration: dict | None = None, remember: bool = False, keep_alive: bool = False, stream: bool = False) -> tuple[Any, dict]
⋮----
@abstractmethod
    def load(self) -> None
⋮----
@abstractmethod
    def unload(self) -> None
⋮----
@abstractmethod
    def reset(self) -> None
⋮----
@abstractmethod
    def loaded(self) -> bool
⋮----
@abstractmethod
    def configuration(self) -> dict
````

## File: universal_intelligence/core/universal_tool.py
````python
class AbstractUniversalTool(ABC)
⋮----
@classmethod
@abstractmethod
    def contract(cls) -> Contract
⋮----
@classmethod
@abstractmethod
    def requirements(cls) -> list[Requirement]
⋮----
@abstractmethod
    def __init__(self, configuration: dict | None = None, verbose: bool | str = False) -> None
````

## File: universal_intelligence/www/community/__utils__/logger.ts
````typescript
export enum LogLevel {
  NONE = 'NONE',
  DEFAULT = 'DEFAULT',
  DEBUG = 'DEBUG'
}
export class Logger
⋮----
constructor(level: LogLevel = LogLevel.DEFAULT)
private shouldLog(): boolean
log(...args: any[]): void
info(...args: any[]): void
warn(...args: any[]): void
error(...args: any[]): void
debug(...args: any[]): void
setLevel(level: LogLevel): void
getLevel(): LogLevel
````

## File: universal_intelligence/www/community/agents/simple_agent/agent.ts
````typescript
import { AbstractUniversalModel } from "../../../core/UniversalModel"
import UniversalModel from "../../models/local/qwen2_5_3b_instruct/model"
import { Logger, LogLevel } from "./../../../community/__utils__/logger"
import { Contract, Compatibility, Requirement, Message } from "./../../../core/types"
import { AbstractUniversalAgent } from "./../../../core/UniversalAgent"
import { AbstractUniversalTool } from "./../../../core/UniversalTool"
⋮----
export default class UniversalAgent extends AbstractUniversalAgent
⋮----
public static contract(): Contract
public static compatibility(): Compatibility[]
public static requirements(): Requirement[]
contract(): Contract
compatibility(): Compatibility[]
requirements(): Requirement[]
⋮----
constructor(
    payload?: {
      credentials?: string | Record<string, any>,
      model?: AbstractUniversalModel,
      expandTools?: AbstractUniversalTool[],
      expandTeam?: AbstractUniversalAgent[],
      configuration?: Record<string, any>,
      verbose?: boolean | string
    } | undefined
)
private async _planDependencyCalls(
    query: string,
    extraTools: AbstractUniversalTool[] | null = null,
    extraTeam: AbstractUniversalAgent[] | null = null
): Promise<any[]>
private async _executeDependencyCalls(
    plannedCalls: Array<Record<string, any>>,
    extraTools: AbstractUniversalTool[] | null = null,
    extraTeam: AbstractUniversalAgent[] | null = null
): Promise<Array<Record<string, any>>>
async process(
    input: string | Message[],
    payload?: {
      context?: any[],
      configuration?: Record<string, any>,
      remember?: boolean,
      stream?: boolean,
      extraTools?: AbstractUniversalTool[],
      extraTeam?: AbstractUniversalAgent[],
      keepAlive?: boolean
} | undefined): Promise<[any, Record<string, any>]>
async load(): Promise<void>
async loaded(): Promise<boolean>
async unload(): Promise<void>
async reset(): Promise<void>
async connect(
    payload: {
      tools?: AbstractUniversalTool[],
      agents?: AbstractUniversalAgent[]
    }
): Promise<void>
async disconnect(
    payload: {
      tools?: AbstractUniversalTool[],
      agents?: AbstractUniversalAgent[]
    }
): Promise<void>
````

## File: universal_intelligence/www/community/agents/simple_agent/index.ts
````typescript
import UniversalAgent from "./agent"
````

## File: universal_intelligence/www/community/agents/index.ts
````typescript
import { UniversalAgent as SimpleAgent } from "./simple_agent"
````

## File: universal_intelligence/www/community/models/__utils__/mixins/hf_text_to_text/interface.ts
````typescript
import { MLCEngine } from "@mlc-ai/web-llm"
import { Logger, LogLevel } from '../../../../../community/__utils__/logger'
import { QuantizationSettings , Message, Contract, Compatibility } from '../../../../../core/types'
import { AbstractUniversalModel } from '../../../../../core/UniversalModel'
import { extractPrecisionFromDescriptor } from './meta'
import { InferenceConfiguration, ModelConfiguration, ProcessorConfiguration, Sources, QuantizationConfig } from './types'
export abstract class UniversalModelMixin extends AbstractUniversalModel
⋮----
private async _getAvailableMemory(deviceType: string = 'webgpu'): Promise<number>
constructor(
    interfaceConfig: {
      name: string;
      sources: Sources;
      model_configuration: ModelConfiguration;
      inference_configuration: InferenceConfiguration;
      processor_configuration: ProcessorConfiguration;
    },
    payload?: {
      engine?: string | string[],
      quantization?: string | string[] | QuantizationSettings,
      maxMemoryAllocation?: number,
      configuration?: Record<string, any>,
      verbose?: boolean | string,
      credentials?: string | Record<string, any>
    } | undefined
)
⋮----
// Start async initialization
⋮----
async ready(): Promise<void>
private async _initializeAsync(
    engine: string | string[] | null | undefined,
    quantization: string | string[] | QuantizationSettings | null | undefined,
    maxMemoryAllocation: number | null | undefined
): Promise<void>
⋮----
// Detect device type
⋮----
// For now we only support WebGPU, but the structure is ready for future devices
⋮----
// Get device-specific sources
⋮----
async loaded(): Promise<boolean>
async reset(): Promise<void>
private _translateModelConfig(config: any =
private _translateInferenceConfig(config: any =
async load(): Promise<void>
⋮----
const initProgressCallback = (progress: any) : void =>
⋮----
async unload(): Promise<void>
async process(input: string | Message[], payload? : {
    context?: any[],
    configuration?: Record<string, any>,
    remember?: boolean,
    keepAlive?: boolean,
    stream?: boolean
}): Promise<[string, any]>
⋮----
// Handle non-streaming response
⋮----
// Update history if remember is true
⋮----
async configuration(): Promise<any>
⋮----
// Wait for model to be ready
⋮----
static contract(): Contract
static compatibility(): Compatibility[]
abstract contract(): Contract;
abstract compatibility(): Compatibility[];
````

## File: universal_intelligence/www/community/models/__utils__/mixins/hf_text_to_text/meta.ts
````typescript
import { Contract, Compatibility, Output } from '../../../../../core/types'
import { SourcesConfig, Sources, EngineConfig, QuantizationConfig } from './types'
export function extractPrecisionFromDescriptor(precisionDescriptor: string): number
export function generateSourcesFromConfig(data: SourcesConfig): Sources
export function generateStandardContract(name: string, description: string): Contract
export function generateStandardCompatibility(sources: Sources): Compatibility[]
````

## File: universal_intelligence/www/community/models/__utils__/mixins/hf_text_to_text/types.ts
````typescript
export interface EngineConfig {
    name: string;
    model_id: string;
    model_file?: string | null;
    is_default: boolean;
}
export interface QuantizationConfig {
    available_engines: EngineConfig[];
    is_default: boolean;
    memory: number;
    precision: number;
}
export type Sources = {
  webgpu: Record<string, QuantizationConfig>
};
export type ModelConfiguration = {
    [key: string]: {
        [key: string]: any;
    };
};
export type InferenceConfiguration = {
    [key: string]: {
        [key: string]: any;
    };
};
export interface InputProcessorConfig {
    tokenizer?: {
        [key: string]: any;
    };
    chat_template?: {
        [key: string]: any;
    };
}
export interface ProcessorConfig {
    input?: InputProcessorConfig;
    output?: {
        [key: string]: any;
    };
}
export type ProcessorConfiguration = {
    [K in 'webllm']: ProcessorConfig;
};
export interface ChatTemplate {
    system_start: string;
    system_end: string;
    user_start: string;
    user_end: string;
    assistant_start: string;
    assistant_end: string;
    default_system_message: string;
    generation_prompt: string;
}
export type PrecisionType = '2bit' | '3bit' | '4bit' | '5bit' | '6bit' | '8bit' | '16bit' | '32bit';
export interface ModelInfo {
  name: string;
  default_quantization: {
    webgpu?: string;
  };
}
export interface QuantizationInfo {
  engine: string;
  model_id: string;
  model_file?: string;
  model_size: number;
  supported_devices: string[];
}
export interface SourcesConfig{
  model_info: ModelInfo;
  quantizations: Record<string, QuantizationInfo>;
}
⋮----
interface Navigator {
    gpu?: {
      requestAdapter: () => GPUAdapter | null;
    };
  }
⋮----
interface GPUAdapter {
  limits: {
    maxBufferSize: number;
    maxStorageBufferBindingSize: number;
  };
}
````

## File: universal_intelligence/www/community/models/__utils__/mixins/openrouter_text_to_text/interface.ts
````typescript
import { Logger, LogLevel } from '../../../../../community/__utils__/logger'
import { Message, Contract, Compatibility } from '../../../../../core/types'
import { AbstractUniversalModel } from '../../../../../core/UniversalModel'
import { InferenceConfiguration } from './types'
export abstract class UniversalModelMixin extends AbstractUniversalModel
⋮----
constructor(
        interfaceConfig: { name: string; inference_configuration: InferenceConfiguration },
        payload?: {
            credentials?: string | { api_key: string; http_referrer?: string; x_title?: string },
            verbose?: boolean | string
        } | undefined
)
private _translateGenerationConfig(configuration?: Record<string, any>): Record<string, any>
async process(
        input: string | Message[],
        payload?: {
            context?: any[],
            configuration?: Record<string, any>,
            remember?: boolean
        } | undefined
): Promise<[any, Record<string, any>]>
⋮----
// Update history if remember is True
⋮----
async load(): Promise<void>
async unload(): Promise<void>
async loaded(): Promise<boolean>
async configuration(): Promise<Record<string, any>>
async reset(): Promise<void>
async ready(): Promise<void>
static contract(): Contract
static compatibility(): Compatibility[]
abstract contract(): Contract;
abstract compatibility(): Compatibility[];
````

## File: universal_intelligence/www/community/models/__utils__/mixins/openrouter_text_to_text/meta.ts
````typescript
import { Compatibility, Contract } from '../../../../../core/types'
export function generateStandardContract(name: string, description: string): Contract
export function generateStandardCompatibility(): Compatibility[]
````

## File: universal_intelligence/www/community/models/__utils__/mixins/openrouter_text_to_text/types.ts
````typescript
export type ModelConfiguration = {
    [key: string]: {
        [key: string]: any;
    };
};
export type InferenceConfiguration = {
    [key: string]: {
        [key: string]: any;
    };
};
````

## File: universal_intelligence/www/community/models/index.ts
````typescript
import local from './local'
import remote from './remote'
````

## File: universal_intelligence/www/community/tools/api_caller/index.ts
````typescript
import { UniversalTool } from './tool'
````

## File: universal_intelligence/www/community/tools/api_caller/tool.ts
````typescript
import { Contract, Requirement } from '../../../core/types'
import { AbstractUniversalTool } from '../../../core/UniversalTool'
import { Logger, LogLevel } from './../../../community/__utils__/logger'
export class UniversalTool extends AbstractUniversalTool
⋮----
static contract(): Contract
static requirements(): Requirement[]
contract(): Contract
requirements(): Requirement[]
constructor(configuration?: Record<string, any>)
async callApi({
    url,
    method = "GET",
    body,
    params,
    headers,
    timeout
  }: {
    url: string,
    method?: string,
    body?: Record<string, any>,
    params?: Record<string, any>,
    headers?: Record<string, string>,
    timeout?: number
}): Promise<[Record<string, any>, Record<string, any>]>
````

## File: universal_intelligence/www/community/tools/simple_error_generator/index.ts
````typescript
import { UniversalTool } from './tool'
````

## File: universal_intelligence/www/community/tools/simple_error_generator/tool.ts
````typescript
import { Contract, Requirement } from '../../../core/types'
import { AbstractUniversalTool } from '../../../core/UniversalTool'
import { Logger, LogLevel } from './../../../community/__utils__/logger'
export class UniversalTool extends AbstractUniversalTool
⋮----
static contract(): Contract
static requirements(): Requirement[]
contract(): Contract
requirements(): Requirement[]
constructor(configuration?: Record<string, any>)
raiseError(
````

## File: universal_intelligence/www/community/tools/simple_printer/index.ts
````typescript
import { UniversalTool } from './tool'
````

## File: universal_intelligence/www/community/tools/simple_printer/tool.ts
````typescript
import { Contract, Requirement } from '../../../core/types'
import { AbstractUniversalTool } from '../../../core/UniversalTool'
import { Logger, LogLevel } from './../../../community/__utils__/logger'
export class UniversalTool extends AbstractUniversalTool
⋮----
static contract(): Contract
static requirements(): Requirement[]
contract(): Contract
requirements(): Requirement[]
constructor(configuration?: Record<string, any>)
printText(
````

## File: universal_intelligence/www/community/tools/index.ts
````typescript
import APICaller from './api_caller'
import SimpleErrorGenerator from './simple_error_generator'
import SimplePrinter from './simple_printer'
````

## File: universal_intelligence/www/community/index.ts
````typescript
import agents from './agents'
import models from './models'
import tools from './tools'
````

## File: universal_intelligence/www/core/index.ts
````typescript
import { AbstractUniversalAgent } from './UniversalAgent'
import { AbstractUniversalModel } from './UniversalModel'
import { AbstractUniversalTool } from './UniversalTool'
````

## File: universal_intelligence/www/core/types.ts
````typescript
export interface Message {
  role: string;
  content: any;
}
export interface Schema {
  maxLength?: number;
  pattern?: string;
  minLength?: number;
  nested?: Argument[];
  properties?: Record<string, Schema>;
  items?: Schema;
  oneOf?: any[];
}
export interface Argument {
  name: string;
  type: string;
  schema?: Schema;
  description: string;
  required: boolean;
}
export interface Output {
  type: string;
  description: string;
  required: boolean;
  schema?: Schema;
}
export interface Method {
  name: string;
  description: string;
  arguments: Argument[];
  outputs: Output[];
  asynchronous?: boolean;
}
export interface Contract {
  name: string;
  description: string;
  methods: Method[];
}
export interface Requirement {
  name: string;
  type: string;
  schema: Schema;
  description: string;
  required: boolean;
}
export interface Compatibility {
  engine: string;
  quantization: string;
  devices: string[];
  memory: number;
  dependencies: string[];
  precision: number;
}
export interface QuantizationSettings {
  default?: string;
  minPrecision?: string;
  maxPrecision?: string;
}
````

## File: universal_intelligence/www/core/UniversalAgent.ts
````typescript
import { Contract, Requirement, Compatibility, Message } from './types'
import { AbstractUniversalModel } from './UniversalModel'
import { AbstractUniversalTool } from './UniversalTool'
export abstract class AbstractUniversalAgent
⋮----
static contract(): Contract
static requirements(): Requirement[]
static compatibility(): Compatibility[]
abstract contract(): Contract;
abstract requirements(): Requirement[];
abstract compatibility(): Compatibility[];
constructor(payload: {
    credentials?: string | Record<string, any>,
    model?: AbstractUniversalModel,
    expandTools?: AbstractUniversalTool[],
    expandTeam?: AbstractUniversalAgent[],
    configuration?: Record<string, any>,
    verbose?: boolean | string
} | undefined)
abstract process(input: any | Message[], payload: {
    context?: any[],
    configuration?: Record<string, any>,
    remember?: boolean,
    stream?: boolean,
    extraTools?: AbstractUniversalTool[],
    extraTeam?: AbstractUniversalAgent[],
    keepAlive?: boolean
  } | undefined): Promise<[any | null, Record<string, any>]>;
abstract load(): Promise<void>;
abstract unload(): Promise<void>;
abstract reset(): Promise<void>;
abstract loaded(): Promise<boolean>;
abstract connect(payload: {
    tools?: AbstractUniversalTool[],
    agents?: AbstractUniversalAgent[]
  }): Promise<void>;
abstract disconnect(payload: {
    tools?: AbstractUniversalTool[],
    agents?: AbstractUniversalAgent[]
  }): Promise<void>;
````

## File: universal_intelligence/www/core/UniversalModel.ts
````typescript
import { Contract, Compatibility, Message, QuantizationSettings } from './types'
export abstract class AbstractUniversalModel
⋮----
static contract(): Contract
static compatibility(): Compatibility[]
abstract contract(): Contract;
abstract compatibility(): Compatibility[];
constructor(payload: {
    credentials?: string | Record<string, any>,
    engine?: string | string[],
    quantization?: string | string[] | QuantizationSettings,
    maxMemoryAllocation?: number,
    configuration?: Record<string, any>,
    verbose?: boolean | string
} | undefined)
abstract ready(): Promise<void>;
abstract process(input: any | Message[], payload?: {
    context?: any[],
    configuration?: Record<string, any>,
    remember?: boolean,
    keepAlive?: boolean,
    stream?: boolean
  } | undefined): Promise<[any | null, Record<string, any>]>;
abstract load(): Promise<void>;
abstract unload(): Promise<void>;
abstract reset(): Promise<void>;
abstract loaded(): Promise<boolean>;
abstract configuration(): Promise<Record<string, any>>;
````

## File: universal_intelligence/www/core/UniversalTool.ts
````typescript
import { Contract, Requirement } from './types'
export abstract class AbstractUniversalTool
⋮----
static contract(): Contract
static requirements(): Requirement[]
abstract contract(): Contract;
abstract requirements(): Requirement[];
constructor(configuration?: Record<string, any> | undefined)
````

## File: universal_intelligence/www/index.ts
````typescript
import community from './community'
import core from './core'
````

## File: universal_intelligence/__init__.py
````python
__all__ = ["core", "community", "Model", "Tool", "Agent", "OtherAgent", "RemoteModel"]
````

## File: .gitignore
````
.DS_Store
__pycache__
.venv
.env
playground.py
.sources.md
.sources.yaml
.sources.yml
.configurations.md
.configurations.yaml
.configurations.yml
.instructions.md
.instructions.yaml
.instructions.json
.example.sources.yaml
.example.instructions.yaml
__unreleased__
.localcmds
.localcmds.md
dist
dist_past
build
*.egg-info/
*.dist-info/
*.whl
*.tar.gz
*.zip
*.tar.bz2
*.tar.xz
requirements-release.txt
.ruff_cache
test_imports.py
=3.*
node_modules
webdist
distweb
.cursorignore
.private*
````

## File: .nvmrc
````
22.12.0
````

## File: .pre-commit-config.yaml
````yaml
repos:
-   repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
    -   id: ruff
        args: [--fix]
        types: [python]
-   repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
    -   id: black
        types: [python]
-   repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
    -   id: isort
        types: [python]
````

## File: eslint.config.js
````javascript
tsconfigRootDir: process.cwd(),
````

## File: LICENSE
````
Copyright 2025 Bluera Inc. | All rights reserved.

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
````

## File: package.json
````json
{
  "name": "universalintelligence",
  "version": "1.0.0",
  "description": "Universal Intelligence Protocols and Community Components",
  "main": "distweb/index.js",
  "type": "module",
  "scripts": {
    "build": "tsc && vite build",
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix"
  },
  "dependencies": {
    "@mlc-ai/web-llm": "^0.2.0",
    "@types/js-yaml": "^4.0.9",
    "js-yaml": "^4.1.0"
  },
  "devDependencies": {
    "@eslint/js": "^9.24.0",
    "@typescript-eslint/eslint-plugin": "^8.30.1",
    "@typescript-eslint/parser": "^8.30.1",
    "eslint": "^9.24.0",
    "eslint-plugin-import": "^2.31.0",
    "globals": "^16.0.0",
    "typescript": "^5.0.0",
    "vite": "^5.1.0"
  }
}
````

## File: pyproject.toml
````toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "universal-intelligence"
version = "1.0.0"
authors = [
    { name = "Bluera Inc.", email = "bluera@bluera.ai" },
]
description = "Universal Intelligence"
readme = "README.md"
requires-python = ">=3.10,<3.13"
license = { file = "LICENSE" }
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
]

[project.urls]
"Homepage" = "https://github.com/blueraai/universal-intelligence"
"Bug Tracker" = "https://github.com/blueraai/universal-intelligence/issues"

[project.optional-dependencies]
community = [
    "torch",
    "transformers",
    "huggingface_hub",
    "psutil",
    "accelerate",
    "protobuf",
    "llama-cpp-python"
]
mps = [
    "mlx",
    "mlx-lm",
]
cuda = [
    "llama-cpp-python",
    "auto-gptq",
    "optimum",
    "autoawq",
    "bitsandbytes",
    "accelerate",
]
mcp = [
    "mcp"
]
dev = [
    "ruff>=0.3.0",
    "black>=24.2.0",
    "isort>=5.13.2",
]

[tool.hatch.build.targets.wheel]
packages = ["universal_intelligence"]

[tool.hatch.metadata]
allow-direct-references = true

[tool.ruff]
line-length = 300
target-version = "py310"
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "C",   # flake8-comprehensions
    "B",   # flake8-bugbear
    "UP",  # pyupgrade
    "N",   # pep8-naming
    "RUF", # ruff-specific rules
]
ignore = ["B026", "E501", "RUF001"]

[tool.ruff.mccabe]
max-complexity = 50

[tool.ruff.isort]
known-first-party = ["universal_intelligence"]

[tool.black]
line-length = 300
target-version = ["py310"]
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
line_length = 300
````

## File: README.md
````markdown
![Universal Intelligence](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//universal-intelligence-banner-rsm.png)

<p align="center">
    <a href="https://github.com/blueraai/universal-intelligence/releases"><img alt="GitHub Release" src="https://img.shields.io/github/release/blueraai/universal-intelligence.svg?color=1c4afe"></a>
    <a href="https://github.com/blueraai/universal-intelligence/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/blueraai/universal-intelligence.svg?color=00bf48"></a>
    <a href="https://discord.gg/7g9SrEc5yT"><img alt="Discord" src="https://img.shields.io/badge/Join-Discord-7289DA?logo=discord&logoColor=white&color=4911ff"></a>
</p>

> ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-python-16.png) This page aims to document **Python** protocols and usage (e.g. cloud, desktop).
>
> Looking for [**Javascript/Typescript instructions**](https://github.com/blueraai/universal-intelligence/blob/main/README_WEB.md)?

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

UIN is a protocol aiming to standardize, simplify and modularize these fundamental AI components (ie. models, tools and agents), for them to be accessible to any developer, and distributed on any platform.

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
# Choose relevant install for your device
pip install "universal-intelligence[community,mps]" # Apple
pip install "universal-intelligence[community,cuda]" # NVIDIA

# Log into Hugging Face CLI so you can download models
huggingface-cli login
```

#### 🧠 Simple model

```python
from universal_intelligence import Model # (or in the cloud) RemoteModel

model = Model() # (or in the cloud) RemoteModel(credentials='openrouter-api-key')
result, logs = model.process("Hello, how are you?")
```

> Models may run locally or in the cloud.
>
> See *Documentation>Community Components>Remote Models* for details.

Preview:

- *Local Model*

![uin-model-demo](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//model-demo.png)

- *Remote Model (cloud-based)*

![ui-remote-model-demo](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//remotemodel-demo.png)

#### 🔧 Simple tool

```python
from universal_intelligence import Tool

tool = Tool()
result, logs = tool.print_text("This needs to be printed")
```

Preview:

![uin-tool-demo](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//tool-demo.png)

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

Preview:

![uin-agent-demo](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//simple-agent-demo.png)

### Playground

A ready-made playground is available to help familiarize yourself with the protocols and components.

```sh
python -m playground.example
```

## Documentation

<details>
<summary><strong style="display: inline; cursor: pointer; margin: 0; padding: 0;">Protocol Specifications</strong></summary>

## Protocol Specifications

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
  credentials='<token>', # (or) object containing credentials eg. { id: 'example', passkey: 'example' }
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
  },
  verbose=True # or string describing log level
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

tool = Tool(
  # configuration={ "any": "configuration" },
  # verbose=False
)
result, logs = tool.example_task(example_argument=data)
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
  credentials='<token>', # (or) object containing credentials eg. { id: 'example', passkey: 'example' }
  model=Model(), # see Universal Model API for customizations
  expand_tools=[Tool()], # see Universal Tool API for customizations
  expand_team=[OtherAgent()],  # see Universal Agent API for customizations
  configuration={
    # agent configuration (eg. guardrails, behavior, tracing)
  },
  verbose=True # or string describing log level
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
agent.connect(tools=[tool], agents=[other_agent]) # connects additionnal tools/agents
agent.disconnect(tools=[tool], agents=[other_agent]) # disconnects tools/agents

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
| `__init__` | • `credentials: str \| Dict = None`: Authentication information (e.g. authentication token (or) object containing credentials such as  *{ id: 'example', passkey: 'example' }*)<br>• `engine: str \| List[str] = None`: Engine used (e.g., 'transformers', 'llama.cpp', (or) ordered by priority *['transformers', 'llama.cpp']*). Prefer setting quantizations over engines for broader portability.<br>• `quantization: str \| List[str] \| QuantizationSettings = None`: Quantization specification (e.g., *'Q4_K_M'*, (or) ordered by priority *['Q4_K_M', 'Q8_0']* (or) auto in range *{'default': 'Q4_K_M', 'min_precision': '4bit', 'max_precision': '8bit'}*)<br>• `max_memory_allocation: float = None`: Maximum allowed memory allocation in percentage<br>• `configuration: Dict = None`: Configuration for model and processor settings<br>• `verbose: bool \| str = "DEFAULT"`: Enable/Disable logs, or set a specific log level | `None` | Initialize a Universal Model |
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
| `__init__` | • `credentials: str \| Dict = None`: Authentication information (e.g. authentication token (or) object containing credentials such as  *{ id: 'example', passkey: 'example' }*)<br>• `model: UniversalModel = None`: Model powering this agent<br>• `expand_tools: List[UniversalTool] = None`: Tools to connect<br>• `expand_team: List[UniversalAgent] = None`: Other agents to connect<br>• `configuration: Dict = None`: Agent configuration (eg. guardrails, behavior, tracing)<br>• `verbose: bool \| str = "DEFAULT"`: Enable/Disable logs, or set a specific log level | `None` | Initialize a Universal Agent |
| `process` | • `input: Any \| List[Message]`: Input or input messages<br>• `context: List[Any] = None`: Context items (multimodal)<br>• `configuration: Dict = None`: Runtime configuration<br>• `remember: bool = False`: Remember this interaction. Please be mindful of the available context length of the underlaying model.<br>• `stream: bool = False`: Stream output asynchronously<br>• `extra_tools: List[UniversalTool] = None`: Additional tools<br>• `extra_team: List[UniversalAgent] = None`: Additional agents<br>• `keep_alive: bool = None`: Keep underlaying model loaded for faster consecutive interactions | `Tuple[Any, Dict]` | Process input through the agent and return output and logs. The output is typically the agent's response and the logs contain processing metadata including tool/agent calls |
| `load` | None | `None` | Load agent's model into memory |
| `loaded` | None | `bool` | Check if the agent's model is currently loaded in memory |
| `unload` | None | `None` | Unload agent's model from memory |
| `reset` | None | `None` | Reset agent's chat history |
| `connect` | • `tools: List[UniversalTool] = None`: Tools to connect<br>• `agents: List[UniversalAgent] = None`: Agents to connect | `None` | Connect additional tools and agents |
| `disconnect` | • `tools: List[UniversalTool] = None`: Tools to disconnect<br>• `agents: List[UniversalAgent] = None`: Agents to disconnect | `None` | Disconnect tools and agents |
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

</details>

<details>
<summary><strong style="display: inline; cursor: pointer; margin: 0; padding: 0;">Community Components</strong></summary>

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

#### Local Models

```python
from universal_intelligence.community.models.local.default import UniversalModel as Model

model = Model()
output, logs = model.process("How are you doing today?")
```

> View [Universal Intelligence Protocols](https://github.com/blueraai/universal-intelligence/blob/main/README.md) for additional information.

#### Remote Models

```python
from universal_intelligence.community.models.remote.default import UniversalModel as Model

model = Model(credentials='your-openrouter-api-key-here')
output, logs = model.process("How are you doing today?")
```

> View [Universal Intelligence Protocols](https://github.com/blueraai/universal-intelligence/blob/main/README.md) for additional information.

#### Tools

```python
from universal_intelligence.community.tools.simple_printer import UniversalTool as Tool

tool = Tool()
result, logs = tool.print_text("This needs to be printed")
```

> View [Universal Intelligence Protocols](https://github.com/blueraai/universal-intelligence/blob/main/README.md) for additional information.

#### Agents

```python
from universal_intelligence.community.agents.default import UniversalAgent as Agent

agent = Agent(
  # model=Model(),                  # customize or share 🧠 across [🤖,🤖,🤖,..]
  # expand_tools=[Tool()],          # expand 🔧 set
  # expand_team=[OtherAgent()]      # expand 🤖 team
)
result, logs = agent.process("Please print 'Hello World' to the console", extra_tools=[Tool()])
```

> View [Universal Intelligence Protocols](https://github.com/blueraai/universal-intelligence/blob/main/README.md) for additional information.

### Supported Components

#### Models

##### Local Models

> Import path: `universal_intelligence.community.models.local.<import>`
>
> (eg. *universal_intelligence.community.models.local.default*)

| I/O | Name | Import | Description | Supported Configurations |
|------|------|------|-------------|-----------|
| Text/Text | *Qwen2.5-7B-Instruct* (default)| `default`<br> or `qwen2_5_7b_instruct` | Small powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_7b_instruct/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | *Qwen2.5-32B-Instruct* | `qwen2_5_32b_instruct` | Large powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_32b_instruct/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | *Qwen2.5-14B-Instruct* | `qwen2_5_14b_instruct` | Medium powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_14b_instruct/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | *Qwen2.5-14B-Instruct-1M* | `qwen2_5_14b_instruct_1m` | Medium powerful model with 1M context by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_14b_instruct_1m/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | *Qwen2.5-7B-Instruct-1M* | `qwen2_5_7b_instruct_1m` | Small powerful model with 1M context by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_7b_instruct_1m/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | *Qwen2.5-3B-Instruct* | `qwen2_5_3b_instruct` | Compact powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_3b_instruct/sources.yaml)<br><br>Default:<br>`cuda:BNB_4:transformers`<br>`mps:MLX_4:mlx`<br>`cpu:Q4_K_M:llama.cpp` |
| Text/Text | *Qwen2.5-1.5B-Instruct* | `qwen2_5_1d5b_instruct` | Ultra-compact powerful model by Alibaba Cloud |  [Supported Configurations](https://github.com/blueraai/universal-intelligence/blob/main/universal_intelligence/community/models/qwen2_5_1d5b_instruct/sources.yaml)<br><br>Default:<br>`cuda:bfloat16:transformers`<br>`mps:MLX_8:mlx`<br>`cpu:Q4_K_M:llama.cpp` |

##### Remote Models

> Import path: `universal_intelligence.community.models.remote.<import>`
>
> (eg. *universal_intelligence.community.models.remote.default*)

| I/O | Name | Import | Description | Provider |
|------|------|------|-------------|-----------|
| Text/Text | *openrouter/auto* | `default` (default) | Your prompt will be processed by a meta-model and routed to one of dozens of models (see below), optimizing for the best possible output. To see which model was used, visit [Activity](/activity), or read the `model` attribute of the response. Your response will be priced at the same rate as the routed model. The meta-model is powered by [Not Diamond](https://docs.notdiamond.ai/docs/how-not-diamond-works). Learn more in our [docs](/docs/model-routing). Requests will be routed to the following models:- [openai/gpt-4o-2024-08-06](/openai/gpt-4o-2024-08-06)- [openai/gpt-4o-2024-05-13](/openai/gpt-4o-2024-05-13)- [openai/gpt-4o-mini-2024-07-18](/openai/gpt-4o-mini-2024-07-18)- [openai/chatgpt-4o-latest](/openai/chatgpt-4o-latest)- [openai/o1-preview-2024-09-12](/openai/o1-preview-2024-09-12)- [openai/o1-mini-2024-09-12](/openai/o1-mini-2024-09-12)- [anthropic/claude-3.5-sonnet](/anthropic/claude-3.5-sonnet)- [anthropic/claude-3.5-haiku](/anthropic/claude-3.5-haiku)- [anthropic/claude-3-opus](/anthropic/claude-3-opus)- [anthropic/claude-2.1](/anthropic/claude-2.1)- [google/gemini-pro-1.5](/google/gemini-pro-1.5)- [google/gemini-flash-1.5](/google/gemini-flash-1.5)- [mistralai/mistral-large-2407](/mistralai/mistral-large-2407)- [mistralai/mistral-nemo](/mistralai/mistral-nemo)- [deepseek/deepseek-r1](/deepseek/deepseek-r1)- [meta-llama/llama-3.1-70b-instruct](/meta-llama/llama-3.1-70b-instruct)- [meta-llama/llama-3.1-405b-instruct](/meta-llama/llama-3.1-405b-instruct)- [mistralai/mixtral-8x22b-instruct](/mistralai/mixtral-8x22b-instruct)- [cohere/command-r-plus](/cohere/command-r-plus)- [cohere/command-r](/cohere/command-r) |  `openrouter` |

#### Tools

> Import path: `universal_intelligence.community.tools.<import>`
>
> (eg. *universal_intelligence.community.tools.mcp_client*)

| Name | Import | Description | Configuration Requirements |
|------|------|-------------|-----------|
| *Simple Printer* | `simple_printer` | Prints a given text to the console | `prefix: Optional[str]`: Optional prefix for log messages |
| *Simple Error Generator* | `simple_error_generator` | Raises an error with optional custom message | `prefix: Optional[str]`: Optional prefix for error messages |
| *MCP Client* | `mcp_client` | Calls tools on a remote MCP server and manages server communication | `server_command: str`: Command to execute the MCP server<br>`server_args: Optional[List[str]]`: Command line arguments for the MCP server<br>`server_env: Optional[Dict[str, str]]`: Environment variables for the MCP server |
| *API Caller* | `api_caller` | Makes HTTP requests to configured API endpoints | `base_url: str`: Base URL for the API<br>`default_headers: Optional[Dict[str, str]]`: Default headers to include in every request<br>`timeout: Optional[int]`: Request timeout in seconds |

#### Agents

> Import path: `universal_intelligence.community.agents.<import>`
>
> (eg. *universal_intelligence.community.agents.default*)


| I/O | Name | Import | Description | Default Model | Default Tools | Default Team |
|------|------|------|-------------|-----------|-----------|-----------|
| Text/Text | *Simple Agent* (default)| `default`<br> or `simple_agent` | Simple Agent which can use provided Tools and Agents to complete a task |  `Qwen2.5-7B-Instruct`<br><br>`cuda:Q4_K_M:llama.cpp`<br>`mps:Q4_K_M:llama.cpp`<br>`cpu:Q4_K_M:llama.cpp` | None | None |

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

</details>

## Cross-Platform Support

![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-python-16.png) ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-javascript-16.png) `Universal Intelligence` protocols and components can be used across **all platforms** (cloud, desktop, web, mobile).

- ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-python-16.png) [How to use natively with `python` (cloud, desktop)](https://github.com/blueraai/universal-intelligence/blob/main/README.md)
- ![lng_icon](https://fasplnlepuuumfjocrsu.supabase.co/storage/v1/object/public/web-assets//icons8-javascript-16.png) [How to use on the web, or in web-native apps, with `javascript/typescript` (cloud, desktop, web, mobile)](https://github.com/blueraai/universal-intelligence/blob/main/README_WEB.md)
````

## File: requirements-community.txt
````
# Community Components Dependencies
torch
transformers
huggingface_hub
psutil
accelerate
protobuf
llama-cpp-python
````

## File: requirements-cuda.txt
````
# CUDA device dependencies (NVIDIA GPUs)
auto-gptq
optimum
autoawq
bitsandbytes
accelerate
````

## File: requirements-dev.txt
````
ruff
black
isort
````

## File: requirements-mcp.txt
````
mcp
````

## File: requirements-mps.txt
````
# MPS device dependencies (Apple Silicon)
mlx
mlx-lm 
accelerate
````

## File: requirements.txt
````
# Abstract Classes/Types Dependencies
# N/A

# For optional dependencies, use the appropriate requirements file:
# - requirements-community.txt for community components
# - requirements-mlx.txt for MPS device optimizations (Apple Silicon)
# - requirements-cuda.txt for CUDA device optimizations (NVIDIA GPUs)
# - requirements-gemma.txt for Gemma model support
# - requirements-mpc.txt for MPC tool support
````

## File: tsconfig.json
````json
{
  "compilerOptions": {
    "target": "es2019",
    "module": "esnext",
    "moduleResolution": "bundler",
    "outDir": "./distweb",
    "rootDir": ".",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "noImplicitAny": false,
    "noEmit": false,
    "emitDeclarationOnly": false,
    "resolveJsonModule": true,
    "allowSyntheticDefaultImports": true,
    "declaration": true,
    "sourceMap": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["universal_intelligence/www/*"]
    }
  },
  "include": ["universal_intelligence/www/**/*.ts", "vite.config.ts"],
  "exclude": ["node_modules"]
}
````

## File: vite.config.ts
````typescript
import path from 'path'
import { defineConfig } from 'vite'
````

## File: README_WEB.md
````markdown
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
````
