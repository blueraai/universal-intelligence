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

// Custom console output capture
const outputConsole = {
    logs: [],
    log: function(...args) {
        log.debug('outputConsole.log()', 'args:', args);
        const message = args.map(arg => {
            if (typeof arg === 'object') {
                return JSON.stringify(arg, null, 2);
            }
            return String(arg);
        }).join(' ');
        log.debug('outputConsole.log()', 'formatted message:', message);
        this.logs.push(message);
        updateOutput();
    },
    clear: function() {
        log.debug('outputConsole.clear()', 'previous logs length:', this.logs.length);
        this.logs = [];
        updateOutput();
    }
};

function updateOutput() {
    log.debug('updateOutput()', 'logs length:', outputConsole.logs.length);
    const output = document.getElementById('resultOutput').querySelector('code');
    const content = outputConsole.logs.join('\n') || 'Ready to run...';
    log.debug('updateOutput()', 'setting content:', content);
    output.textContent = content;
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
            if (generatorsReady) {
                log.debug('languageButton.click()', 'generators ready, updating code');
                updateCode();
            }
        });
    });

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
        
        const variablesToCreate = ['model', 'tool', 'agent', 'result'];
        variablesToCreate.forEach(varName => {
            if (!variableMap.getVariable(varName)) {
                log.debug('addDefaultBlocks()', 'creating variable:', varName);
                variableMap.createVariable(varName, null, varName + 'Var');
            } else {
                log.debug('addDefaultBlocks()', 'variable already exists:', varName);
            }
        });

        // Create a simple example: model processes text and printer displays output
        const xmlText = `<xml xmlns="https://developers.google.com/blockly/xml">
  <variables>
    <variable id="modelVar">model</variable>
    <variable id="inputVar">userInput</variable>
    <variable id="outputVar">modelOutput</variable>
    <variable id="printerVar">printer</variable>
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
            <field name="TEXT">Hello! Tell me a short joke about programming.</field>
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
              <block type="variables_set">
                <field name="VAR" id="printerVar">printer</field>
                <value name="VALUE">
                  <block type="uin_tool_printer"></block>
                </value>
                <next>
                  <block type="uin_tool_call">
                    <value name="TOOL">
                      <block type="variables_get">
                        <field name="VAR" id="printerVar">printer</field>
                      </block>
                    </value>
                    <value name="METHOD">
                      <block type="text">
                        <field name="TEXT">printText</field>
                      </block>
                    </value>
                    <value name="PARAMS">
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
        
        // Create a function that uses global UIN components
        log.debug('runCode()', 'creating execution function');
        // Make sure the classes are available globally
        const executeCode = new Function('console', `
            // Use the global UIN components
            const Model = window.Model;
            const RemoteModel = window.RemoteModel;
            const Agent = window.Agent;
            const Tool = window.Tool;
            
            ${code}
        `);
        
        // Execute with our custom console
        log.info('runCode()', 'executing user code');
        await executeCode(outputConsole);
        
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

log.info('app-web.js', 'initialization complete');