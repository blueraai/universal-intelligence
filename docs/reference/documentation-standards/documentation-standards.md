# Documentation Standards

## Directory Structure

The documentation is organized into the following subdirectories:

```
docs/
├── README.md
├── guides/        # User-focused how-to guides and reference documentation
├── specs/         # Technical specifications and implementation details
├── playbooks/     # Step-by-step procedures for common tasks
└── examples/      # Example configurations and use cases
```

## Documentation Types

The documentation follows a structured approach with different document types serving specific purposes:

1. **Guides (`guide-*.md`)**: User-focused documentation that explains how to use features, provides reference information, and offers best practices. Guides answer "how to" questions.

2. **Specifications (`spec-*.md`)**: Technical documentation that details the implementation, architecture, and design decisions. Specifications answer "how it works" questions.

3. **Playbooks (`playbook-*.md`)**: Step-by-step procedures for accomplishing specific tasks or workflows. Playbooks answer "what steps to follow" questions.

4. **Analysis (`analysis-*.md`)**: In-depth examination of problems, requirements, or existing systems. Analysis documents answer "what and why" questions.

5. **Plans (`plan-*.md`)**: Forward-looking documents outlining future work, roadmaps, or implementation strategies. Plans answer "what will be done" questions.

## Naming Conventions

All documentation follows this naming convention:

```
[document-type]-[descriptive-name]-v[major].[minor].[patch].[extension]
```

Where:
- **document-type**: The type of document (guide, spec, playbook, analysis, plan)
- **descriptive-name**: A hyphen-separated name describing the content
- **version**: Semantic versioning with major.minor.patch format
- **extension**: File extension (typically .md for Markdown)

Examples:
- `guide-mode-mapping-v1.2.0.md`
- `spec-custom-modes-implementation-v1.2.0.md`
- `playbook-settings-synchronization-v1.0.0.md`

## Versioning Guidelines

When updating documentation:

1. **Patch Version (v1.0.x)**: Increment for minor corrections, typo fixes, or clarifications that don't change the content's meaning.

2. **Minor Version (v1.x.0)**: Increment for additions, improvements, or restructuring that doesn't fundamentally change the document's purpose or main content.

3. **Major Version (vx.0.0)**: Increment for significant rewrites, changes to the document's purpose, or when the subject matter itself has undergone major changes.