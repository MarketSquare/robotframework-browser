import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { BrowserContext } from 'playwright';

import { Response, Request } from './generated/playwright_pb';
import { stringResponse } from './response-util';

export async function getCookies(
    call: ServerUnaryCall<Request.Empty>,
    callback: sendUnaryData<Response.String>,
    context: BrowserContext | undefined,
) {
    callback(null, stringResponse('foobar'));
}
