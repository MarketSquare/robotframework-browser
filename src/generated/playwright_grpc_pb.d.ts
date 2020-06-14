// package: 
// file: playwright.proto

/* tslint:disable */
/* eslint-disable */

import * as grpc from "grpc";
import * as playwright_pb from "./playwright_pb";

interface IPlaywrightService extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
    openBrowser: IPlaywrightService_IOpenBrowser;
    closeBrowser: IPlaywrightService_ICloseBrowser;
    shutdown: IPlaywrightService_IShutdown;
}

interface IPlaywrightService_IOpenBrowser extends grpc.MethodDefinition<playwright_pb.openBrowserRequest, playwright_pb.Response> {
    path: string; // "/.Playwright/OpenBrowser"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.openBrowserRequest>;
    requestDeserialize: grpc.deserialize<playwright_pb.openBrowserRequest>;
    responseSerialize: grpc.serialize<playwright_pb.Response>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response>;
}
interface IPlaywrightService_ICloseBrowser extends grpc.MethodDefinition<playwright_pb.Empty, playwright_pb.Response> {
    path: string; // "/.Playwright/CloseBrowser"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response>;
}
interface IPlaywrightService_IShutdown extends grpc.MethodDefinition<playwright_pb.Empty, playwright_pb.Response> {
    path: string; // "/.Playwright/Shutdown"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response>;
}

export const PlaywrightService: IPlaywrightService;

export interface IPlaywrightServer {
    openBrowser: grpc.handleUnaryCall<playwright_pb.openBrowserRequest, playwright_pb.Response>;
    closeBrowser: grpc.handleUnaryCall<playwright_pb.Empty, playwright_pb.Response>;
    shutdown: grpc.handleUnaryCall<playwright_pb.Empty, playwright_pb.Response>;
}

export interface IPlaywrightClient {
    openBrowser(request: playwright_pb.openBrowserRequest, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    openBrowser(request: playwright_pb.openBrowserRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    openBrowser(request: playwright_pb.openBrowserRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    closeBrowser(request: playwright_pb.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    closeBrowser(request: playwright_pb.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    closeBrowser(request: playwright_pb.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    shutdown(request: playwright_pb.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    shutdown(request: playwright_pb.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    shutdown(request: playwright_pb.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
}

export class PlaywrightClient extends grpc.Client implements IPlaywrightClient {
    constructor(address: string, credentials: grpc.ChannelCredentials, options?: object);
    public openBrowser(request: playwright_pb.openBrowserRequest, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    public openBrowser(request: playwright_pb.openBrowserRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    public openBrowser(request: playwright_pb.openBrowserRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    public closeBrowser(request: playwright_pb.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    public closeBrowser(request: playwright_pb.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    public closeBrowser(request: playwright_pb.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    public shutdown(request: playwright_pb.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    public shutdown(request: playwright_pb.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
    public shutdown(request: playwright_pb.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response) => void): grpc.ClientUnaryCall;
}
