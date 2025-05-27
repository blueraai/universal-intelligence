// Centralized logger configuration for the Blockly playground
import pino from 'pino';

// For browser environments, we need to use CSS styling since ANSI codes don't work
const isBrowser = typeof window !== 'undefined';

// Create appropriate logger based on environment
const logger = isBrowser ? 
    // Browser logger with CSS styling
    pino({
        level: 'trace',  // Set to trace to ensure all levels are captured
        browser: {
            serialize: true,
            asObject: false,
            transmit: {
                send: function (level, logEvent) {
                    // level.value contains the numeric level
                    const levelStyles = {
                        10: { label: 'TRACE', color: '#999', method: 'log' },
                        20: { label: 'DEBUG', color: '#0099ff', method: 'log' },
                        30: { label: 'INFO', color: '#00cc00', method: 'log' },
                        40: { label: 'WARN', color: '#ff9900', method: 'warn' },
                        50: { label: 'ERROR', color: '#ff0000', method: 'error' },
                        60: { label: 'FATAL', color: '#ff00ff', method: 'error' }
                    };
                    
                    const style = levelStyles[level.value] || { label: 'LOG', color: '#666', method: 'log' };
                    const args = logEvent.messages || [];
                    
                    console[style.method](
                        `%c[${style.label}]%c`,
                        `color: ${style.color}; font-weight: bold`,
                        '',
                        ...args
                    );
                }
            }
        }
    }) :
    // Node.js logger with pino-pretty
    pino({
        level: 'debug',
        transport: {
            target: 'pino-pretty',
            options: {
                colorize: true,
                translateTime: 'HH:MM:ss',
                ignore: 'pid,hostname'
            }
        }
    });

// Create a fallback logger for non-module contexts (like custom-blocks.js)
export const createFallbackLogger = (prefix = '') => ({
    trace: (...args) => console.log('%c[TRACE]%c', 'color: #999; font-weight: bold', '', prefix, ...args),
    debug: (...args) => console.log('%c[DEBUG]%c', 'color: #0099ff; font-weight: bold', '', prefix, ...args),
    info: (...args) => console.log('%c[INFO]%c', 'color: #00cc00; font-weight: bold', '', prefix, ...args),
    warn: (...args) => console.warn('%c[WARN]%c', 'color: #ff9900; font-weight: bold', '', prefix, ...args),
    error: (...args) => console.error('%c[ERROR]%c', 'color: #ff0000; font-weight: bold', '', prefix, ...args),
    fatal: (...args) => console.error('%c[FATAL]%c', 'color: #ff00ff; font-weight: bold', '', prefix, ...args)
});

// Export the logger as default
export default logger;

// Also expose it globally for non-module scripts
if (typeof window !== 'undefined') {
    window.logger = logger;
    window.createFallbackLogger = createFallbackLogger;
}