import { Contract, Requirement } from '../../../core/types'
import { AbstractUniversalTool } from '../../../core/UniversalTool'

import { Logger, LogLevel } from './../../../community/__utils__/logger'

export class UniversalTool extends AbstractUniversalTool {
  private static readonly _contract: Contract = {
    name: "API Caller",
    description: "Makes HTTP requests to an API endpoint",
    methods: [
      {
        name: "callApi",
        description: "Makes an HTTP request to an API endpoint",
        arguments: [
          {
            name: "url",
            type: "string",
            schema: {},
            description: "API endpoint URL",
            required: true
          },
          {
            name: "method",
            type: "string",
            schema: { oneOf: ["GET", "POST", "PUT", "DELETE", "PATCH"] },
            description: "HTTP method to use",
            required: false
          },
          {
            name: "body",
            type: "object",
            schema: {},
            description: "Request body for POST/PUT/PATCH requests",
            required: false
          },
          {
            name: "params",
            type: "object",
            schema: {},
            description: "Query parameters for the request",
            required: false
          },
          {
            name: "headers",
            type: "object",
            schema: {},
            description: "Additional headers to include in the request",
            required: false
          },
          {
            name: "timeout",
            type: "number",
            schema: {},
            description: "Timeout for the request in seconds",
            required: false
          }
        ],
        outputs: [
          {
            type: "object",
            description: "API response with status code and data",
            required: true
          },
          {
            type: "object",
            description: "Status of the operation",
            required: true
          }
        ],
        asynchronous: true
      },
      {
        name: "contract",
        description: "Get a copy of the tool's contract specification",
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
        description: "Get a copy of the tool's configuration requirements",
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

  private static readonly _requirements: Requirement[] = []

  private _configuration: Record<string, any>
  private _defaultHeaders: Record<string, string>
  private _lastRequestTime: number
  private readonly _minRequestInterval: number
  private _logger: Logger

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
    this._defaultHeaders = {
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    this._lastRequestTime = 0
    this._minRequestInterval = 2 // Minimum seconds between requests
    
    const { verbose } = this._configuration || {}
    if (typeof verbose === 'string') {
      this._logger = new Logger(LogLevel[verbose as keyof typeof LogLevel])
    } else if (typeof verbose === 'boolean') {
      this._logger = new Logger(verbose ? LogLevel.DEBUG : LogLevel.NONE)
    } else {
      this._logger = new Logger()
    }
  }

  async callApi({
    url,
    method = "GET",
    body,
    params,
    headers,
    timeout
  }: {  
    url: string,
    method?: string,
    body?: Record<string, any>,
    params?: Record<string, any>,
    headers?: Record<string, string>,
    timeout?: number
  }): Promise<[Record<string, any>, Record<string, any>]> {
    this._logger.log("[Tool Call] API Caller.callApi", { args: { url, method, body, params, headers, timeout }})

    // Throttle requests to avoid rate limiting
    const currentTime = Date.now() / 1000
    const timeSinceLastRequest = currentTime - this._lastRequestTime
    if (timeSinceLastRequest < this._minRequestInterval) {
      const delay = this._minRequestInterval - timeSinceLastRequest + (Math.random() * 1 + 0.5)
      await new Promise(resolve => setTimeout(resolve, delay * 1000))
    }

    // Merge default headers with request-specific headers
    const requestHeaders = { ...this._defaultHeaders }
    if (headers) {
      Object.assign(requestHeaders, headers)
    }

    try {
      const response = await fetch(url, {
        method,
        headers: requestHeaders,
        body: body ? JSON.stringify(body) : undefined,
        ...(params && { searchParams: new URLSearchParams(params) }),
        ...(timeout && { signal: AbortSignal.timeout(timeout * 1000) })
      })

      this._lastRequestTime = Date.now() / 1000

      // Try to parse JSON response, but handle non-JSON responses gracefully
      let data
      try {
        data = await response.json()
      } catch (error) {
        data = {
          raw_response: await response.text(),
          error: `Failed to parse JSON response: ${error}`
        }
      }

      return [
        {
          status_code: response.status,
          headers: Object.fromEntries(response.headers.entries()),
          data,
          raw_response: typeof data !== 'object' ? await response.text() : null
        },
        { status: "success" }
      ]
    } catch (error) {
      return [
        {
          error: error instanceof Error ? error.message : String(error),
          status_code: 500,
          details: {
            url,
            method,
            error_type: error instanceof Error ? error.constructor.name : 'Unknown'
          }
        },
        { status: "error" }
      ]
    }
  }
} 