import { editor, languages, Position } from 'monaco-editor';

// Custom completion provider for Monaco Editor
export const createCompletionProvider = () => {
  return {
    provideCompletionItems: (
      model: editor.ITextModel,
      position: Position
    ): languages.ProviderResult<languages.CompletionList> => {
      const word = model.getWordUntilPosition(position);
      const range = {
        startLineNumber: position.lineNumber,
        endLineNumber: position.lineNumber,
        startColumn: word.startColumn,
        endColumn: word.endColumn,
      };

      // Basic Python keywords and Universal Intelligence specific completions
      const suggestions: languages.CompletionItem[] = [
        // Python keywords
        { label: 'from', kind: languages.CompletionItemKind.Keyword, insertText: 'from', range },
        { label: 'import', kind: languages.CompletionItemKind.Keyword, insertText: 'import', range },
        { label: 'def', kind: languages.CompletionItemKind.Keyword, insertText: 'def ', range },
        { label: 'class', kind: languages.CompletionItemKind.Keyword, insertText: 'class ', range },
        { label: 'if', kind: languages.CompletionItemKind.Keyword, insertText: 'if ', range },
        { label: 'else', kind: languages.CompletionItemKind.Keyword, insertText: 'else:', range },
        { label: 'for', kind: languages.CompletionItemKind.Keyword, insertText: 'for ', range },
        { label: 'while', kind: languages.CompletionItemKind.Keyword, insertText: 'while ', range },
        { label: 'return', kind: languages.CompletionItemKind.Keyword, insertText: 'return ', range },
        { label: 'True', kind: languages.CompletionItemKind.Keyword, insertText: 'True', range },
        { label: 'False', kind: languages.CompletionItemKind.Keyword, insertText: 'False', range },
        { label: 'None', kind: languages.CompletionItemKind.Keyword, insertText: 'None', range },
        { label: 'print', kind: languages.CompletionItemKind.Function, insertText: 'print()', range },

        // Universal Intelligence specific
        { label: 'universal_intelligence', kind: languages.CompletionItemKind.Module, insertText: 'universal_intelligence', range },
        { label: 'Model', kind: languages.CompletionItemKind.Class, insertText: 'Model', range },
        { label: 'Agent', kind: languages.CompletionItemKind.Class, insertText: 'Agent', range },
        { label: 'Tool', kind: languages.CompletionItemKind.Class, insertText: 'Tool', range },
        { label: 'process', kind: languages.CompletionItemKind.Method, insertText: 'process', range },
        { label: 'execute', kind: languages.CompletionItemKind.Method, insertText: 'execute', range },

        // Snippets with tabstops
        {
          label: 'model_init',
          kind: languages.CompletionItemKind.Snippet,
          insertText: 'model = Model()\nresponse = model.process("${1:prompt}")\nprint(response)',
          insertTextRules: languages.CompletionItemInsertTextRule.InsertAsSnippet,
          range,
          documentation: 'Initialize a model, process a prompt, and print the response',
        },
        {
          label: 'tool_init',
          kind: languages.CompletionItemKind.Snippet,
          insertText: 'tool = Tool()\nresult = tool.execute("${1:command}")\nprint(result)',
          insertTextRules: languages.CompletionItemInsertTextRule.InsertAsSnippet,
          range,
          documentation: 'Initialize a tool, execute a command, and print the result',
        },
        {
          label: 'agent_init',
          kind: languages.CompletionItemKind.Snippet,
          insertText: 'model = Model()\nagent = Agent(universal_model=model)\nresult = agent.process("${1:prompt}")\nprint(result)',
          insertTextRules: languages.CompletionItemInsertTextRule.InsertAsSnippet,
          range,
          documentation: 'Initialize a model and agent, process a prompt, and print the result',
        },
      ];

      return { suggestions };
    },
  };
};
