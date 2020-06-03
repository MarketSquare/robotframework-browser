import { IPlaywrightServer, PlaywrightService } from './generated/playwright_grpc_pb';
import { firefox } from 'playwright';
import * as grpc from "grpc";
import {sendUnaryData, ServerUnaryCall} from "grpc";
import {Empty} from "./generated/playwright_pb";


class PlaywrightServer implements IPlaywrightServer {
    private browser: any;
    async closeBrowser(call: ServerUnaryCall<Empty>, callback: sendUnaryData<Empty>): Promise<void> {
        await this.browser.close();
        callback(null, new Empty());
    }

    async openBrowser(call: ServerUnaryCall<Empty>, callback: sendUnaryData<Empty>): Promise<void> {
        this.browser = await firefox.launch({headless:false});
        callback(null, new Empty());
    }
}

const server = new grpc.Server();
server.addService<IPlaywrightServer>(PlaywrightService, new PlaywrightServer());
console.log(`Listening on 50051`);
server.bind(`localhost:50051`, grpc.ServerCredentials.createInsecure());
server.start();