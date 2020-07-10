import { sendUnaryData } from 'grpc';
import { Page } from 'playwright';

// This is necessary for improved typescript inference
/*
 * If obj is not trueish call callback with new Error containing message
 */
export function exists<T1, T2>(obj: T1, callback: sendUnaryData<T2>, message: string): asserts obj is NonNullable<T1> {
    if (!obj) {
        callback(new Error(message), null);
    }
}

function pageExists<T>(page: Page | undefined, callback: sendUnaryData<T>, message: string) {
    exists(page, callback, message);
}

export async function invokeOnPage(page: Page | undefined, callback: any, methodName: string, ...args: any[]) {
    pageExists(page, callback, `Tried to do playwirght action '${methodName}', but no open browser.`);
    const fn: any = (page as { [key: string]: any })[methodName].bind(page);
    try {
        return await fn(...args);
    } catch (e) {
        console.log(`Error invoking Playwright action '${methodName}': ${e}`);
        callback(e, null);
    }
}
