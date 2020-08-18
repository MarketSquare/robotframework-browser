import { IPlaywrightServer, PlaywrightService } from './generated/playwright_grpc_pb';
import { PlaywrightServer } from './grpc-service';
import { Server, ServerCredentials } from 'grpc';

import * as pino from 'pino';
const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

const server = new Server();
server.addService<IPlaywrightServer>(PlaywrightService, new PlaywrightServer());
const port = process.env.PORT || '0';
server.bind(`localhost:${port}`, ServerCredentials.createInsecure());
logger.info(`Listening on ${port}`);
server.start();
