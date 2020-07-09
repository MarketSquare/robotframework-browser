import { Response } from './generated/playwright_pb';

export function emptyWithLog(text: string): Response.Empty {
    const response = new Response.Empty();
    response.setLog(text);
    return response;
}

export function stringResponse(body: string) {
    const response = new Response.String();
    response.setBody(body);
    return response;
}

export function boolResponse(value: boolean) {
    const response = new Response.Bool();
    response.setBody(value);
    return response;
}

export function jsResponse(result: string) {
    const response = new Response.JavascriptExecutionResult();
    response.setResult(JSON.stringify(result));
    return response;
}
