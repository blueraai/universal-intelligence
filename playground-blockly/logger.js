// Centralized logger configuration for the Blockly playground
import pino from 'pino';

// For browser environments, we need to use CSS styling since ANSI codes don't work
const isBrowser = typeof window !== 'undefined';

// Create appropriate logger based on environment
const logger = isBrowser ? 
    // Browser logger with CSS styling
    pino({
        level: 'debug',
        browser: {
            write: {
                trace: function (o) {
                    console.log('%c[TRACE]%c', 'color: #999; font-weight: bold', '', o.msg);
                },
                debug: function (o) {
                    console.log('%c[DEBUG]%c', 'color: #0099ff; font-weight: bold', '', o.msg);
                },
                info: function (o) {
                    console.log('%c[INFO]%c', 'color: #00cc00; font-weight: bold', '', o.msg);
                },
                warn: function (o) {
                    console.warn('%c[WARN]%c', 'color: #ff9900; font-weight: bold', '', o.msg);
                },
                error: function (o) {
                    console.error('%c[ERROR]%c', 'color: #ff0000; font-weight: bold', '', o.msg);
                },
                fatal: function (o) {
                    console.error('%c[FATAL]%c', 'color: #ff00ff; font-weight: bold', '', o.msg);
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