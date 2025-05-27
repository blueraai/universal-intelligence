// Centralized logger configuration for the Blockly playground
import pino from 'pino';

// Create a logger that works in the browser with colors
const logger = pino({
    level: 'trace',
    browser: {
        serialize: false,
        asObject: false
    },
    hooks: {
        logMethod(inputArgs, method) {
            // Handle multiple arguments properly
            const args = Array.from(inputArgs);
            const level = method.name;
            
            // Map pino levels to console methods and colors
            const levelMap = {
                trace: { console: 'log', color: 'color: #999', label: 'TRACE' },
                debug: { console: 'log', color: 'color: #0099ff', label: 'DEBUG' },
                info: { console: 'log', color: 'color: #00cc00', label: 'INFO' },
                warn: { console: 'warn', color: 'color: #ff9900', label: 'WARN' },
                error: { console: 'error', color: 'color: #ff0000', label: 'ERROR' },
                fatal: { console: 'error', color: 'color: #ff00ff', label: 'FATAL' }
            };
            
            const config = levelMap[level] || { console: 'log', color: 'color: #666', label: 'LOG' };
            
            // Output with colors using CSS styling
            console[config.console](
                `%c[${config.label}]%c`,
                `${config.color}; font-weight: bold`,
                'color: inherit',
                ...args
            );
            
            return method.apply(this, inputArgs);
        }
    }
});

// Create a fallback logger for non-module contexts (like custom-blocks.js)
export const createFallbackLogger = (prefix = '') => ({
    trace: (...args) => console.log('%c[TRACE]%c', 'color: #999; font-weight: bold', 'color: inherit', prefix, ...args),
    debug: (...args) => console.log('%c[DEBUG]%c', 'color: #0099ff; font-weight: bold', 'color: inherit', prefix, ...args),
    info: (...args) => console.log('%c[INFO]%c', 'color: #00cc00; font-weight: bold', 'color: inherit', prefix, ...args),
    warn: (...args) => console.warn('%c[WARN]%c', 'color: #ff9900; font-weight: bold', 'color: inherit', prefix, ...args),
    error: (...args) => console.error('%c[ERROR]%c', 'color: #ff0000; font-weight: bold', 'color: inherit', prefix, ...args),
    fatal: (...args) => console.error('%c[FATAL]%c', 'color: #ff00ff; font-weight: bold', 'color: inherit', prefix, ...args)
});

// Export the logger as default
export default logger;

// Also expose it globally for non-module scripts
if (typeof window !== 'undefined') {
    window.logger = logger;
    window.createFallbackLogger = createFallbackLogger;
}