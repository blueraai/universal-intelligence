export interface Message {
  role: string;
  content: any;
}

export interface Schema {
  maxLength?: number;
  pattern?: string;
  minLength?: number;
  nested?: Argument[];
  properties?: Record<string, Schema>;
  items?: Schema;
  oneOf?: any[];
}

export interface Argument {
  name: string;
  type: string;
  schema?: Schema;
  description: string;
  required: boolean;
}

export interface Output {
  type: string;
  description: string;
  required: boolean;
  schema?: Schema;
}

export interface Method {
  name: string;
  description: string;
  arguments: Argument[];
  outputs: Output[];
  asynchronous?: boolean;
}

export interface Contract {
  name: string;
  description: string;
  methods: Method[];
}

export interface Requirement {
  name: string;
  type: string;
  schema: Schema;
  description: string;
  required: boolean;
}

export interface Compatibility {
  engine: string;
  quantization: string;
  devices: string[];
  memory: number;
  dependencies: string[];
  precision: number;
}

export interface QuantizationSettings {
  default?: string;
  minPrecision?: string;
  maxPrecision?: string;
} 