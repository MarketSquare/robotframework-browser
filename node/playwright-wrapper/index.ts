// Copyright 2020-     Robot Framework Foundation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { PlaywrightServer } from './grpc-service';
import { Server, ServerCredentials, ServiceDefinition, UntypedServiceImplementation } from '@grpc/grpc-js';

import * as pino from 'pino';
import { PlaywrightService } from './generated/playwright_grpc_pb';
const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

const port = process.argv.slice(2);
if (Object.keys(port).length == 0) {
    throw new Error(`No port defined`);
}
const server = new Server();
server.addService(
    PlaywrightService as unknown as ServiceDefinition<UntypedServiceImplementation>,
    new PlaywrightServer() as unknown as UntypedServiceImplementation,
);
server.bindAsync(`localhost:${port}`, ServerCredentials.createInsecure(), () => {
    logger.info(`Listening on ${port}`);
    server.start();
});
