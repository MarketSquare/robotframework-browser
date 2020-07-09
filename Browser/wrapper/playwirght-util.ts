import { sendUnaryData } from 'grpc';

// This is necessary for improved typescript inference
/*
 * If obj is not trueish call callback with new Error containing message
 */
export function exists<T1, T2>(obj: T1, callback: sendUnaryData<T2>, message: string): asserts obj is NonNullable<T1> {
    if (!obj) {
        callback(new Error(message), null);
    }
}

export async function invokePlaywright(page: any, callback: any, methodName: any, ...args: any[]) {
    exists(page, callback, `Tried to do playwirght action '${methodName}', but no open browser.`);
    const fn = page[methodName].bind(page);
    try {
        return await fn(...args);
    } catch (e) {
        console.log(`Error invoking Playwright action '${methodName}': ${e}`);
        callback(e, null);
    }
}
