// Initialize Pino logger
import pino from 'pino';

const log = pino({
    level: 'debug',
    browser: {
        serialize: true,
        asObject: false,
        transmit: {
            send: function (level, logEvent) {
                const msg = logEvent.messages.join(' ');
                const levelColors = {
                    10: '\x1b[90m', // trace - gray
                    20: '\x1b[36m', // debug - cyan
                    30: '\x1b[32m', // info - green
                    40: '\x1b[33m', // warn - yellow
                    50: '\x1b[31m', // error - red
                    60: '\x1b[35m'  // fatal - magenta
                };
                const levelNames = {
                    10: 'TRACE',
                    20: 'DEBUG',
                    30: 'INFO',
                    40: 'WARN',
                    50: 'ERROR',
                    60: 'FATAL'
                };
                const color = levelColors[logEvent.level] || '';
                const reset = '\x1b[0m';
                const timestamp = new Date().toISOString();
                console.log(`${color}[${timestamp}] ${levelNames[logEvent.level]}${reset} ${msg}`);
            }
        }
    }
});

log.info('app-web.js', 'initializing');

// Create a logger for custom-blocks.js (which can't import modules)
window.customBlocksLogger = pino({
    level: 'debug',
    browser: {
        serialize: true,
        asObject: false,
        transmit: {
            send: function (level, logEvent) {
                const msg = logEvent.messages.join(' ');
                const levelColors = {
                    10: '\x1b[90m', // trace - gray
                    20: '\x1b[36m', // debug - cyan
                    30: '\x1b[32m', // info - green
                    40: '\x1b[33m', // warn - yellow
                    50: '\x1b[31m', // error - red
                    60: '\x1b[35m'  // fatal - magenta
                };
                const levelNames = {
                    10: 'TRACE',
                    20: 'DEBUG',
                    30: 'INFO',
                    40: 'WARN',
                    50: 'ERROR',
                    60: 'FATAL'
                };
                const color = levelColors[logEvent.level] || '';
                const reset = '\x1b[0m';
                const timestamp = new Date().toISOString();
                console.log(`${color}[${timestamp}] ${levelNames[logEvent.level]} [custom-blocks]${reset} ${msg}`);
            }
        }
    }
});

// Initialize Blockly for web execution
let workspace;
let currentLanguage = 'javascript'; // Default to JavaScript for web
let generatorsReady = false;

log.debug('initializeGlobals()', 'workspace:', workspace, 'currentLanguage:', currentLanguage, 'generatorsReady:', generatorsReady);

// Store the original console for internal logging
const originalConsole = window.console;

// Custom console output capture (without internal logging to avoid recursion)
const outputConsole = {
    logs: [],
    log: function(...args) {
        const message = args.map(arg => {
            if (typeof arg === 'object') {
                try {
                    return JSON.stringify(arg, null, 2);
                } catch (e) {
                    return '[object]';
                }
            }
            return String(arg);
        }).join(' ');
        this.logs.push(message);
        updateOutput();
    },
    error: function(...args) {
        this.log('ERROR:', ...args);
    },
    warn: function(...args) {
        this.log('WARN:', ...args);
    },
    info: function(...args) {
        this.log('INFO:', ...args);
    },
    debug: function(...args) {
        this.log('DEBUG:', ...args);
    },
    clear: function() {
        this.logs = [];
        updateOutput();
    }
};

function updateOutput() {
    // Use original console for internal logging
    originalConsole.debug('updateOutput()', 'logs length:', outputConsole.logs.length);
    const output = document.getElementById('resultOutput').querySelector('code');
    const content = outputConsole.logs.join('\n') || 'Ready to run...';
    output.textContent = content;
    
    // Auto-scroll to bottom
    const container = document.getElementById('resultOutput');
    container.scrollTop = container.scrollHeight;
}

// Check if generators are initialized
function checkGeneratorsReady() {
    log.debug('checkGeneratorsReady()', 'checking conditions');
    const uinGeneratorsReady = window.uinGeneratorsReady === true;
    const uinLoaded = window.UINLoaded === true;
    const customBlocksLoaded = window.customBlocksLoaded === true;
    
    // Also check if a test generator exists
    let generatorExists = false;
    try {
        generatorExists = typeof Blockly !== 'undefined' && 
                         typeof Blockly.JavaScript !== 'undefined' &&
                         typeof Blockly.JavaScript.forBlock !== 'undefined' &&
                         typeof Blockly.JavaScript.forBlock['uin_model_remote'] === 'function';
    } catch (e) {
        log.debug('checkGeneratorsReady()', 'error checking generator:', e);
    }
    
    const result = uinGeneratorsReady && uinLoaded && customBlocksLoaded && generatorExists;
    log.debug('checkGeneratorsReady()', 
        'uinGeneratorsReady:', uinGeneratorsReady, 
        'uinLoaded:', uinLoaded,
        'customBlocksLoaded:', customBlocksLoaded,
        'generatorExists:', generatorExists,
        'result:', result);
    return result;
}

// Wait for generators and UIN to be ready
function waitForReady(callback) {
    log.debug('waitForReady()', 'callback:', callback.name || 'anonymous');
    if (checkGeneratorsReady()) {
        log.info('waitForReady()', 'generators ready, executing callback');
        generatorsReady = true;
        callback();
    } else {
        log.debug('waitForReady()', 'generators not ready, waiting 100ms');
        setTimeout(() => waitForReady(callback), 100);
    }
}

// Initialize workspace when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    log.info('DOMContentLoaded', 'event fired');
    
    // Wait for both UIN and custom blocks to load
    function checkAndInitialize() {
        if (!window.UINLoaded) {
            log.debug('checkAndInitialize', 'waiting for UIN...');
            window.addEventListener('uin-loaded', checkAndInitialize, { once: true });
            return;
        }
        
        if (!window.customBlocksLoaded) {
            log.debug('checkAndInitialize', 'waiting for custom blocks...');
            window.addEventListener('custom-blocks-loaded', checkAndInitialize, { once: true });
            return;
        }
        
        log.info('checkAndInitialize', 'both UIN and custom blocks loaded, initializing workspace');
        initializeWorkspace();
    }
    
    checkAndInitialize();
});

function initializeWorkspace() {
    log.info('initializeWorkspace()', 'starting');
    
    workspace = Blockly.inject('blocklyDiv', {
        toolbox: document.getElementById('toolbox'),
        grid: {
            spacing: 20,
            length: 3,
            colour: '#ccc',
            snap: true
        },
        zoom: {
            controls: true,
            wheel: true,
            startScale: 1.0,
            maxScale: 3,
            minScale: 0.3,
            scaleSpeed: 1.2
        },
        trashcan: true
    });
    
    log.debug('initializeWorkspace()', 'workspace created:', workspace);
    
    // Initialize custom block generators now that workspace exists
    if (typeof window.initializeBlocklyGenerators === 'function') {
        log.info('initializeWorkspace()', 'initializing custom block generators');
        const success = window.initializeBlocklyGenerators();
        if (success) {
            log.info('initializeWorkspace()', 'custom block generators initialized successfully');
            // Set the flag immediately
            generatorsReady = true;
            window.uinGeneratorsReady = true;
        } else {
            log.error('initializeWorkspace()', 'custom block generators initialization failed!');
            return; // Don't continue if generators failed
        }
    } else {
        log.error('initializeWorkspace()', 'initializeBlocklyGenerators not found!');
        // Try again in 100ms
        setTimeout(() => initializeWorkspace(), 100);
        return;
    }

    // Set up language selector
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            log.debug('languageButton.click()', 'language:', this.dataset.lang);
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentLanguage = this.dataset.lang;
            log.debug('languageButton.click()', 'currentLanguage set to:', currentLanguage);
            
            // Update run button state based on language
            updateRunButtonState();
            
            if (generatorsReady) {
                log.debug('languageButton.click()', 'generators ready, updating code');
                updateCode();
            }
        });
    });
    
    // Function to update run button state
    function updateRunButtonState() {
        const runBtn = document.getElementById('runCode');
        if (currentLanguage === 'python') {
            runBtn.disabled = true;
            runBtn.innerHTML = '▶ Run in Browser (JavaScript only)';
        } else {
            runBtn.disabled = false;
            runBtn.innerHTML = '▶ Run in Browser';
        }
    }
    
    // Set initial run button state
    updateRunButtonState();

    // Set up run button
    document.getElementById('runCode').addEventListener('click', runCode);
    log.debug('initializeWorkspace()', 'run button listener added');

    // Set up copy button
    document.getElementById('copyCode').addEventListener('click', copyCode);
    log.debug('initializeWorkspace()', 'copy button listener added');

    // Set up clear button
    document.getElementById('clearOutput').addEventListener('click', () => {
        log.debug('clearButton.click()', 'clearing output');
        outputConsole.clear();
    });
    log.debug('initializeWorkspace()', 'clear button listener added');
    
    // Set up example selector
    document.getElementById('exampleSelect').addEventListener('change', function() {
        const example = this.value;
        log.info('exampleSelect.change()', 'loading example:', example);
        if (example) {
            loadExample(example);
            this.value = ''; // Reset selector
        }
    });
    log.debug('initializeWorkspace()', 'example selector listener added');

    // Add change listener
    workspace.addChangeListener(() => {
        log.debug('workspace.changeListener()', 'change detected, generatorsReady:', generatorsReady);
        if (generatorsReady && window.uinGeneratorsReady) {
            updateCode();
        } else {
            log.warn('workspace.changeListener()', 'skipping updateCode - generators not ready');
        }
    });
    
    // Add default blocks
    log.info('initializeWorkspace()', 'adding default blocks');
    addDefaultBlocks();
    
    // Initial code update
    log.debug('initializeWorkspace()', 'performing initial code update');
    updateCode();
}

function updateCode() {
    log.debug('updateCode()', 'generatorsReady:', generatorsReady, 'currentLanguage:', currentLanguage, 'window.uinGeneratorsReady:', window.uinGeneratorsReady);
    
    // Check if generators exist
    const generatorExists = typeof Blockly?.JavaScript?.forBlock?.['uin_model_remote'] === 'function';
    log.debug('updateCode()', 'uin_model_remote generator exists:', generatorExists);
    
    // Check both flags and generator existence
    if (!generatorsReady || !window.uinGeneratorsReady || !generatorExists) {
        log.warn('updateCode()', 'generators not ready yet', 
            'generatorsReady:', generatorsReady, 
            'window.uinGeneratorsReady:', window.uinGeneratorsReady,
            'generatorExists:', generatorExists);
        
        // Try to initialize if not ready
        if (!generatorExists && typeof window.initializeBlocklyGenerators === 'function') {
            log.info('updateCode()', 'attempting to initialize generators');
            window.initializeBlocklyGenerators();
        }
        return;
    }
    
    try {
        let code;
        
        if (currentLanguage === 'python') {
            log.debug('updateCode()', 'generating Python code');
            // Python code for reference only
            let imports = `from universal_intelligence import Model, RemoteModel, Agent, Tool

`;
            code = imports + Blockly.Python.workspaceToCode(workspace);
            log.debug('updateCode()', 'Python code generated, length:', code.length);
        } else {
            log.debug('updateCode()', 'generating JavaScript code');
            // JavaScript code that will actually run
            code = Blockly.JavaScript.workspaceToCode(workspace);
            log.debug('updateCode()', 'JavaScript code generated, length:', code.length);
        }
        
        log.debug('updateCode()', 'setting code output');
        document.getElementById('codeOutput').querySelector('code').textContent = code;
    } catch (error) {
        log.error('updateCode()', 'error:', error.message, 'stack:', error.stack);
        document.getElementById('codeOutput').querySelector('code').textContent = '// Error generating code. Please ensure all blocks are properly connected.';
    }
}

function addDefaultBlocks() {
    log.info('addDefaultBlocks()', 'starting');
    
    // Check if workspace exists
    if (!workspace) {
        log.error('addDefaultBlocks()', 'workspace is null or undefined!');
        return;
    }
    
    try {
        // Create variables first using the new API
        const variableMap = workspace.getVariableMap();
        log.debug('addDefaultBlocks()', 'got variableMap:', variableMap);
        
        // Clear any existing variables first
        workspace.getVariableMap().clear();
        
        // Create the variables we need with specific IDs
        const variablesToCreate = [
            { name: 'model', id: 'modelVar' },
            { name: 'userInput', id: 'inputVar' },
            { name: 'modelOutput', id: 'outputVar' }
        ];
        
        variablesToCreate.forEach(varInfo => {
            log.debug('addDefaultBlocks()', 'creating variable:', varInfo.name, 'with id:', varInfo.id);
            variableMap.createVariable(varInfo.name, null, varInfo.id);
        });

        // Create a simple example: model processes text and displays output
        const xmlText = `<xml xmlns="https://developers.google.com/blockly/xml">
  <variables>
    <variable id="modelVar">model</variable>
    <variable id="inputVar">userInput</variable>
    <variable id="outputVar">modelOutput</variable>
  </variables>
  <block type="variables_set" x="20" y="20">
    <field name="VAR" id="modelVar">model</field>
    <value name="VALUE">
      <block type="uin_model_local">
        <field name="ENGINE">AUTO</field>
        <field name="QUANTIZATION">AUTO</field>
      </block>
    </value>
    <next>
      <block type="variables_set">
        <field name="VAR" id="inputVar">userInput</field>
        <value name="VALUE">
          <block type="text">
            <field name="TEXT">Hello! I'm learning about Universal Intelligence.

Can you:
1. Tell me a short joke about programming
2. Explain what makes it funny
3. Rate the joke from 1-10</field>
          </block>
        </value>
        <next>
          <block type="variables_set">
            <field name="VAR" id="outputVar">modelOutput</field>
            <value name="VALUE">
              <block type="uin_model_process">
                <field name="REMEMBER">FALSE</field>
                <value name="MODEL">
                  <block type="variables_get">
                    <field name="VAR" id="modelVar">model</field>
                  </block>
                </value>
                <value name="INPUT">
                  <block type="variables_get">
                    <field name="VAR" id="inputVar">userInput</field>
                  </block>
                </value>
              </block>
            </value>
            <next>
              <block type="text_pretty_print">
                <value name="TEXT">
                  <block type="variables_get">
                    <field name="VAR" id="outputVar">modelOutput</field>
                  </block>
                </value>
              </block>
            </next>
          </block>
        </next>
      </block>
    </next>
  </block>
</xml>`;
        
        log.debug('addDefaultBlocks()', 'parsing XML, length:', xmlText.length);
        
        // Parse and load the XML
        const parser = new DOMParser();
        const xml = parser.parseFromString(xmlText, 'text/xml');
        log.debug('addDefaultBlocks()', 'XML parsed successfully');
        
        // Check for parser errors
        const parserError = xml.querySelector('parsererror');
        if (parserError) {
            log.error('addDefaultBlocks()', 'XML parser error:', parserError.textContent);
            throw new Error('XML parsing failed');
        }
        
        // Use the newer Blockly serialization API if available
        if (Blockly.serialization && Blockly.serialization.workspaces) {
            log.debug('addDefaultBlocks()', 'using new serialization API');
            const state = Blockly.Xml.domToWorkspace(xml.documentElement, workspace);
        } else {
            log.debug('addDefaultBlocks()', 'using legacy XML API');
            Blockly.Xml.clearWorkspaceAndLoadFromXml(xml.documentElement, workspace);
        }
        log.info('addDefaultBlocks()', 'blocks loaded successfully');
        
        // Force a workspace render
        workspace.render();
        log.debug('addDefaultBlocks()', 'workspace rendered');
        
        // Clear output for fresh start
        outputConsole.clear();
        const resultOutput = document.getElementById('resultOutput');
        resultOutput.classList.remove('error', 'success');
    } catch (error) {
        log.error('addDefaultBlocks()', 'error:', error.message, 'stack:', error.stack);
        
        // Try a simpler default block as fallback
        try {
            log.info('addDefaultBlocks()', 'trying simple fallback block');
            const simpleXml = `<xml xmlns="https://developers.google.com/blockly/xml">
              <block type="variables_set" x="20" y="20">
                <field name="VAR">model</field>
                <value name="VALUE">
                  <block type="uin_model_local">
                    <field name="ENGINE">AUTO</field>
                    <field name="QUANTIZATION">AUTO</field>
                  </block>
                </value>
              </block>
            </xml>`;
            
            const parser = new DOMParser();
            const xml = parser.parseFromString(simpleXml, 'text/xml');
            Blockly.Xml.domToWorkspace(xml.documentElement, workspace);
            log.info('addDefaultBlocks()', 'simple fallback loaded');
        } catch (fallbackError) {
            log.error('addDefaultBlocks()', 'fallback also failed:', fallbackError.message);
        }
    }
}

async function runCode() {
    log.info('runCode()', 'starting', 'currentLanguage:', currentLanguage);
    
    const runBtn = document.getElementById('runCode');
    const resultOutput = document.getElementById('resultOutput');
    
    if (currentLanguage === 'python') {
        log.debug('runCode()', 'Python execution not supported in browser');
        resultOutput.classList.remove('error', 'success');
        resultOutput.querySelector('code').textContent = 'Python execution not available in browser. Switch to JavaScript to run code.';
        return;
    }
    
    // Check if generators are ready
    if (!window.uinGeneratorsReady) {
        log.warn('runCode()', 'generators not ready yet');
        resultOutput.classList.add('error');
        resultOutput.querySelector('code').textContent = 'Code generators are still loading. Please try again in a moment.';
        return;
    }
    
    // Update UI
    log.debug('runCode()', 'updating UI state');
    runBtn.disabled = true;
    runBtn.innerHTML = '⏳ Running...';
    outputConsole.clear();
    
    try {
        // Get the generated JavaScript code
        const code = Blockly.JavaScript.workspaceToCode(workspace);
        log.debug('runCode()', 'generated code length:', code.length);
        log.debug('runCode()', 'code:', code);
        
        // Create an async function that uses global UIN components
        log.debug('runCode()', 'creating execution function');
        
        // Wrap the code in an async function since it contains await
        const asyncCode = `
            (async function() {
                // Use the global UIN components
                const Model = window.Model;
                const RemoteModel = window.RemoteModel;
                const Agent = window.Agent;
                const Tool = window.Tool;
                
                ${code}
            })()
        `;
        
        // Execute with our custom console available globally
        log.info('runCode()', 'executing user code');
        
        // Temporarily replace console
        window.console = outputConsole;
        try {
            await eval(asyncCode);
        } finally {
            // Restore original console
            window.console = originalConsole;
        }
        
        log.debug('runCode()', 'execution completed successfully');
        resultOutput.classList.add('success');
        if (outputConsole.logs.length === 0) {
            log.debug('runCode()', 'no output logs, adding success message');
            outputConsole.log('Code executed successfully!');
        }
    } catch (error) {
        log.error('runCode()', 'execution error:', error.message, 'stack:', error.stack);
        resultOutput.classList.add('error');
        outputConsole.log(`Error: ${error.message}`);
    } finally {
        log.debug('runCode()', 'resetting UI state');
        runBtn.disabled = false;
        runBtn.innerHTML = '▶ Run in Browser';
    }
}

function loadExample(exampleName) {
    log.info('loadExample()', 'loading example:', exampleName);
    
    let xmlText = '';
    
    switch(exampleName) {
        case 'basic':
            xmlText = getBasicExample();
            break;
        case 'fetch':
            xmlText = getFetchExample();
            break;
        case 'research':
            xmlText = getResearchExample();
            break;
        case 'multi-tool':
            xmlText = getMultiToolExample();
            break;
        default:
            log.warn('loadExample()', 'unknown example:', exampleName);
            return;
    }
    
    try {
        const parser = new DOMParser();
        const xml = parser.parseFromString(xmlText, 'text/xml');
        Blockly.Xml.clearWorkspaceAndLoadFromXml(xml.documentElement, workspace);
        log.info('loadExample()', 'example loaded successfully');
        
        // Clear the output when loading a new example
        outputConsole.clear();
        const resultOutput = document.getElementById('resultOutput');
        resultOutput.classList.remove('error', 'success');
        log.debug('loadExample()', 'output cleared');
    } catch (error) {
        log.error('loadExample()', 'error loading example:', error);
    }
}

function getBasicExample() {
    // This is our current default example
    return `<xml xmlns="https://developers.google.com/blockly/xml">
  <variables>
    <variable id="modelVar">model</variable>
    <variable id="inputVar">userInput</variable>
    <variable id="outputVar">modelOutput</variable>
  </variables>
  <block type="variables_set" x="20" y="20">
    <field name="VAR" id="modelVar">model</field>
    <value name="VALUE">
      <block type="uin_model_local">
        <field name="ENGINE">AUTO</field>
        <field name="QUANTIZATION">AUTO</field>
      </block>
    </value>
    <next>
      <block type="variables_set">
        <field name="VAR" id="inputVar">userInput</field>
        <value name="VALUE">
          <block type="text">
            <field name="TEXT">Hello! I'm learning about Universal Intelligence.

Can you:
1. Tell me a short joke about programming
2. Explain what makes it funny
3. Rate the joke from 1-10</field>
          </block>
        </value>
        <next>
          <block type="variables_set">
            <field name="VAR" id="outputVar">modelOutput</field>
            <value name="VALUE">
              <block type="uin_model_process">
                <field name="REMEMBER">FALSE</field>
                <value name="MODEL">
                  <block type="variables_get">
                    <field name="VAR" id="modelVar">model</field>
                  </block>
                </value>
                <value name="INPUT">
                  <block type="variables_get">
                    <field name="VAR" id="inputVar">userInput</field>
                  </block>
                </value>
              </block>
            </value>
            <next>
              <block type="text_pretty_print">
                <value name="TEXT">
                  <block type="variables_get">
                    <field name="VAR" id="outputVar">modelOutput</field>
                  </block>
                </value>
              </block>
            </next>
          </block>
        </next>
      </block>
    </next>
  </block>
</xml>`;
}

function getFetchExample() {
    return `<xml xmlns="https://developers.google.com/blockly/xml">
  <variables>
    <variable id="fetchVar">fetchTool</variable>
    <variable id="resultVar">result</variable>
  </variables>
  <block type="variables_set" x="20" y="20">
    <field name="VAR" id="fetchVar">fetchTool</field>
    <value name="VALUE">
      <block type="uin_tool_fetch">
        <value name="URL">
          <block type="text">
            <field name="TEXT">https://api.github.com/repos/blueraai/universal-intelligence</field>
          </block>
        </value>
      </block>
    </value>
    <next>
      <block type="variables_set">
        <field name="VAR" id="resultVar">result</field>
        <value name="VALUE">
          <block type="uin_tool_call">
            <value name="TOOL">
              <block type="variables_get">
                <field name="VAR" id="fetchVar">fetchTool</field>
              </block>
            </value>
            <value name="METHOD">
              <block type="text">
                <field name="TEXT">fetchData</field>
              </block>
            </value>
            <value name="PARAMS">
              <block type="text">
                <field name="TEXT">{}</field>
              </block>
            </value>
          </block>
        </value>
        <next>
          <block type="text_pretty_print">
            <value name="TEXT">
              <block type="text_join">
                <mutation items="2"></mutation>
                <value name="ADD0">
                  <block type="text">
                    <field name="TEXT">Repository Stars: </field>
                  </block>
                </value>
                <value name="ADD1">
                  <block type="object_get_property">
                    <value name="OBJECT">
                      <block type="variables_get">
                        <field name="VAR" id="resultVar">result</field>
                      </block>
                    </value>
                    <value name="PROPERTY">
                      <block type="text">
                        <field name="TEXT">stargazers_count</field>
                      </block>
                    </value>
                  </block>
                </value>
              </block>
            </value>
          </block>
        </next>
      </block>
    </next>
  </block>
</xml>`;
}

function getResearchExample() {
    return `<xml xmlns="https://developers.google.com/blockly/xml">
  <variables>
    <variable id="modelVar">model</variable>
    <variable id="researchAgentVar">researchAgent</variable>
    <variable id="resultVar">result</variable>
  </variables>
  <block type="variables_set" x="20" y="20">
    <field name="VAR" id="modelVar">model</field>
    <value name="VALUE">
      <block type="uin_model_local">
        <field name="ENGINE">AUTO</field>
        <field name="QUANTIZATION">AUTO</field>
      </block>
    </value>
    <next>
      <block type="variables_set">
        <field name="VAR" id="researchAgentVar">researchAgent</field>
        <value name="VALUE">
          <block type="uin_agent_research">
            <value name="MODEL">
              <block type="variables_get">
                <field name="VAR" id="modelVar">model</field>
              </block>
            </value>
            <value name="SOURCES">
              <block type="lists_create_with">
                <mutation items="2"></mutation>
                <value name="ADD0">
                  <block type="text">
                    <field name="TEXT">https://api.github.com/repos/blueraai/universal-intelligence</field>
                  </block>
                </value>
                <value name="ADD1">
                  <block type="text">
                    <field name="TEXT">https://api.github.com/repos/google/blockly</field>
                  </block>
                </value>
              </block>
            </value>
          </block>
        </value>
        <next>
          <block type="variables_set">
            <field name="VAR" id="resultVar">result</field>
            <value name="VALUE">
              <block type="uin_tool_call">
                <value name="TOOL">
                  <block type="variables_get">
                    <field name="VAR" id="researchAgentVar">researchAgent</field>
                  </block>
                </value>
                <value name="METHOD">
                  <block type="text">
                    <field name="TEXT">research</field>
                  </block>
                </value>
                <value name="PARAMS">
                  <block type="text">
                    <field name="TEXT">Analyze the purpose and key features of these GitHub repositories</field>
                  </block>
                </value>
              </block>
            </value>
            <next>
              <block type="text_pretty_print">
                <value name="TEXT">
                  <block type="variables_get">
                    <field name="VAR" id="resultVar">result</field>
                  </block>
                </value>
              </block>
            </next>
          </block>
        </next>
      </block>
    </next>
  </block>
</xml>`;
}

function getMultiToolExample() {
    return `<xml xmlns="https://developers.google.com/blockly/xml">
  <variables>
    <variable id="modelVar">model</variable>
    <variable id="fetchVar">fetchTool</variable>
    <variable id="printerVar">printerTool</variable>
    <variable id="agentVar">multiAgent</variable>
    <variable id="resultVar">result</variable>
  </variables>
  <block type="variables_set" x="20" y="20">
    <field name="VAR" id="modelVar">model</field>
    <value name="VALUE">
      <block type="uin_model_local">
        <field name="ENGINE">AUTO</field>
        <field name="QUANTIZATION">AUTO</field>
      </block>
    </value>
    <next>
      <block type="variables_set">
        <field name="VAR" id="fetchVar">fetchTool</field>
        <value name="VALUE">
          <block type="uin_tool_fetch"></block>
        </value>
        <next>
          <block type="variables_set">
            <field name="VAR" id="printerVar">printerTool</field>
            <value name="VALUE">
              <block type="uin_tool_printer"></block>
            </value>
            <next>
              <block type="variables_set">
                <field name="VAR" id="agentVar">multiAgent</field>
                <value name="VALUE">
                  <block type="uin_agent_create">
                    <value name="MODEL">
                      <block type="variables_get">
                        <field name="VAR" id="modelVar">model</field>
                      </block>
                    </value>
                    <value name="TOOLS">
                      <block type="lists_create_with">
                        <mutation items="2"></mutation>
                        <value name="ADD0">
                          <block type="variables_get">
                            <field name="VAR" id="fetchVar">fetchTool</field>
                          </block>
                        </value>
                        <value name="ADD1">
                          <block type="variables_get">
                            <field name="VAR" id="printerVar">printerTool</field>
                          </block>
                        </value>
                      </block>
                    </value>
                  </block>
                </value>
                <next>
                  <block type="variables_set">
                    <field name="VAR" id="resultVar">result</field>
                    <value name="VALUE">
                      <block type="uin_agent_process">
                        <field name="REMEMBER">TRUE</field>
                        <value name="AGENT">
                          <block type="variables_get">
                            <field name="VAR" id="agentVar">multiAgent</field>
                          </block>
                        </value>
                        <value name="INPUT">
                          <block type="text">
                            <field name="TEXT">Please do the following:
1. Fetch data from https://api.github.com/users/github
2. Print the user's name and bio
3. Tell me an interesting fact about the number of public repos they have</field>
                          </block>
                        </value>
                      </block>
                    </value>
                    <next>
                      <block type="text_pretty_print">
                        <value name="TEXT">
                          <block type="variables_get">
                            <field name="VAR" id="resultVar">result</field>
                          </block>
                        </value>
                      </block>
                    </next>
                  </block>
                </next>
              </block>
            </next>
          </block>
        </next>
      </block>
    </next>
  </block>
</xml>`;
}

function copyCode() {
    log.info('copyCode()', 'starting');
    
    const code = document.getElementById('codeOutput').querySelector('code').textContent;
    const copyBtn = document.getElementById('copyCode');
    
    log.debug('copyCode()', 'code length:', code.length);
    
    navigator.clipboard.writeText(code).then(() => {
        log.debug('copyCode()', 'copy successful');
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '✓ Copied!';
        copyBtn.classList.add('copied');
        
        setTimeout(() => {
            log.debug('copyCode()', 'resetting button text');
            copyBtn.innerHTML = originalText;
            copyBtn.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        log.error('copyCode()', 'copy failed:', err.message);
    });
}

// Helper to create workspace from saved XML
function loadWorkspace(xmlText) {
    log.info('loadWorkspace()', 'xmlText length:', xmlText.length);
    
    try {
        workspace.clear();
        log.debug('loadWorkspace()', 'workspace cleared');
        
        const parser = new DOMParser();
        const xml = parser.parseFromString(xmlText, 'text/xml');
        log.debug('loadWorkspace()', 'XML parsed');
        
        Blockly.Xml.clearWorkspaceAndLoadFromXml(xml.documentElement, workspace);
        log.info('loadWorkspace()', 'workspace loaded successfully');
    } catch (error) {
        log.error('loadWorkspace()', 'error:', error.message, 'stack:', error.stack);
    }
}

// Helper to save workspace as XML
function saveWorkspace() {
    log.info('saveWorkspace()', 'starting');
    
    const xml = Blockly.Xml.workspaceToDom(workspace);
    const xmlText = Blockly.Xml.domToText(xml);
    
    log.debug('saveWorkspace()', 'XML generated, length:', xmlText.length);
    return xmlText;
}

// Modal handling for pretty print
function setupModal() {
    const modal = document.getElementById('printModal');
    const modalClose = modal.querySelector('.modal-close');
    const modalDismiss = modal.querySelector('.modal-dismiss');
    const modalOutput = document.getElementById('modalOutput').querySelector('code');
    
    // Show modal function
    window.showPrettyPrint = function(content) {
        log.debug('showPrettyPrint()', 'content:', content);
        
        // Format the content nicely
        let displayContent = content;
        if (typeof content === 'object') {
            try {
                displayContent = JSON.stringify(content, null, 2);
            } catch (e) {
                displayContent = String(content);
            }
        }
        
        modalOutput.textContent = displayContent;
        modal.classList.add('show');
        
        // Focus on dismiss button for accessibility
        modalDismiss.focus();
    };
    
    // Close modal function
    function closeModal() {
        modal.classList.remove('show');
        log.debug('closeModal()', 'modal closed');
    }
    
    // Event handlers
    modalClose.addEventListener('click', closeModal);
    modalDismiss.addEventListener('click', closeModal);
    
    // Close on background click
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Close on ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeModal();
        }
    });
    
    log.debug('setupModal()', 'modal handlers initialized');
}

// Initialize modal when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupModal);
} else {
    setupModal();
}

log.info('app-web.js', 'initialization complete');