import { devices } from 'playwright';

import { ServerUnaryCall, sendUnaryData } from 'grpc';

import { Request, Response } from './generated/playwright_pb';
import { stringResponse } from './response-util';

export async function getDevice(call: ServerUnaryCall<Request.Device>, callback: sendUnaryData<Response.String>) {
    const name = call.request.getName();
    const device = devices[name];
    if (!device) callback(new Error(`No device named ${name}`), null);
    callback(null, stringResponse(JSON.stringify(device), ''));
}

export async function getDevices(callback: sendUnaryData<Response.String>) {
    callback(null, stringResponse(JSON.stringify(devices), ''));
}
