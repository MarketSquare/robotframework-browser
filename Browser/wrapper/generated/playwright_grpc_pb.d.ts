// package: 
// file: playwright.proto

/* tslint:disable */
/* eslint-disable */

import * as grpc from "grpc";
import * as playwright_pb from "./playwright_pb";

interface IPlaywrightService extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
    screenshot: IPlaywrightService_IScreenshot;
    openBrowser: IPlaywrightService_IOpenBrowser;
    closeBrowser: IPlaywrightService_ICloseBrowser;
    goTo: IPlaywrightService_IGoTo;
    getTitle: IPlaywrightService_IGetTitle;
    inputText: IPlaywrightService_IInputText;
    getDomProperty: IPlaywrightService_IGetDomProperty;
    getBoolProperty: IPlaywrightService_IGetBoolProperty;
    getTextContent: IPlaywrightService_IGetTextContent;
    getUrl: IPlaywrightService_IGetUrl;
    clickButton: IPlaywrightService_IClickButton;
    checkCheckbox: IPlaywrightService_ICheckCheckbox;
    uncheckCheckbox: IPlaywrightService_IUncheckCheckbox;
    health: IPlaywrightService_IHealth;
}

interface IPlaywrightService_IScreenshot extends grpc.MethodDefinition<playwright_pb.Request.screenshot, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/Screenshot"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.screenshot>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.screenshot>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IOpenBrowser extends grpc.MethodDefinition<playwright_pb.Request.openBrowser, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/OpenBrowser"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.openBrowser>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.openBrowser>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_ICloseBrowser extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/CloseBrowser"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGoTo extends grpc.MethodDefinition<playwright_pb.Request.goTo, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/GoTo"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.goTo>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.goTo>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGetTitle extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.String> {
    path: string; // "/.Playwright/GetTitle"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IInputText extends grpc.MethodDefinition<playwright_pb.Request.inputText, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/InputText"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.inputText>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.inputText>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGetDomProperty extends grpc.MethodDefinition<playwright_pb.Request.getDomProperty, playwright_pb.Response.String> {
    path: string; // "/.Playwright/GetDomProperty"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.getDomProperty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.getDomProperty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IGetBoolProperty extends grpc.MethodDefinition<playwright_pb.Request.getDomProperty, playwright_pb.Response.Bool> {
    path: string; // "/.Playwright/GetBoolProperty"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.getDomProperty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.getDomProperty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Bool>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Bool>;
}
interface IPlaywrightService_IGetTextContent extends grpc.MethodDefinition<playwright_pb.Request.selector, playwright_pb.Response.String> {
    path: string; // "/.Playwright/GetTextContent"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.selector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.selector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IGetUrl extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.String> {
    path: string; // "/.Playwright/GetUrl"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IClickButton extends grpc.MethodDefinition<playwright_pb.Request.selector, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/ClickButton"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.selector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.selector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_ICheckCheckbox extends grpc.MethodDefinition<playwright_pb.Request.selector, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/CheckCheckbox"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.selector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.selector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IUncheckCheckbox extends grpc.MethodDefinition<playwright_pb.Request.selector, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/UncheckCheckbox"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.selector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.selector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IHealth extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.String> {
    path: string; // "/.Playwright/Health"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}

export const PlaywrightService: IPlaywrightService;

export interface IPlaywrightServer {
    screenshot: grpc.handleUnaryCall<playwright_pb.Request.screenshot, playwright_pb.Response.Empty>;
    openBrowser: grpc.handleUnaryCall<playwright_pb.Request.openBrowser, playwright_pb.Response.Empty>;
    closeBrowser: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Empty>;
    goTo: grpc.handleUnaryCall<playwright_pb.Request.goTo, playwright_pb.Response.Empty>;
    getTitle: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.String>;
    inputText: grpc.handleUnaryCall<playwright_pb.Request.inputText, playwright_pb.Response.Empty>;
    getDomProperty: grpc.handleUnaryCall<playwright_pb.Request.getDomProperty, playwright_pb.Response.String>;
    getBoolProperty: grpc.handleUnaryCall<playwright_pb.Request.getDomProperty, playwright_pb.Response.Bool>;
    getTextContent: grpc.handleUnaryCall<playwright_pb.Request.selector, playwright_pb.Response.String>;
    getUrl: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.String>;
    clickButton: grpc.handleUnaryCall<playwright_pb.Request.selector, playwright_pb.Response.Empty>;
    checkCheckbox: grpc.handleUnaryCall<playwright_pb.Request.selector, playwright_pb.Response.Empty>;
    uncheckCheckbox: grpc.handleUnaryCall<playwright_pb.Request.selector, playwright_pb.Response.Empty>;
    health: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.String>;
}

export interface IPlaywrightClient {
    screenshot(request: playwright_pb.Request.screenshot, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    screenshot(request: playwright_pb.Request.screenshot, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    screenshot(request: playwright_pb.Request.screenshot, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    openBrowser(request: playwright_pb.Request.openBrowser, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    openBrowser(request: playwright_pb.Request.openBrowser, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    openBrowser(request: playwright_pb.Request.openBrowser, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeBrowser(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeBrowser(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeBrowser(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    goTo(request: playwright_pb.Request.goTo, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    goTo(request: playwright_pb.Request.goTo, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    goTo(request: playwright_pb.Request.goTo, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    getTitle(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getTitle(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getTitle(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    inputText(request: playwright_pb.Request.inputText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    inputText(request: playwright_pb.Request.inputText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    inputText(request: playwright_pb.Request.inputText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    getDomProperty(request: playwright_pb.Request.getDomProperty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getDomProperty(request: playwright_pb.Request.getDomProperty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getDomProperty(request: playwright_pb.Request.getDomProperty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getBoolProperty(request: playwright_pb.Request.getDomProperty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Bool) => void): grpc.ClientUnaryCall;
    getBoolProperty(request: playwright_pb.Request.getDomProperty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Bool) => void): grpc.ClientUnaryCall;
    getBoolProperty(request: playwright_pb.Request.getDomProperty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Bool) => void): grpc.ClientUnaryCall;
    getTextContent(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getTextContent(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getTextContent(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getUrl(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getUrl(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getUrl(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    clickButton(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clickButton(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clickButton(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    checkCheckbox(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    checkCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    checkCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    uncheckCheckbox(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    uncheckCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    uncheckCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    health(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    health(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    health(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
}

export class PlaywrightClient extends grpc.Client implements IPlaywrightClient {
    constructor(address: string, credentials: grpc.ChannelCredentials, options?: object);
    public screenshot(request: playwright_pb.Request.screenshot, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public screenshot(request: playwright_pb.Request.screenshot, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public screenshot(request: playwright_pb.Request.screenshot, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public openBrowser(request: playwright_pb.Request.openBrowser, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public openBrowser(request: playwright_pb.Request.openBrowser, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public openBrowser(request: playwright_pb.Request.openBrowser, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeBrowser(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeBrowser(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeBrowser(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public goTo(request: playwright_pb.Request.goTo, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public goTo(request: playwright_pb.Request.goTo, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public goTo(request: playwright_pb.Request.goTo, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public getTitle(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getTitle(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getTitle(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public inputText(request: playwright_pb.Request.inputText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public inputText(request: playwright_pb.Request.inputText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public inputText(request: playwright_pb.Request.inputText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public getDomProperty(request: playwright_pb.Request.getDomProperty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getDomProperty(request: playwright_pb.Request.getDomProperty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getDomProperty(request: playwright_pb.Request.getDomProperty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getBoolProperty(request: playwright_pb.Request.getDomProperty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Bool) => void): grpc.ClientUnaryCall;
    public getBoolProperty(request: playwright_pb.Request.getDomProperty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Bool) => void): grpc.ClientUnaryCall;
    public getBoolProperty(request: playwright_pb.Request.getDomProperty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Bool) => void): grpc.ClientUnaryCall;
    public getTextContent(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getTextContent(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getTextContent(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getUrl(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getUrl(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getUrl(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public clickButton(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clickButton(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clickButton(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public checkCheckbox(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public checkCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public checkCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public uncheckCheckbox(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public uncheckCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public uncheckCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public health(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public health(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public health(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
}
