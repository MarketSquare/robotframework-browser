/*
 * Idea from https://github.com/norbornen/execution-time-decorator/
 */
// eslint-disable-next-line @typescript-eslint/ban-types
export function class_async_timer(target: Function) {
    for (const propertyName of Object.keys(target.prototype)) {
        const descriptor = Object.getOwnPropertyDescriptor(target.prototype, propertyName);
        const isMethod = descriptor?.value instanceof Function;
        if (!isMethod || !descriptor) continue;

        const timered_method = async_timer(descriptor.value, propertyName, descriptor);
        Object.defineProperty(target.prototype, propertyName, timered_method);
    }
}

export function async_timer(
    target: any,
    propertyKey: string,
    propertyDescriptor: PropertyDescriptor,
): PropertyDescriptor {
    if (propertyDescriptor === undefined) {
        propertyDescriptor = Object.getOwnPropertyDescriptor(target, propertyKey)!;
    }
    const timername =
        (target instanceof Function ? `static ${target.name}` : target.constructor.name) + `::${propertyKey}`;
    const originalMethod = propertyDescriptor.value;
    propertyDescriptor.value = async function (...args: any[]) {
        const t0 = new Date().valueOf();
        console.log(`[timer] [${timername}]: begin`);
        try {
            const result = await originalMethod.apply(this, args);
            console.log(`[timer] [${timername}]: timer ${((new Date().valueOf() - t0) * 0.001).toFixed(3)}s`);
            return result;
        } catch (err) {
            console.log(`[timer] [${timername}]: timer ${((new Date().valueOf() - t0) * 0.001).toFixed(3)}s`);
            throw err;
        }
    };
    return propertyDescriptor;
}

export function async_hrtimer(target: any, propertyKey: string, propertyDescriptor: PropertyDescriptor) {
    if (propertyDescriptor === undefined) {
        propertyDescriptor = Object.getOwnPropertyDescriptor(target, propertyKey)!;
    }
    const timername =
        (target instanceof Function ? `static ${target.name}` : target.constructor.name) + `::${propertyKey}`;
    const originalMethod = propertyDescriptor.value;
    propertyDescriptor.value = async function (...args: any[]) {
        const t0 = process.hrtime.bigint();
        console.log(`[hrtimer] [${timername}]: begin`);
        try {
            const result = await originalMethod.apply(this, args);
            console.log(`[hrtimer] [${timername}]: timer ${process.hrtime.bigint() - t0}ns`);
            return result;
        } catch (err) {
            console.log(`[hrtimer] [${timername}]: timer ${process.hrtime.bigint() - t0}ns`);
            throw err;
        }
    };
    return propertyDescriptor;
}
