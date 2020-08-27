import { devices } from 'playwright';

import { ServerUnaryCall, sendUnaryData } from 'grpc';

import { Request, Response } from './generated/playwright_pb';
import { jsonResponse} from './response-util';

export async function getDevice(call: ServerUnaryCall<Request.Device>, callback: sendUnaryData<Response.Json>) {
    const name = call.request.getName();
    const device = devices[name];
    if (!device) callback(new Error(`No device named ${name}`), null);
    callback(null, jsonResponse(JSON.stringify(device), ''));
}

export async function getDevices(callback: sendUnaryData<Response.Json>) {
    callback(null, jsonResponse(JSON.stringify(devices), ''));
}
