import { Contract, Requirement } from '../../../core/types'
import { AbstractUniversalTool } from '../../../core/UniversalTool'

export class UniversalTool extends AbstractUniversalTool {
  private static readonly _contract: Contract = {
    name: "Simple Printer",
    description: "Prints a given text to the console",
    methods: [
      {
        name: "printText",
        description: "Prints to the console",
        arguments: [
          {
            name: "text",
            type: "string",
            schema: { maxLength: 100 },
            description: "Text to be printed",
            required: true
          }
        ],
        outputs: [
          {
            type: "string",
            description: "Text printed in the console",
            required: true
          },
          {
            type: "object",
            description: "Status of the operation",
            required: true
          }
        ]
      },
      {
        name: "contract",
        description: "Get a copy of the tool's contract specification, which describes its capabilities, methods, and interfaces. This helps understand what functionality the tool provides.",
        arguments: [],
        outputs: [
          {
            type: "Contract",
            description: "A copy of the tool's contract specification",
            required: true
          }
        ]
      },
      {
        name: "requirements",
        description: "Get a copy of the tool's configuration requirements, detailing what credentials and settings are needed to use this tool. This helps ensure proper tool setup.",
        arguments: [],
        outputs: [
          {
            type: "Requirement[]",
            description: "A list of the tool's configuration requirements",
            required: true
          }
        ]
      }
    ]
  }

  private static readonly _requirements: Requirement[] = [
    {
      name: "prefix",
      type: "string",
      schema: {},
      description: "Prefix for the example tool logs",
      required: false
    }
  ]

  private _configuration: Record<string, any>

  static contract(): Contract {
    return { ...UniversalTool._contract }
  }

  static requirements(): Requirement[] {
    return [...UniversalTool._requirements]
  }

  contract(): Contract {
    return { ...UniversalTool._contract }
  }

  requirements(): Requirement[] {
    return [...UniversalTool._requirements]
  }

  constructor(configuration?: Record<string, any>) {
    super(configuration)
    this._configuration = configuration || {}
  }

  printText({ text }: { text: string }): [string, Record<string, any>] {
    console.log("[Tool Call] Simple Printer.printText", { args: { text }})
    console.log("\n\n\n")
    if (this._configuration.prefix) {
      console.log(`[${this._configuration.prefix}] ${text}`)
    } else {
      console.log(text)
    }
    console.log("\n\n\n")
    return [text, { status: "success" }]
  }
} 