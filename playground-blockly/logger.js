// Centralized logger configuration for the Blockly playground
import pino from 'pino';

// Simple wrapper that uses pino but formats nicely for browser
const logger = pino({
    level: 'trace',
    browser: {
        serialize: false,
        write: function(o) {
            const levelMap = {
                10: { label: 'TRACE', color: '#999', method: 'log' },
                20: { label: 'DEBUG', color: '#0099ff', method: 'log' },
                30: { label: 'INFO', color: '#00cc00', method: 'log' },
                40: { label: 'WARN', color: '#ff9900', method: 'warn' },
                50: { label: 'ERROR', color: '#ff0000', method: 'error' },
                60: { label: 'FATAL', color: '#ff00ff', method: 'error' }
            };
            
            const level = levelMap[o.level] || { label: 'LOG', color: '#666', method: 'log' };
            
            // Build the output parts
            const parts = [];
            
            // Add the main message
            if (o.msg) {
                parts.push(o.msg);
            }
            
            // Add any extra fields that were passed
            Object.keys(o).forEach(key => {
                if (!['time', 'level', 'msg', 'pid', 'hostname', 'name'].includes(key)) {
                    parts.push(`${key}:`, o[key]);
                }
            });
            
            // Output with color
            console[level.method](
                `%c[${level.label}]%c ${parts.join(' ')}`,
                `color: ${level.color}; font-weight: bold`,
                'color: inherit'
            );
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