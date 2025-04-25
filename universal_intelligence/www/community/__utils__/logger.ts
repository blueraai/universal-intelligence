export enum LogLevel {
  NONE = 'NONE',
  DEFAULT = 'DEFAULT',
  DEBUG = 'DEBUG'
}

export class Logger {
  private level: LogLevel

  constructor(level: LogLevel = LogLevel.DEFAULT) {
    this.level = level
  }

  private shouldLog(): boolean {
    return this.level !== LogLevel.NONE
  }

  log(...args: any[]): void {
    if (this.shouldLog()) {
      console.log(...args)
    }
  }

  info(...args: any[]): void {
    if (this.shouldLog()) {
      console.info(...args)
    }
  }

  warn(...args: any[]): void {
    if (this.shouldLog()) {
      console.warn(...args)
    }
  }

  error(...args: any[]): void {
    if (this.shouldLog()) {
      console.error(...args)
    }
  }

  debug(...args: any[]): void {
    if (this.level === LogLevel.DEBUG) {
      console.debug(...args)
    }
  }

  setLevel(level: LogLevel): void {
    this.level = level
  }

  getLevel(): LogLevel {
    return this.level
  }
}