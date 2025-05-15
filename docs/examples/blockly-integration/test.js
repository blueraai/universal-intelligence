/**
 * Integration tests for Universal Agents Blockly integration.
 * 
 * These tests ensure that the Blockly integration works as expected
 * by testing key functionality like:
 * - Workspace initialization
 * - Block creation and connection
 * - Code generation
 * - Saving and loading workspaces
 */

// Debug logging
const DEBUG = true;

function debugLog(...args) {
  if (DEBUG) {
    console.log('%c[DEBUG]', 'color: blue; font-weight: bold', ...args);
  }
}

function debugDir(obj, label) {
  if (DEBUG) {
    console.groupCollapsed(`%c[DEBUG] ${label}`, 'color: blue; font-weight: bold');
    console.dir(obj);
    console.groupEnd();
  }
}

// Environment check
debugLog('Checking environment...');
debugLog('Blockly available:', typeof Blockly !== 'undefined');
debugLog('Browser:', navigator.userAgent);
if (typeof Blockly !== 'undefined') {
  debugDir(Blockly, 'Blockly object');
  debugLog('Blockly version:', Blockly.VERSION || 'unknown');
}

// Test framework (simple implementation)
class TestSuite {
  constructor(name) {
    this.name = name;
    this.tests = [];
    this.results = {
      passed: 0,
      failed: 0,
      total: 0
    };
    debugLog(`Test suite created: ${name}`);
  }

  addTest(name, testFn) {
    this.tests.push({ name, testFn });
    debugLog(`Test added: ${name}`);
  }

  async runTests() {
    console.log(`Running test suite: ${this.name}`);
    debugLog(`Starting test suite execution: ${this.name} with ${this.tests.length} tests`);
    const results = [];

    for (const test of this.tests) {
      console.log(`  Running test: ${test.name}`);
      debugLog(`Executing test: ${test.name}`);
      try {
        await test.testFn();
        console.log(`  ✓ PASS: ${test.name}`);
        debugLog(`✓ Test passed: ${test.name}`);
        this.results.passed++;
        results.push({ name: test.name, passed: true, error: null });
      } catch (error) {
        console.error(`  ✗ FAIL: ${test.name}`);
        console.error(`    Error: ${error.message}`);
        debugLog(`✗ Test failed: ${test.name}`, error);
        debugLog('Error stack:', error.stack);
        this.results.failed++;
        results.push({ name: test.name, passed: false, error: error.message });
      }
      this.results.total++;
    }

    console.log(`\nTest suite: ${this.name}`);
    console.log(`  Passed: ${this.results.passed}/${this.results.total}`);
    console.log(`  Failed: ${this.results.failed}/${this.results.total}`);
    debugLog(`Test suite completed: ${this.name}`, this.results);

    return {
      name: this.name,
      results,
      summary: this.results
    };
  }
}

// Assertion utilities
class Assertions {
  static assertEquals(actual, expected, message) {
    debugLog(`Assertion - equals: ${JSON.stringify(actual)} === ${JSON.stringify(expected)}`);
    if (actual !== expected) {
      debugLog(`Assertion FAILED: ${JSON.stringify(actual)} !== ${JSON.stringify(expected)}`);
      throw new Error(message || `Expected ${expected}, but got ${actual}`);
    }
    debugLog('Assertion passed');
  }

  static assertTrue(condition, message) {
    debugLog(`Assertion - true: ${condition}`);
    if (!condition) {
      debugLog(`Assertion FAILED: ${condition} is not true`);
      throw new Error(message || 'Assertion failed: expected true but got false');
    }
    debugLog('Assertion passed');
  }

  static assertFalse(condition, message) {
    debugLog(`Assertion - false: ${condition}`);
    if (condition) {
      debugLog(`Assertion FAILED: ${condition} is not false`);
      throw new Error(message || 'Assertion failed: expected false but got true');
    }
    debugLog('Assertion passed');
  }

  static assertNotNull(value, message) {
    debugLog(`Assertion - not null: ${value}`);
    if (value === null || value === undefined) {
      debugLog(`Assertion FAILED: ${value} is null or undefined`);
      throw new Error(message || 'Assertion failed: value is null or undefined');
    }
    debugLog('Assertion passed');
  }

  static assertContains(text, substring, message) {
    debugLog(`Assertion - contains: "${text}" should contain "${substring}"`);
    if (!text.includes(substring)) {
      debugLog(`Assertion FAILED: "${text}" does not contain "${substring}"`);
      throw new Error(message || `Expected text to contain "${substring}" but it doesn't`);
    }
    debugLog('Assertion passed');
  }
}

/**
 * Run the integration tests.
 * This function assumes it's being run in the context of the Blockly demo page.
 */
async function runBlocklyIntegrationTests() {
  debugLog('Starting integration tests...');
  
  try {
    // Check if required DOM elements exist
    debugLog('Checking required DOM elements...');
    const blocklyDiv = document.getElementById('blocklyDiv');
    const codeDiv = document.getElementById('codeDiv');
    const pythonCodeDiv = document.getElementById('pythonCodeDiv');
    const flowVisualization = document.getElementById('flowVisualization');
    
    if (!blocklyDiv) {
      console.error('Missing #blocklyDiv element');
      throw new Error('Missing #blocklyDiv element, cannot proceed with tests');
    }
    
    if (!codeDiv || !pythonCodeDiv || !flowVisualization) {
      console.warn('Some display elements are missing:', {
        codeDiv: !!codeDiv,
        pythonCodeDiv: !!pythonCodeDiv,
        flowVisualization: !!flowVisualization
      });
    }
    
    // Check if Blockly is properly initialized
    debugLog('Checking Blockly initialization...');
    if (typeof Blockly === 'undefined') {
      console.error('Blockly is not defined');
      throw new Error('Blockly is not loaded, cannot proceed with tests');
    }
    
    // Store original DOM state to restore later
    debugLog('Storing original DOM state...');
    const originalBlocklyDiv = blocklyDiv.innerHTML;
    const originalCodeDiv = codeDiv ? codeDiv.innerHTML : '';
    const originalPythonCodeDiv = pythonCodeDiv ? pythonCodeDiv.innerHTML : '';
    const originalFlowVisualization = flowVisualization ? flowVisualization.innerHTML : '';
    
    // Create test suite
    debugLog('Creating test suite...');
    const testSuite = new TestSuite('Universal Agents Blockly Integration Tests');

    // Test: Workspace initialization
    testSuite.addTest('Workspace initialization', () => {
      debugLog('Testing workspace initialization...');
      // Check if Blockly workspace is initialized
      const workspace = Blockly.getMainWorkspace();
      debugDir(workspace, 'Main workspace');
      Assertions.assertNotNull(workspace, 'Blockly workspace should be initialized');
      
      // Clear any existing blocks to ensure a clean test environment
      workspace.clear();
      
      // Check if workspace is empty
      const blocks = workspace.getAllBlocks(false);
      debugDir(blocks, 'Blocks in workspace');
      Assertions.assertEquals(blocks.length, 0, 'Workspace should be empty');
    });

    // Test: Toolbox configuration
    testSuite.addTest('Toolbox configuration', () => {
      debugLog('Testing toolbox configuration...');
      // Check if toolbox has categories
      const toolbox = document.getElementById('toolbox');
      debugDir(toolbox, 'Toolbox element');
      Assertions.assertNotNull(toolbox, 'Toolbox element should exist');
      
      const categories = toolbox.querySelectorAll('category');
      debugLog('Categories found:', categories.length);
      Assertions.assertTrue(categories.length > 0, 'Toolbox should have categories');
      
      // Check specific categories
      const categoryNames = Array.from(categories).map(cat => cat.getAttribute('name'));
      debugLog('Category names:', categoryNames);
      Assertions.assertTrue(categoryNames.includes('Core'), 'Toolbox should have a Core category');
      Assertions.assertTrue(categoryNames.includes('Universal Agents'), 'Toolbox should have a Universal Agents category');
      Assertions.assertTrue(categoryNames.includes('Patterns'), 'Toolbox should have a Patterns category');
    });

    // Test: Block creation
    testSuite.addTest('Block creation', () => {
      debugLog('Testing block creation...');
      // Create a simple block
      const workspace = Blockly.getMainWorkspace();
      workspace.clear();  // Ensure workspace is clean
      
      debugLog('Creating text_print block...');
      const block = workspace.newBlock('text_print');
      debugDir(block, 'Created block');
      Assertions.assertNotNull(block, 'Block should be created');
      Assertions.assertEquals(block.type, 'text_print', 'Block should be of correct type');
      
      // Position the block
      debugLog('Positioning and rendering block...');
      try {
        block.initSvg();
        block.render();
        if (typeof Blockly.utils.Coordinate === 'undefined') {
          debugLog('Blockly.utils.Coordinate is undefined, trying alternative APIs');
          // Try alternative APIs based on Blockly version
          if (typeof Blockly.utils.Coordinate === 'undefined' && 
              typeof Blockly.utils.Rect !== 'undefined') {
            block.moveBy(50, 50);
          } else {
            // Fallback for very old versions
            block.moveBy(50, 50);
          }
        } else {
          block.moveTo(new Blockly.utils.Coordinate(50, 50));
        }
      } catch (error) {
        debugLog('Error during block positioning:', error);
        // Continue with the test even if positioning fails
      }
      
      // Check if block is in workspace
      const blocks = workspace.getAllBlocks(false);
      debugLog('Blocks in workspace after creation:', blocks.length);
      debugDir(blocks, 'All blocks');
      Assertions.assertEquals(blocks.length, 1, 'Workspace should have one block');
    });

    // Test: Code generation
    testSuite.addTest('Code generation', () => {
      debugLog('Testing code generation...');
      // Get generated code
      const workspace = Blockly.getMainWorkspace();
      
      // Check if code generators are available
      Assertions.assertNotNull(Blockly.JavaScript, 'JavaScript generator should be available');
      Assertions.assertNotNull(Blockly.Python, 'Python generator should be available');
      
      const jsCode = Blockly.JavaScript.workspaceToCode(workspace);
      debugLog('Generated JavaScript code:', jsCode);
      const pythonCode = Blockly.Python.workspaceToCode(workspace);
      debugLog('Generated Python code:', pythonCode);
      
      // Check if code was generated
      Assertions.assertTrue(jsCode.length > 0, 'JavaScript code should be generated');
      Assertions.assertTrue(pythonCode.length > 0, 'Python code should be generated');
      
      // Check if code appears in the code div
      if (codeDiv && pythonCodeDiv) {
        Assertions.assertEquals(codeDiv.textContent, jsCode, 'JavaScript code should appear in the code div');
        Assertions.assertEquals(pythonCodeDiv.textContent, pythonCode, 'Python code should appear in the Python code div');
      } else {
        debugLog('Code display divs not available, skipping display check');
      }
    });

    // Test: Block connection
    testSuite.addTest('Block connection', () => {
      debugLog('Testing block connection...');
      // Create blocks that can be connected
      const workspace = Blockly.getMainWorkspace();
      workspace.clear();  // Clear existing blocks
      
      debugLog('Creating if and compare blocks...');
      const ifBlock = workspace.newBlock('controls_if');
      const compareBlock = workspace.newBlock('logic_compare');
      
      // Initialize blocks
      debugLog('Initializing blocks...');
      try {
        ifBlock.initSvg();
        ifBlock.render();
        compareBlock.initSvg();
        compareBlock.render();
        
        // Position blocks (using safe positioning)
        debugLog('Positioning blocks...');
        ifBlock.moveBy(50, 50);
        compareBlock.moveBy(50, 150);
        
        // Connect blocks
        debugLog('Connecting blocks...');
        const ifInput = ifBlock.getInput('IF0');
        debugDir(ifInput, 'IF0 input');
        
        if (ifInput && ifInput.connection) {
          const connection = ifInput.connection;
          connection.connect(compareBlock.outputConnection);
          
          // Check if blocks are connected
          Assertions.assertTrue(compareBlock.outputConnection.isConnected(), 'Blocks should be connected');
          Assertions.assertEquals(compareBlock.outputConnection.targetConnection, connection, 'Connection should be to the correct input');
        } else {
          debugLog('IF0 input or connection not available, skipping connection test');
        }
      } catch (error) {
        debugLog('Error during block connection:', error);
        throw error;
      }
    });

    // Test: Tab switching
    testSuite.addTest('Tab switching', () => {
      debugLog('Testing tab switching...');
      const jsPanel = document.getElementById('jsPanel');
      const pythonPanel = document.getElementById('pythonPanel');
      const jsTab = document.getElementById('jsTab');
      const pythonTab = document.getElementById('pythonTab');
      
      if (!jsPanel || !pythonPanel || !jsTab || !pythonTab) {
        debugLog('Tab elements not found, skipping tab switching test');
        return;
      }
      
      // JavaScript tab should be active by default
      Assertions.assertTrue(jsPanel.classList.contains('active'), 'JavaScript panel should be active by default');
      
      // Click Python tab
      debugLog('Clicking Python tab...');
      pythonTab.click();
      Assertions.assertFalse(jsPanel.classList.contains('active'), 'JavaScript panel should not be active after clicking Python tab');
      Assertions.assertTrue(pythonPanel.classList.contains('active'), 'Python panel should be active after clicking Python tab');
      
      // Click JavaScript tab again
      debugLog('Clicking JavaScript tab...');
      jsTab.click();
      Assertions.assertTrue(jsPanel.classList.contains('active'), 'JavaScript panel should be active after clicking JavaScript tab');
      Assertions.assertFalse(pythonPanel.classList.contains('active'), 'Python panel should not be active after clicking JavaScript tab');
    });

    // Test: Saving and loading workspace
    testSuite.addTest('Saving and loading workspace', () => {
      debugLog('Testing saving and loading workspace...');
      // Create a workspace with a block
      const workspace = Blockly.getMainWorkspace();
      workspace.clear();  // Clear existing blocks
      
      debugLog('Creating test block for saving...');
      const block = workspace.newBlock('text_print');
      block.initSvg();
      block.render();
      
      const saveButton = document.getElementById('saveButton');
      const loadButton = document.getElementById('loadButton');
      
      if (!saveButton || !loadButton) {
        debugLog('Save/Load buttons not found, skipping save/load test');
        return;
      }
      
      // Save workspace
      debugLog('Clicking save button...');
      saveButton.click();
      
      // Clear workspace
      debugLog('Clearing workspace...');
      workspace.clear();
      Assertions.assertEquals(workspace.getAllBlocks(false).length, 0, 'Workspace should be empty after clearing');
      
      // Load workspace
      debugLog('Clicking load button...');
      loadButton.click();
      
      // Check if block was loaded
      const loadedBlocks = workspace.getAllBlocks(false);
      debugLog('Blocks after loading:', loadedBlocks.length);
      Assertions.assertEquals(loadedBlocks.length, 1, 'Workspace should have one block after loading');
      Assertions.assertEquals(loadedBlocks[0].type, 'text_print', 'Loaded block should be of correct type');
    });

    // Test: Run button and visualization
    testSuite.addTest('Run button and visualization', () => {
      debugLog('Testing run button and visualization...');
      // Create a workspace with blocks
      const workspace = Blockly.getMainWorkspace();
      workspace.clear();  // Clear existing blocks
      
      debugLog('Creating test blocks for run test...');
      const block1 = workspace.newBlock('text_print');
      const block2 = workspace.newBlock('text');
      
      block1.initSvg();
      block1.render();
      block2.initSvg();
      block2.render();
      
      const runButton = document.getElementById('runButton');
      
      if (!runButton || !flowVisualization) {
        debugLog('Run button or flow visualization element not found, skipping run test');
        return;
      }
      
      // Run flow
      debugLog('Clicking run button...');
      runButton.click();
      
      // Check visualization
      const visualization = flowVisualization.innerHTML;
      debugLog('Visualization content:', visualization);
      Assertions.assertContains(visualization, 'Flow execution started', 'Visualization should indicate flow execution');
      Assertions.assertContains(visualization, 'text_print', 'Visualization should mention blocks in the flow');
      
      // Check status bar
      const statusBar = document.getElementById('statusBar');
      if (statusBar) {
        const statusText = statusBar.textContent;
        debugLog('Status bar content:', statusText);
        Assertions.assertContains(statusText, 'Running flow', 'Status bar should indicate flow is running');
      } else {
        debugLog('Status bar element not found, skipping status check');
      }
    });

    // Run all tests
    debugLog('Running all tests...');
    const results = await testSuite.runTests();
    
    // Restore original DOM state
    debugLog('Restoring original DOM state...');
    if (blocklyDiv) blocklyDiv.innerHTML = originalBlocklyDiv;
    if (codeDiv) codeDiv.innerHTML = originalCodeDiv;
    if (pythonCodeDiv) pythonCodeDiv.innerHTML = originalPythonCodeDiv;
    if (flowVisualization) flowVisualization.innerHTML = originalFlowVisualization;
    
    debugLog('Tests completed, returning results');
    return results;
  } catch (error) {
    console.error('Fatal error during test execution:', error);
    debugLog('Fatal error:', error);
    return {
      name: 'Universal Agents Blockly Integration Tests',
      results: [{ name: 'Test initialization', passed: false, error: error.message }],
      summary: { passed: 0, failed: 1, total: 1 }
    };
  }
}

// Function to display test results in the page
function displayTestResults(results) {
  // Create test results display
  const resultsDiv = document.createElement('div');
  resultsDiv.id = 'testResults';
  resultsDiv.style.position = 'fixed';
  resultsDiv.style.top = '50px';
  resultsDiv.style.right = '20px';
  resultsDiv.style.backgroundColor = '#f8f8f8';
  resultsDiv.style.border = '1px solid #ddd';
  resultsDiv.style.padding = '15px';
  resultsDiv.style.zIndex = '1000';
  resultsDiv.style.maxHeight = '80vh';
  resultsDiv.style.overflow = 'auto';
  resultsDiv.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
  
  // Create header
  const header = document.createElement('h3');
  header.textContent = results.name;
  resultsDiv.appendChild(header);
  
  // Create summary
  const summary = document.createElement('p');
  summary.innerHTML = `
    <strong>Summary:</strong><br>
    Passed: <span style="color: green">${results.summary.passed}</span>/${results.summary.total}<br>
    Failed: <span style="color: red">${results.summary.failed}</span>/${results.summary.total}
  `;
  resultsDiv.appendChild(summary);
  
  // Create test list
  const list = document.createElement('ul');
  list.style.paddingLeft = '20px';
  
  for (const test of results.results) {
    const item = document.createElement('li');
    if (test.passed) {
      item.innerHTML = `<span style="color: green">✓</span> ${test.name}`;
    } else {
      item.innerHTML = `<span style="color: red">✗</span> ${test.name}<br><small style="color: #666">${test.error}</small>`;
    }
    list.appendChild(item);
  }
  
  resultsDiv.appendChild(list);
  
  // Add close button
  const closeButton = document.createElement('button');
  closeButton.textContent = 'Close';
  closeButton.style.marginTop = '10px';
  closeButton.addEventListener('click', () => {
    document.body.removeChild(resultsDiv);
  });
  resultsDiv.appendChild(closeButton);
  
  // Add to page
  document.body.appendChild(resultsDiv);
}

// Add button to run tests
function addTestButton() {
  const button = document.createElement('button');
  button.textContent = 'Run Tests';
  button.style.backgroundColor = '#9c27b0';
  button.style.marginLeft = '10px';
  
  button.addEventListener('click', async () => {
    button.disabled = true;
    button.textContent = 'Running Tests...';
    
    // Run tests and display results
    try {
      const results = await runBlocklyIntegrationTests();
      displayTestResults(results);
    } catch (error) {
      console.error('Error running tests:', error);
      alert('Error running tests: ' + error.message);
    } finally {
      button.disabled = false;
      button.textContent = 'Run Tests';
    }
  });
  
  // Add button to controls
  document.querySelector('.controls').appendChild(button);
}

// Initialize tests when page loads
window.addEventListener('load', () => {
  // Add test button after a short delay to ensure Blockly is fully loaded
  setTimeout(addTestButton, 500);
});