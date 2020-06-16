// package: 
// file: playwright.proto

/* tslint:disable */
/* eslint-disable */

import * as grpc from "grpc";
import * as playwright_pb from "./playwright_pb";

interface IPlaywrightService extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
    openBrowser: IPlaywrightService_IOpenBrowser;
    closeBrowser: IPlaywrightService_ICloseBrowser;
    goTo: IPlaywrightService_IGoTo;
    getTitle: IPlaywrightService_IGetTitle;
    inputText: IPlaywrightService_IInputText;
    getText: IPlaywrightService_IGetText;
}

interface IPlaywrightService_IOpenBrowser extends grpc.MethodDefinition<playwright_pb.openBrowserRequest, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/OpenBrowser"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.openBrowserRequest>;
    requestDeserialize: grpc.deserialize<playwright_pb.openBrowserRequest>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_ICloseBrowser extends grpc.MethodDefinition<playwright_pb.Empty, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/CloseBrowser"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGoTo extends grpc.MethodDefinition<playwright_pb.goToRequest, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/GoTo"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.goToRequest>;
    requestDeserialize: grpc.deserialize<playwright_pb.goToRequest>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGetTitle extends grpc.MethodDefinition<playwright_pb.Empty, playwright_pb.Response.String> {
    path: string; // "/.Playwright/GetTitle"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IInputText extends grpc.MethodDefinition<playwright_pb.inputTextRequest, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/InputText"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.inputTextRequest>;
    requestDeserialize: grpc.deserialize<playwright_pb.inputTextRequest>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGetText extends grpc.MethodDefinition<playwright_pb.selectorRequest, playwright_pb.Response.String> {
    path: string; // "/.Playwright/GetText"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.selectorRequest>;
    requestDeserialize: grpc.deserialize<playwright_pb.selectorRequest>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}

export const PlaywrightService: IPlaywrightService;

export interface IPlaywrightServer {
    openBrowser: grpc.handleUnaryCall<playwright_pb.openBrowserRequest, playwright_pb.Response.Empty>;
    closeBrowser: grpc.handleUnaryCall<playwright_pb.Empty, playwright_pb.Response.Empty>;
    goTo: grpc.handleUnaryCall<playwright_pb.goToRequest, playwright_pb.Response.Empty>;
    getTitle: grpc.handleUnaryCall<playwright_pb.Empty, playwright_pb.Response.String>;
    inputText: grpc.handleUnaryCall<playwright_pb.inputTextRequest, playwright_pb.Response.Empty>;
    getText: grpc.handleUnaryCall<playwright_pb.selectorRequest, playwright_pb.Response.String>;
}

export interface IPlaywrightClient {
    openBrowser(request: playwright_pb.openBrowserRequest, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    openBrowser(request: playwright_pb.openBrowserRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    openBrowser(request: playwright_pb.openBrowserRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeBrowser(request: playwright_pb.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeBrowser(request: playwright_pb.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeBrowser(request: playwright_pb.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    goTo(request: playwright_pb.goToRequest, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    goTo(request: playwright_pb.goToRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    goTo(request: playwright_pb.goToRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    getTitle(request: playwright_pb.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getTitle(request: playwright_pb.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getTitle(request: playwright_pb.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    inputText(request: playwright_pb.inputTextRequest, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    inputText(request: playwright_pb.inputTextRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    inputText(request: playwright_pb.inputTextRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    getText(request: playwright_pb.selectorRequest, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getText(request: playwright_pb.selectorRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getText(request: playwright_pb.selectorRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
}

export class PlaywrightClient extends grpc.Client implements IPlaywrightClient {
    constructor(address: string, credentials: grpc.ChannelCredentials, options?: object);
    public openBrowser(request: playwright_pb.openBrowserRequest, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public openBrowser(request: playwright_pb.openBrowserRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public openBrowser(request: playwright_pb.openBrowserRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeBrowser(request: playwright_pb.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeBrowser(request: playwright_pb.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeBrowser(request: playwright_pb.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public goTo(request: playwright_pb.goToRequest, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public goTo(request: playwright_pb.goToRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public goTo(request: playwright_pb.goToRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public getTitle(request: playwright_pb.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getTitle(request: playwright_pb.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getTitle(request: playwright_pb.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public inputText(request: playwright_pb.inputTextRequest, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public inputText(request: playwright_pb.inputTextRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public inputText(request: playwright_pb.inputTextRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public getText(request: playwright_pb.selectorRequest, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getText(request: playwright_pb.selectorRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getText(request: playwright_pb.selectorRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
}
