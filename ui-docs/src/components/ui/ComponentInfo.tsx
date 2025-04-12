import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface ComponentInfoProps {
  title: string;
  description: string;
  codeExample: string;
  docsLink: string;
  color: string;
}

const ComponentInfo: React.FC<ComponentInfoProps> = ({
  title,
  description,
  codeExample,
  docsLink,
  color,
}) => {
  return (
    <div className="bg-slate-800 rounded-lg overflow-hidden h-full flex flex-col">
      <div
        className="p-4"
        style={{ backgroundColor: color }}
      >
        <h2 className="text-2xl font-bold text-white">{title}</h2>
      </div>

      <div className="p-4 flex-1 overflow-y-auto">
        <div className="mb-4">
          <h3 className="text-lg font-semibold mb-2 text-white">Description</h3>
          <p className="text-slate-300">{description}</p>
        </div>

        <div className="mb-4">
          <h3 className="text-lg font-semibold mb-2 text-white">Code Example</h3>
          <div className="rounded-md overflow-hidden">
            <SyntaxHighlighter
              language="python"
              style={vscDarkPlus}
              customStyle={{ margin: 0, borderRadius: '0.375rem' }}
            >
              {codeExample}
            </SyntaxHighlighter>
          </div>
        </div>

        <div>
          <a
            href={docsLink}
            className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded"
            rel="noopener noreferrer"
          >
            Read Documentation
          </a>
        </div>
      </div>
    </div>
  );
};

export default ComponentInfo;
