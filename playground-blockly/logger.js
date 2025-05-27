// Centralized logger configuration for the Blockly playground
import pino from 'pino';

// Create a single logger instance with browser-friendly configuration
const logger = pino({
    level: 'debug',
    browser: {
        serialize: true,
        asObject: false,
        transmit: {
            send: function (level, logEvent) {
                const msg = logEvent.messages.join(' ');
                const levelStyles = {
                    10: 'color: #999', // trace - gray
                    20: 'color: #0088cc', // debug - blue
                    30: 'color: #44bb44', // info - green
                    40: 'color: #ff8800', // warn - orange
                    50: 'color: #ff4444', // error - red
                    60: 'color: #ff00ff'  // fatal - magenta
                };
                const levelNames = {
                    10: 'TRACE',
                    20: 'DEBUG',
                    30: 'INFO',
                    40: 'WARN',
                    50: 'ERROR',
                    60: 'FATAL'
                };
                const style = levelStyles[logEvent.level] || '';
                const timestamp = new Date().toISOString().split('T')[1].slice(0, -1); // Just time, not full date
                
                // Use console methods that match the log level for better browser integration
                const consoleMethods = {
                    10: 'debug',
                    20: 'debug',
                    30: 'info',
                    40: 'warn',
                    50: 'error',
                    60: 'error'
                };
                const method = consoleMethods[logEvent.level] || 'log';
                
                console[method](
                    `%c${levelNames[logEvent.level]} %c[${timestamp}]%c ${msg}`,
                    `${style}; font-weight: bold; padding: 2px 4px; border-radius: 2px; background: ${style.replace('color:', '')}22`,
                    'color: #666; font-size: 0.9em',
                    'color: inherit'
                );
            }
        }
    }
});

// Create a fallback logger for non-module contexts (like custom-blocks.js)
export const createFallbackLogger = (prefix = '') => ({
    trace: (...args) => console.debug('%cTRACE%c', 'color: #999; font-weight: bold', 'color: inherit', prefix, ...args),
    debug: (...args) => console.debug('%cDEBUG%c', 'color: #0088cc; font-weight: bold', 'color: inherit', prefix, ...args),
    info: (...args) => console.info('%cINFO%c', 'color: #44bb44; font-weight: bold', 'color: inherit', prefix, ...args),
    warn: (...args) => console.warn('%cWARN%c', 'color: #ff8800; font-weight: bold', 'color: inherit', prefix, ...args),
    error: (...args) => console.error('%cERROR%c', 'color: #ff4444; font-weight: bold', 'color: inherit', prefix, ...args),
    fatal: (...args) => console.error('%cFATAL%c', 'color: #ff00ff; font-weight: bold', 'color: inherit', prefix, ...args)
});

// Export the logger as default
export default logger;

// Also expose it globally for non-module scripts
if (typeof window !== 'undefined') {
    window.logger = logger;
    window.createFallbackLogger = createFallbackLogger;
}