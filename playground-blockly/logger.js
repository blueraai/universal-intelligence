// Centralized logger configuration for the Blockly playground
import pino from 'pino';

// Create logger with pino-pretty transport
const logger = pino({
    level: 'trace',
    transport: {
        target: 'pino-pretty',
        options: {
            colorize: true,
            translateTime: false,
            ignore: 'pid,hostname',
            messageFormat: '{msg}',
            singleLine: true
        }
    }
});

// Create a fallback logger for non-module contexts (like custom-blocks.js)
export const createFallbackLogger = (prefix = '') => ({
    trace: (...args) => console.log('[TRACE]', prefix, ...args),
    debug: (...args) => console.log('[DEBUG]', prefix, ...args),
    info: (...args) => console.log('[INFO]', prefix, ...args),
    warn: (...args) => console.warn('[WARN]', prefix, ...args),
    error: (...args) => console.error('[ERROR]', prefix, ...args),
    fatal: (...args) => console.error('[FATAL]', prefix, ...args)
});

// Export the logger as default
export default logger;

// Also expose it globally for non-module scripts
if (typeof window !== 'undefined') {
    window.logger = logger;
    window.createFallbackLogger = createFallbackLogger;
}