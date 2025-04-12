import React, { useRef } from 'react';
import Editor, { Monaco } from '@monaco-editor/react';
import { createCompletionProvider } from './CompletionProvider';
import { editor } from 'monaco-editor';

interface CodeEditorProps {
  code: string;
  onChange: (value: string) => void;
}

const CodeEditor: React.FC<CodeEditorProps> = ({ code, onChange }) => {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);

  // Function to handle editor mounting
  const handleEditorDidMount = (editor: editor.IStandaloneCodeEditor, monaco: Monaco) => {
    editorRef.current = editor;

    // Add custom completions if Monaco is available
    monaco.languages.registerCompletionItemProvider('python', createCompletionProvider());
  };

  // Define editor options
  const editorOptions: editor.IStandaloneEditorConstructionOptions = {
    selectOnLineNumbers: true,
    roundedSelection: false,
    readOnly: false,
    cursorStyle: 'line',
    automaticLayout: true,
    minimap: { enabled: true },
    lineNumbers: 'on',
    scrollBeyondLastLine: false,
    wordWrap: 'on',
    fontSize: 14,
  };

  return (
    <div style={{ border: '1px solid #333', borderRadius: '4px', overflow: 'hidden' }}>
      <Editor
        height="400px"
        defaultLanguage="python"
        theme="vs-dark"
        value={code}
        options={editorOptions}
        onChange={(value) => onChange(value || '')}
        onMount={handleEditorDidMount}
      />
    </div>
  );
};

export default CodeEditor;
