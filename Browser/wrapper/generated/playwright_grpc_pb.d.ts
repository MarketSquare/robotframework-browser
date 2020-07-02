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
    typeText: IPlaywrightService_ITypeText;
    fillText: IPlaywrightService_IFillText;
    clearText: IPlaywrightService_IClearText;
    getDomProperty: IPlaywrightService_IGetDomProperty;
    getBoolProperty: IPlaywrightService_IGetBoolProperty;
    getTextContent: IPlaywrightService_IGetTextContent;
    getUrl: IPlaywrightService_IGetUrl;
    click: IPlaywrightService_IClick;
    press: IPlaywrightService_IPress;
    checkCheckbox: IPlaywrightService_ICheckCheckbox;
    uncheckCheckbox: IPlaywrightService_IUncheckCheckbox;
    health: IPlaywrightService_IHealth;
    setTimeout: IPlaywrightService_ISetTimeout;
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
interface IPlaywrightService_ITypeText extends grpc.MethodDefinition<playwright_pb.Request.typeText, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/TypeText"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.typeText>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.typeText>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IFillText extends grpc.MethodDefinition<playwright_pb.Request.fillText, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/FillText"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.fillText>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.fillText>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IClearText extends grpc.MethodDefinition<playwright_pb.Request.clearText, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/ClearText"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.clearText>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.clearText>;
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
interface IPlaywrightService_IClick extends grpc.MethodDefinition<playwright_pb.Request.selector, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/Click"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.selector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.selector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IPress extends grpc.MethodDefinition<playwright_pb.Request.press, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/Press"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.press>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.press>;
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
interface IPlaywrightService_ISetTimeout extends grpc.MethodDefinition<playwright_pb.Request.timeout, playwright_pb.Response.Empty> {
    path: string; // "/.Playwright/SetTimeout"
    requestStream: boolean; // false
    responseStream: boolean; // false
    requestSerialize: grpc.serialize<playwright_pb.Request.timeout>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.timeout>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}

export const PlaywrightService: IPlaywrightService;

export interface IPlaywrightServer {
    screenshot: grpc.handleUnaryCall<playwright_pb.Request.screenshot, playwright_pb.Response.Empty>;
    openBrowser: grpc.handleUnaryCall<playwright_pb.Request.openBrowser, playwright_pb.Response.Empty>;
    closeBrowser: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Empty>;
    goTo: grpc.handleUnaryCall<playwright_pb.Request.goTo, playwright_pb.Response.Empty>;
    getTitle: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.String>;
    inputText: grpc.handleUnaryCall<playwright_pb.Request.inputText, playwright_pb.Response.Empty>;
    typeText: grpc.handleUnaryCall<playwright_pb.Request.typeText, playwright_pb.Response.Empty>;
    fillText: grpc.handleUnaryCall<playwright_pb.Request.fillText, playwright_pb.Response.Empty>;
    clearText: grpc.handleUnaryCall<playwright_pb.Request.clearText, playwright_pb.Response.Empty>;
    getDomProperty: grpc.handleUnaryCall<playwright_pb.Request.getDomProperty, playwright_pb.Response.String>;
    getBoolProperty: grpc.handleUnaryCall<playwright_pb.Request.getDomProperty, playwright_pb.Response.Bool>;
    getTextContent: grpc.handleUnaryCall<playwright_pb.Request.selector, playwright_pb.Response.String>;
    getUrl: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.String>;
    click: grpc.handleUnaryCall<playwright_pb.Request.selector, playwright_pb.Response.Empty>;
    press: grpc.handleUnaryCall<playwright_pb.Request.press, playwright_pb.Response.Empty>;
    checkCheckbox: grpc.handleUnaryCall<playwright_pb.Request.selector, playwright_pb.Response.Empty>;
    uncheckCheckbox: grpc.handleUnaryCall<playwright_pb.Request.selector, playwright_pb.Response.Empty>;
    health: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.String>;
    setTimeout: grpc.handleUnaryCall<playwright_pb.Request.timeout, playwright_pb.Response.Empty>;
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
    typeText(request: playwright_pb.Request.typeText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    typeText(request: playwright_pb.Request.typeText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    typeText(request: playwright_pb.Request.typeText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    fillText(request: playwright_pb.Request.fillText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    fillText(request: playwright_pb.Request.fillText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    fillText(request: playwright_pb.Request.fillText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clearText(request: playwright_pb.Request.clearText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clearText(request: playwright_pb.Request.clearText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clearText(request: playwright_pb.Request.clearText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
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
    click(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    click(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    click(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    press(request: playwright_pb.Request.press, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    press(request: playwright_pb.Request.press, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    press(request: playwright_pb.Request.press, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    checkCheckbox(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    checkCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    checkCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    uncheckCheckbox(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    uncheckCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    uncheckCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    health(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    health(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    health(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    setTimeout(request: playwright_pb.Request.timeout, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setTimeout(request: playwright_pb.Request.timeout, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setTimeout(request: playwright_pb.Request.timeout, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
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
    public typeText(request: playwright_pb.Request.typeText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public typeText(request: playwright_pb.Request.typeText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public typeText(request: playwright_pb.Request.typeText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public fillText(request: playwright_pb.Request.fillText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public fillText(request: playwright_pb.Request.fillText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public fillText(request: playwright_pb.Request.fillText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clearText(request: playwright_pb.Request.clearText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clearText(request: playwright_pb.Request.clearText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clearText(request: playwright_pb.Request.clearText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
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
    public click(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public click(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public click(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public press(request: playwright_pb.Request.press, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public press(request: playwright_pb.Request.press, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public press(request: playwright_pb.Request.press, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public checkCheckbox(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public checkCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public checkCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public uncheckCheckbox(request: playwright_pb.Request.selector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public uncheckCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public uncheckCheckbox(request: playwright_pb.Request.selector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public health(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public health(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public health(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public setTimeout(request: playwright_pb.Request.timeout, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setTimeout(request: playwright_pb.Request.timeout, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setTimeout(request: playwright_pb.Request.timeout, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
}
