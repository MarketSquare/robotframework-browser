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
