import { pino } from 'pino';
const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

// Idea and async logger method from https://github.com/norbornen/execution-time-decorator/
// eslint-disable-next-line
export function class_async_logger(target: Function) {
    for (const propertyName of Object.keys(target.prototype)) {
        const descriptor = Object.getOwnPropertyDescriptor(target.prototype, propertyName);
        const isMethod = descriptor?.value instanceof Function;
        if (!isMethod || !descriptor) continue;

        const timered_method = async_logger(propertyName, descriptor);
        Object.defineProperty(target.prototype, propertyName, timered_method);
    }
}

export function async_logger(propertyKey: string, propertyDescriptor: PropertyDescriptor): PropertyDescriptor {
    const originalMethod = propertyDescriptor.value;
    propertyDescriptor.value = async function (...args: any[]) {
        try {
            logger.info(`Start of node method ${propertyKey}`);
            const result = await originalMethod.apply(this, args);
            logger.info(`End of node method ${propertyKey}`);
            return result;
        } catch (err) {
            logger.info(`Error of node method  ${propertyKey}`);
            throw err;
        }
    };
    return propertyDescriptor;
}
