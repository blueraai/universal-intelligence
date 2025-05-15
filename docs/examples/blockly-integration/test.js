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
  }

  addTest(name, testFn) {
    this.tests.push({ name, testFn });
  }

  async runTests() {
    console.log(`Running test suite: ${this.name}`);
    const results = [];

    for (const test of this.tests) {
      console.log(`  Running test: ${test.name}`);
      try {
        await test.testFn();
        console.log(`  ✓ PASS: ${test.name}`);
        this.results.passed++;
        results.push({ name: test.name, passed: true, error: null });
      } catch (error) {
        console.error(`  ✗ FAIL: ${test.name}`);
        console.error(`    Error: ${error.message}`);
        this.results.failed++;
        results.push({ name: test.name, passed: false, error: error.message });
      }
      this.results.total++;
    }

    console.log(`\nTest suite: ${this.name}`);
    console.log(`  Passed: ${this.results.passed}/${this.results.total}`);
    console.log(`  Failed: ${this.results.failed}/${this.results.total}`);

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
    if (actual !== expected) {
      throw new Error(message || `Expected ${expected}, but got ${actual}`);
    }
  }

  static assertTrue(condition, message) {
    if (!condition) {
      throw new Error(message || 'Assertion failed: expected true but got false');
    }
  }

  static assertFalse(condition, message) {
    if (condition) {
      throw new Error(message || 'Assertion failed: expected false but got true');
    }
  }

  static assertNotNull(value, message) {
    if (value === null || value === undefined) {
      throw new Error(message || 'Assertion failed: value is null or undefined');
    }
  }

  static assertContains(text, substring, message) {
    if (!text.includes(substring)) {
      throw new Error(message || `Expected text to contain "${substring}" but it doesn't`);
    }
  }
}

/**
 * Run the integration tests.
 * This function assumes it's being run in the context of the Blockly demo page.
 */
async function runBlocklyIntegrationTests() {
  // Store original DOM state to restore later
  const originalBlocklyDiv = document.getElementById('blocklyDiv').innerHTML;
  const originalCodeDiv = document.getElementById('codeDiv').innerHTML;
  const originalPythonCodeDiv = document.getElementById('pythonCodeDiv').innerHTML;
  const originalFlowVisualization = document.getElementById('flowVisualization').innerHTML;
  
  // Create test suite
  const testSuite = new TestSuite('Universal Agents Blockly Integration Tests');

  // Test: Workspace initialization
  testSuite.addTest('Workspace initialization', () => {
    // Check if Blockly workspace is initialized
    Assertions.assertNotNull(Blockly.getMainWorkspace(), 'Blockly workspace should be initialized');
    // Check if workspace is empty
    Assertions.assertEquals(Blockly.getMainWorkspace().getAllBlocks(false).length, 0, 'Workspace should be empty');
  });

  // Test: Toolbox configuration
  testSuite.addTest('Toolbox configuration', () => {
    // Check if toolbox has categories
    const toolbox = document.getElementById('toolbox');
    Assertions.assertNotNull(toolbox, 'Toolbox element should exist');
    const categories = toolbox.querySelectorAll('category');
    Assertions.assertTrue(categories.length > 0, 'Toolbox should have categories');
    
    // Check specific categories
    const categoryNames = Array.from(categories).map(cat => cat.getAttribute('name'));
    Assertions.assertTrue(categoryNames.includes('Core'), 'Toolbox should have a Core category');
    Assertions.assertTrue(categoryNames.includes('Universal Agents'), 'Toolbox should have a Universal Agents category');
    Assertions.assertTrue(categoryNames.includes('Patterns'), 'Toolbox should have a Patterns category');
  });

  // Test: Block creation
  testSuite.addTest('Block creation', () => {
    // Create a simple block
    const workspace = Blockly.getMainWorkspace();
    const block = workspace.newBlock('text_print');
    Assertions.assertNotNull(block, 'Block should be created');
    Assertions.assertEquals(block.type, 'text_print', 'Block should be of correct type');
    
    // Position the block
    block.initSvg();
    block.render();
    block.moveTo(new Blockly.utils.Coordinate(50, 50));
    
    // Check if block is in workspace
    const blocks = workspace.getAllBlocks(false);
    Assertions.assertEquals(blocks.length, 1, 'Workspace should have one block');
  });

  // Test: Code generation
  testSuite.addTest('Code generation', () => {
    // Get generated code
    const workspace = Blockly.getMainWorkspace();
    const jsCode = Blockly.JavaScript.workspaceToCode(workspace);
    const pythonCode = Blockly.Python.workspaceToCode(workspace);
    
    // Check if code was generated
    Assertions.assertTrue(jsCode.length > 0, 'JavaScript code should be generated');
    Assertions.assertTrue(pythonCode.length > 0, 'Python code should be generated');
    
    // Check if code appears in the code div
    const codeDiv = document.getElementById('codeDiv');
    const pythonCodeDiv = document.getElementById('pythonCodeDiv');
    
    Assertions.assertEquals(codeDiv.textContent, jsCode, 'JavaScript code should appear in the code div');
    Assertions.assertEquals(pythonCodeDiv.textContent, pythonCode, 'Python code should appear in the Python code div');
  });

  // Test: Block connection
  testSuite.addTest('Block connection', () => {
    // Create blocks that can be connected
    const workspace = Blockly.getMainWorkspace();
    workspace.clear();  // Clear existing blocks
    
    const ifBlock = workspace.newBlock('controls_if');
    const compareBlock = workspace.newBlock('logic_compare');
    
    // Initialize blocks
    ifBlock.initSvg();
    ifBlock.render();
    compareBlock.initSvg();
    compareBlock.render();
    
    // Position blocks
    ifBlock.moveTo(new Blockly.utils.Coordinate(50, 50));
    compareBlock.moveTo(new Blockly.utils.Coordinate(50, 150));
    
    // Connect blocks
    const connection = ifBlock.getInput('IF0').connection;
    connection.connect(compareBlock.outputConnection);
    
    // Check if blocks are connected
    Assertions.assertTrue(compareBlock.outputConnection.isConnected(), 'Blocks should be connected');
    Assertions.assertEquals(compareBlock.outputConnection.targetConnection, connection, 'Connection should be to the correct input');
  });

  // Test: Tab switching
  testSuite.addTest('Tab switching', () => {
    // JavaScript tab should be active by default
    Assertions.assertTrue(document.getElementById('jsPanel').classList.contains('active'), 'JavaScript panel should be active by default');
    
    // Click Python tab
    document.getElementById('pythonTab').click();
    Assertions.assertFalse(document.getElementById('jsPanel').classList.contains('active'), 'JavaScript panel should not be active after clicking Python tab');
    Assertions.assertTrue(document.getElementById('pythonPanel').classList.contains('active'), 'Python panel should be active after clicking Python tab');
    
    // Click JavaScript tab again
    document.getElementById('jsTab').click();
    Assertions.assertTrue(document.getElementById('jsPanel').classList.contains('active'), 'JavaScript panel should be active after clicking JavaScript tab');
    Assertions.assertFalse(document.getElementById('pythonPanel').classList.contains('active'), 'Python panel should not be active after clicking JavaScript tab');
  });

  // Test: Saving and loading workspace
  testSuite.addTest('Saving and loading workspace', () => {
    // Create a workspace with a block
    const workspace = Blockly.getMainWorkspace();
    workspace.clear();  // Clear existing blocks
    
    const block = workspace.newBlock('text_print');
    block.initSvg();
    block.render();
    
    // Save workspace
    document.getElementById('saveButton').click();
    
    // Clear workspace
    workspace.clear();
    Assertions.assertEquals(workspace.getAllBlocks(false).length, 0, 'Workspace should be empty after clearing');
    
    // Load workspace
    document.getElementById('loadButton').click();
    
    // Check if block was loaded
    const loadedBlocks = workspace.getAllBlocks(false);
    Assertions.assertEquals(loadedBlocks.length, 1, 'Workspace should have one block after loading');
    Assertions.assertEquals(loadedBlocks[0].type, 'text_print', 'Loaded block should be of correct type');
  });

  // Test: Run button and visualization
  testSuite.addTest('Run button and visualization', () => {
    // Create a workspace with blocks
    const workspace = Blockly.getMainWorkspace();
    workspace.clear();  // Clear existing blocks
    
    const block1 = workspace.newBlock('text_print');
    const block2 = workspace.newBlock('text');
    
    block1.initSvg();
    block1.render();
    block2.initSvg();
    block2.render();
    
    // Run flow
    document.getElementById('runButton').click();
    
    // Check visualization
    const visualization = document.getElementById('flowVisualization').innerHTML;
    Assertions.assertContains(visualization, 'Flow execution started', 'Visualization should indicate flow execution');
    Assertions.assertContains(visualization, 'text_print', 'Visualization should mention blocks in the flow');
    
    // Check status bar
    const statusBar = document.getElementById('statusBar').textContent;
    Assertions.assertContains(statusBar, 'Running flow', 'Status bar should indicate flow is running');
  });

  // Run all tests
  const results = await testSuite.runTests();
  
  // Restore original DOM state
  document.getElementById('blocklyDiv').innerHTML = originalBlocklyDiv;
  document.getElementById('codeDiv').innerHTML = originalCodeDiv;
  document.getElementById('pythonCodeDiv').innerHTML = originalPythonCodeDiv;
  document.getElementById('flowVisualization').innerHTML = originalFlowVisualization;
  
  return results;
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