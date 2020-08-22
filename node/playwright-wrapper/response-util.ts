import { Response } from './generated/playwright_pb';

export function emptyWithLog(text: string): Response.Empty {
    const response = new Response.Empty();
    response.setLog(text);
    return response;
}

export function stringResponse(body: string, logMessage: string) {
    const response = new Response.String();
    response.setBody(body);
    response.setLog(logMessage);
    return response;
}

export function jsonResponse(body: string, logMessage: string) {
    const response = new Response.Json();
    response.setJson(body);
    response.setLog(logMessage);
    return response;
}

export function intResponse(body: number, logMessage: string) {
    const response = new Response.Int();
    response.setBody(body);
    response.setLog(logMessage);
    return response;
}

export function boolResponse(value: boolean, logMessage: string) {
    const response = new Response.Bool();
    response.setBody(value);
    response.setLog(logMessage);
    return response;
}

export function jsResponse(result: string, logMessage: string) {
    const response = new Response.JavascriptExecutionResult();
    response.setResult(JSON.stringify(result));
    return response;
}
