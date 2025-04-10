import js from '@eslint/js';
import tsPlugin from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import importPlugin from 'eslint-plugin-import';

export default [
  {
    ignores: [
      '**/node_modules/**',
      '**/dist/**',
      '**/distweb/**',
      '**/webdist/**',
      '**/build/**',
      '**/.next/**',
      '**/coverage/**',
      '**/public/**',
      '**/storybook-static/**',
      '**/*.d.ts',
      '**/*.js.map',
      '**/*.d.ts.map',
      'eslint.config.js',
      'vite.config.js'
    ],
  },
  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        // Browser APIs
        console: 'readonly',
        window: 'readonly',
        navigator: 'readonly',
        document: 'readonly',
        localStorage: 'readonly',
        sessionStorage: 'readonly',
        location: 'readonly',
        history: 'readonly',
        fetch: 'readonly',
        XMLHttpRequest: 'readonly',
        FormData: 'readonly',
        URL: 'readonly',
        URLSearchParams: 'readonly',
        Headers: 'readonly',
        Request: 'readonly',
        Response: 'readonly',
        Blob: 'readonly',
        File: 'readonly',
        FileReader: 'readonly',
        WebSocket: 'readonly',
        Event: 'readonly',
        CustomEvent: 'readonly',
        EventTarget: 'readonly',
        AbortController: 'readonly',
        AbortSignal: 'readonly',
        
        // Timers
        setTimeout: 'readonly',
        clearTimeout: 'readonly',
        setInterval: 'readonly',
        clearInterval: 'readonly',
        setImmediate: 'readonly',
        clearImmediate: 'readonly',
        requestAnimationFrame: 'readonly',
        cancelAnimationFrame: 'readonly',
        
        // Node.js APIs
        process: 'readonly',
        __dirname: 'readonly',
        __filename: 'readonly',
        module: 'readonly',
        exports: 'readonly',
        require: 'readonly',
        Buffer: 'readonly',
        global: 'readonly',
        
        // Web APIs
        self: 'readonly',
        indexedDB: 'readonly',
        crypto: 'readonly',
        performance: 'readonly',
        IntersectionObserver: 'readonly',
        MutationObserver: 'readonly',
        ResizeObserver: 'readonly',
        Intl: 'readonly',
      },
    },
  },
  js.configs.recommended,
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        ecmaFeatures: {
          jsx: true,
        },
        project: ['./tsconfig.json', './packages/*/tsconfig.json'],
        tsconfigRootDir: process.cwd(),
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
      'import': importPlugin,
    },
    rules: {
      ...tsPlugin.configs['recommended'].rules,
      ...tsPlugin.configs['recommended-type-checked'].rules,
      ...importPlugin.configs.recommended.rules,
      'import/no-unresolved': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
      '@typescript-eslint/no-redundant-type-constituents': 'off',
      '@typescript-eslint/no-duplicate-type-constituents': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unsafe-assignment': 'off',
      '@typescript-eslint/no-unsafe-argument': 'off',
      '@typescript-eslint/no-unsafe-member-access': 'off',
      '@typescript-eslint/no-unsafe-call': 'off',
      '@typescript-eslint/no-unsafe-return': 'off',
      '@typescript-eslint/restrict-template-expressions': 'off',
      '@typescript-eslint/await-thenable': 'off',
      '@typescript-eslint/no-floating-promises': 'off',
      '@typescript-eslint/explicit-function-return-type': ['warn', {
        allowExpressions: true,
        allowTypedFunctionExpressions: true,
      }],
      '@typescript-eslint/no-non-null-assertion': 'error',
      'import/order': [
        'error',
        {
          groups: [
            'builtin',
            'external',
            'internal',
            'parent',
            'sibling',
            'index',
            'object',
            'type',
          ],
          'newlines-between': 'always',
          alphabetize: {
            order: 'asc',
            caseInsensitive: true,
          },
        },
      ],
      'semi': ['error', 'never'],
    },
  },
  {
    files: ['**/*.js', '**/*.jsx', '**/*.mjs', '**/*.cjs'],
    plugins: {
      'import': importPlugin,
    },
    rules: {
      ...importPlugin.configs.recommended.rules,
      'import/no-unresolved': 'off',
      'import/order': [
        'error',
        {
          groups: [
            'builtin',
            'external',
            'internal',
            'parent',
            'sibling',
            'index',
            'object',
            'type',
          ],
          'newlines-between': 'always',
          alphabetize: {
            order: 'asc',
            caseInsensitive: true,
          },
        },
      ],
    },
  },
]; 