import { Server, ServerCredentials } from 'grpc';

import { IPlaywrightServer, PlaywrightService } from './generated/playwright_grpc_pb';
import { PlaywrightServer } from './server';

const server = new Server();
server.addService<IPlaywrightServer>(PlaywrightService, new PlaywrightServer());
const port = process.env.PORT || '0';
server.bind(`localhost:${port}`, ServerCredentials.createInsecure());
console.log(`Listening on ${port}`);
server.start();
