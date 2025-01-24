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

import { PlaywrightService } from './generated/playwright_grpc_pb';
import { pino } from 'pino';
const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

const args = process.argv.slice(2);

const host = args[0];
const port = args[1];

if (!host) {
    throw new Error(`No host defined`);
}

if (!port) {
    throw new Error(`No port defined`);
}

const server = new Server();
server.addService(
    PlaywrightService as unknown as ServiceDefinition<UntypedServiceImplementation>,
    new PlaywrightServer() as unknown as UntypedServiceImplementation,
);

server.bindAsync(`${host}:${port}`, ServerCredentials.createInsecure(), () => {
    logger.info(`Listening on ${host}:${port}`);
    server.start();
});
