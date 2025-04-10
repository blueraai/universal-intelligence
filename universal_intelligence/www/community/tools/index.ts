import APICaller from './api_caller'
import SimpleErrorGenerator from './simple_error_generator'
import SimplePrinter from './simple_printer'

const tools = {
  APICaller,
  SimplePrinter,
  SimpleErrorGenerator,
  Tool: SimplePrinter, // default tool
}

export default tools