// package: 
// file: playwright.proto

/* tslint:disable */
/* eslint-disable */

import * as grpc from "grpc";
import * as playwright_pb from "./playwright_pb";

interface IPlaywrightService extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
    ariaSnapShot: IPlaywrightService_IAriaSnapShot;
    addCookie: IPlaywrightService_IAddCookie;
    getCookies: IPlaywrightService_IGetCookies;
    deleteAllCookies: IPlaywrightService_IDeleteAllCookies;
    takeScreenshot: IPlaywrightService_ITakeScreenshot;
    goTo: IPlaywrightService_IGoTo;
    goBack: IPlaywrightService_IGoBack;
    goForward: IPlaywrightService_IGoForward;
    getTitle: IPlaywrightService_IGetTitle;
    getElementCount: IPlaywrightService_IGetElementCount;
    typeText: IPlaywrightService_ITypeText;
    fillText: IPlaywrightService_IFillText;
    clearText: IPlaywrightService_IClearText;
    getDomProperty: IPlaywrightService_IGetDomProperty;
    getText: IPlaywrightService_IGetText;
    getElementAttribute: IPlaywrightService_IGetElementAttribute;
    getBoolProperty: IPlaywrightService_IGetBoolProperty;
    getViewportSize: IPlaywrightService_IGetViewportSize;
    getUrl: IPlaywrightService_IGetUrl;
    getPageSource: IPlaywrightService_IGetPageSource;
    press: IPlaywrightService_IPress;
    getSelectContent: IPlaywrightService_IGetSelectContent;
    selectOption: IPlaywrightService_ISelectOption;
    deselectOption: IPlaywrightService_IDeselectOption;
    checkCheckbox: IPlaywrightService_ICheckCheckbox;
    uncheckCheckbox: IPlaywrightService_IUncheckCheckbox;
    health: IPlaywrightService_IHealth;
    getElement: IPlaywrightService_IGetElement;
    getElements: IPlaywrightService_IGetElements;
    getByX: IPlaywrightService_IGetByX;
    getElementStates: IPlaywrightService_IGetElementStates;
    setTimeout: IPlaywrightService_ISetTimeout;
    addStyleTag: IPlaywrightService_IAddStyleTag;
    highlightElements: IPlaywrightService_IHighlightElements;
    download: IPlaywrightService_IDownload;
    click: IPlaywrightService_IClick;
    tap: IPlaywrightService_ITap;
    hover: IPlaywrightService_IHover;
    focus: IPlaywrightService_IFocus;
    waitForElementsState: IPlaywrightService_IWaitForElementsState;
    waitForFunction: IPlaywrightService_IWaitForFunction;
    evaluateJavascript: IPlaywrightService_IEvaluateJavascript;
    recordSelector: IPlaywrightService_IRecordSelector;
    setViewportSize: IPlaywrightService_ISetViewportSize;
    getStyle: IPlaywrightService_IGetStyle;
    getBoundingBox: IPlaywrightService_IGetBoundingBox;
    httpRequest: IPlaywrightService_IHttpRequest;
    waitForRequest: IPlaywrightService_IWaitForRequest;
    waitForResponse: IPlaywrightService_IWaitForResponse;
    waitForDownload: IPlaywrightService_IWaitForDownload;
    waitForNavigation: IPlaywrightService_IWaitForNavigation;
    waitForPageLoadState: IPlaywrightService_IWaitForPageLoadState;
    setGeolocation: IPlaywrightService_ISetGeolocation;
    getDevice: IPlaywrightService_IGetDevice;
    getDevices: IPlaywrightService_IGetDevices;
    addLocatorHandlerCustom: IPlaywrightService_IAddLocatorHandlerCustom;
    removeLocatorHandler: IPlaywrightService_IRemoveLocatorHandler;
    handleAlert: IPlaywrightService_IHandleAlert;
    waitForAlerts: IPlaywrightService_IWaitForAlerts;
    mouseButton: IPlaywrightService_IMouseButton;
    mouseMove: IPlaywrightService_IMouseMove;
    mouseWheel: IPlaywrightService_IMouseWheel;
    keyboardKey: IPlaywrightService_IKeyboardKey;
    keyboardInput: IPlaywrightService_IKeyboardInput;
    getTableRowIndex: IPlaywrightService_IGetTableRowIndex;
    getTableCellIndex: IPlaywrightService_IGetTableCellIndex;
    uploadFile: IPlaywrightService_IUploadFile;
    uploadFileBySelector: IPlaywrightService_IUploadFileBySelector;
    scrollToElement: IPlaywrightService_IScrollToElement;
    setOffline: IPlaywrightService_ISetOffline;
    reload: IPlaywrightService_IReload;
    switchPage: IPlaywrightService_ISwitchPage;
    switchContext: IPlaywrightService_ISwitchContext;
    switchBrowser: IPlaywrightService_ISwitchBrowser;
    newPage: IPlaywrightService_INewPage;
    newContext: IPlaywrightService_INewContext;
    newBrowser: IPlaywrightService_INewBrowser;
    launchBrowserServer: IPlaywrightService_ILaunchBrowserServer;
    closeBrowserServer: IPlaywrightService_ICloseBrowserServer;
    newPersistentContext: IPlaywrightService_INewPersistentContext;
    launchElectron: IPlaywrightService_ILaunchElectron;
    closeElectron: IPlaywrightService_ICloseElectron;
    connectToBrowser: IPlaywrightService_IConnectToBrowser;
    closeBrowser: IPlaywrightService_ICloseBrowser;
    closeAllBrowsers: IPlaywrightService_ICloseAllBrowsers;
    closeContext: IPlaywrightService_ICloseContext;
    closePage: IPlaywrightService_IClosePage;
    openTraceGroup: IPlaywrightService_IOpenTraceGroup;
    closeTraceGroup: IPlaywrightService_ICloseTraceGroup;
    getConsoleLog: IPlaywrightService_IGetConsoleLog;
    getErrorMessages: IPlaywrightService_IGetErrorMessages;
    getBrowserCatalog: IPlaywrightService_IGetBrowserCatalog;
    getDownloadState: IPlaywrightService_IGetDownloadState;
    cancelDownload: IPlaywrightService_ICancelDownload;
    saveStorageState: IPlaywrightService_ISaveStorageState;
    grantPermissions: IPlaywrightService_IGrantPermissions;
    executePlaywright: IPlaywrightService_IExecutePlaywright;
    clearPermissions: IPlaywrightService_IClearPermissions;
    initializeExtension: IPlaywrightService_IInitializeExtension;
    callExtensionKeyword: IPlaywrightService_ICallExtensionKeyword;
    setPeerId: IPlaywrightService_ISetPeerId;
    pdf: IPlaywrightService_IPdf;
    emulateMedia: IPlaywrightService_IEmulateMedia;
    setTime: IPlaywrightService_ISetTime;
    clockResume: IPlaywrightService_IClockResume;
    clockPauseAt: IPlaywrightService_IClockPauseAt;
    advanceClock: IPlaywrightService_IAdvanceClock;
    startCoverage: IPlaywrightService_IStartCoverage;
    stopCoverage: IPlaywrightService_IStopCoverage;
    mergeCoverage: IPlaywrightService_IMergeCoverage;
}

interface IPlaywrightService_IAriaSnapShot extends grpc.MethodDefinition<playwright_pb.Request.AriaSnapShot, playwright_pb.Response.String> {
    path: "/Playwright/AriaSnapShot";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.AriaSnapShot>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.AriaSnapShot>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IAddCookie extends grpc.MethodDefinition<playwright_pb.Request.Json, playwright_pb.Response.Empty> {
    path: "/Playwright/AddCookie";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Json>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Json>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGetCookies extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.Json> {
    path: "/Playwright/GetCookies";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IDeleteAllCookies extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.Empty> {
    path: "/Playwright/DeleteAllCookies";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_ITakeScreenshot extends grpc.MethodDefinition<playwright_pb.Request.ScreenshotOptions, playwright_pb.Response.String> {
    path: "/Playwright/TakeScreenshot";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ScreenshotOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ScreenshotOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IGoTo extends grpc.MethodDefinition<playwright_pb.Request.UrlOptions, playwright_pb.Response.String> {
    path: "/Playwright/GoTo";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.UrlOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.UrlOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IGoBack extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.Empty> {
    path: "/Playwright/GoBack";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGoForward extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.Empty> {
    path: "/Playwright/GoForward";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGetTitle extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.String> {
    path: "/Playwright/GetTitle";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IGetElementCount extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.Int> {
    path: "/Playwright/GetElementCount";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Int>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Int>;
}
interface IPlaywrightService_ITypeText extends grpc.MethodDefinition<playwright_pb.Request.TypeText, playwright_pb.Response.Empty> {
    path: "/Playwright/TypeText";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.TypeText>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.TypeText>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IFillText extends grpc.MethodDefinition<playwright_pb.Request.FillText, playwright_pb.Response.Empty> {
    path: "/Playwright/FillText";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.FillText>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.FillText>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IClearText extends grpc.MethodDefinition<playwright_pb.Request.ClearText, playwright_pb.Response.Empty> {
    path: "/Playwright/ClearText";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ClearText>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ClearText>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGetDomProperty extends grpc.MethodDefinition<playwright_pb.Request.ElementProperty, playwright_pb.Response.String> {
    path: "/Playwright/GetDomProperty";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementProperty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementProperty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IGetText extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.String> {
    path: "/Playwright/GetText";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IGetElementAttribute extends grpc.MethodDefinition<playwright_pb.Request.ElementProperty, playwright_pb.Response.String> {
    path: "/Playwright/GetElementAttribute";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementProperty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementProperty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IGetBoolProperty extends grpc.MethodDefinition<playwright_pb.Request.ElementProperty, playwright_pb.Response.Bool> {
    path: "/Playwright/GetBoolProperty";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementProperty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementProperty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Bool>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Bool>;
}
interface IPlaywrightService_IGetViewportSize extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.Json> {
    path: "/Playwright/GetViewportSize";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IGetUrl extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.String> {
    path: "/Playwright/GetUrl";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IGetPageSource extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.String> {
    path: "/Playwright/GetPageSource";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IPress extends grpc.MethodDefinition<playwright_pb.Request.PressKeys, playwright_pb.Response.Empty> {
    path: "/Playwright/Press";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.PressKeys>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.PressKeys>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGetSelectContent extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.Select> {
    path: "/Playwright/GetSelectContent";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Select>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Select>;
}
interface IPlaywrightService_ISelectOption extends grpc.MethodDefinition<playwright_pb.Request.SelectElementSelector, playwright_pb.Response.Select> {
    path: "/Playwright/SelectOption";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.SelectElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.SelectElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Select>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Select>;
}
interface IPlaywrightService_IDeselectOption extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.Empty> {
    path: "/Playwright/DeselectOption";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_ICheckCheckbox extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.Empty> {
    path: "/Playwright/CheckCheckbox";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IUncheckCheckbox extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.Empty> {
    path: "/Playwright/UncheckCheckbox";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IHealth extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.String> {
    path: "/Playwright/Health";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IGetElement extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.String> {
    path: "/Playwright/GetElement";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IGetElements extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.Json> {
    path: "/Playwright/GetElements";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IGetByX extends grpc.MethodDefinition<playwright_pb.Request.GetByOptions, playwright_pb.Response.Json> {
    path: "/Playwright/GetByX";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.GetByOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.GetByOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IGetElementStates extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.Json> {
    path: "/Playwright/GetElementStates";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_ISetTimeout extends grpc.MethodDefinition<playwright_pb.Request.Timeout, playwright_pb.Response.Empty> {
    path: "/Playwright/SetTimeout";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Timeout>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Timeout>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IAddStyleTag extends grpc.MethodDefinition<playwright_pb.Request.StyleTag, playwright_pb.Response.Empty> {
    path: "/Playwright/AddStyleTag";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.StyleTag>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.StyleTag>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IHighlightElements extends grpc.MethodDefinition<playwright_pb.Request.ElementSelectorWithDuration, playwright_pb.Response.Int> {
    path: "/Playwright/HighlightElements";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelectorWithDuration>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelectorWithDuration>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Int>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Int>;
}
interface IPlaywrightService_IDownload extends grpc.MethodDefinition<playwright_pb.Request.DownloadOptions, playwright_pb.Response.Json> {
    path: "/Playwright/Download";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.DownloadOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.DownloadOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IClick extends grpc.MethodDefinition<playwright_pb.Request.ElementSelectorWithOptions, playwright_pb.Response.Empty> {
    path: "/Playwright/Click";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelectorWithOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelectorWithOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_ITap extends grpc.MethodDefinition<playwright_pb.Request.ElementSelectorWithOptions, playwright_pb.Response.Empty> {
    path: "/Playwright/Tap";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelectorWithOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelectorWithOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IHover extends grpc.MethodDefinition<playwright_pb.Request.ElementSelectorWithOptions, playwright_pb.Response.Empty> {
    path: "/Playwright/Hover";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelectorWithOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelectorWithOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IFocus extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.Empty> {
    path: "/Playwright/Focus";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IWaitForElementsState extends grpc.MethodDefinition<playwright_pb.Request.ElementSelectorWithOptions, playwright_pb.Response.Empty> {
    path: "/Playwright/WaitForElementsState";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelectorWithOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelectorWithOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IWaitForFunction extends grpc.MethodDefinition<playwright_pb.Request.WaitForFunctionOptions, playwright_pb.Response.Json> {
    path: "/Playwright/WaitForFunction";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.WaitForFunctionOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.WaitForFunctionOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IEvaluateJavascript extends grpc.MethodDefinition<playwright_pb.Request.EvaluateAll, playwright_pb.Response.JavascriptExecutionResult> {
    path: "/Playwright/EvaluateJavascript";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.EvaluateAll>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.EvaluateAll>;
    responseSerialize: grpc.serialize<playwright_pb.Response.JavascriptExecutionResult>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.JavascriptExecutionResult>;
}
interface IPlaywrightService_IRecordSelector extends grpc.MethodDefinition<playwright_pb.Request.Label, playwright_pb.Response.JavascriptExecutionResult> {
    path: "/Playwright/RecordSelector";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Label>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Label>;
    responseSerialize: grpc.serialize<playwright_pb.Response.JavascriptExecutionResult>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.JavascriptExecutionResult>;
}
interface IPlaywrightService_ISetViewportSize extends grpc.MethodDefinition<playwright_pb.Request.Viewport, playwright_pb.Response.Empty> {
    path: "/Playwright/SetViewportSize";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Viewport>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Viewport>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGetStyle extends grpc.MethodDefinition<playwright_pb.Request.ElementStyle, playwright_pb.Response.Json> {
    path: "/Playwright/GetStyle";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementStyle>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementStyle>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IGetBoundingBox extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.Json> {
    path: "/Playwright/GetBoundingBox";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IHttpRequest extends grpc.MethodDefinition<playwright_pb.Request.HttpRequest, playwright_pb.Response.Json> {
    path: "/Playwright/HttpRequest";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.HttpRequest>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.HttpRequest>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IWaitForRequest extends grpc.MethodDefinition<playwright_pb.Request.HttpCapture, playwright_pb.Response.String> {
    path: "/Playwright/WaitForRequest";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.HttpCapture>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.HttpCapture>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IWaitForResponse extends grpc.MethodDefinition<playwright_pb.Request.HttpCapture, playwright_pb.Response.Json> {
    path: "/Playwright/WaitForResponse";
    requestStream: false;
    responseStream: true;
    requestSerialize: grpc.serialize<playwright_pb.Request.HttpCapture>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.HttpCapture>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IWaitForDownload extends grpc.MethodDefinition<playwright_pb.Request.DownloadOptions, playwright_pb.Response.Json> {
    path: "/Playwright/WaitForDownload";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.DownloadOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.DownloadOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IWaitForNavigation extends grpc.MethodDefinition<playwright_pb.Request.UrlOptions, playwright_pb.Response.Empty> {
    path: "/Playwright/WaitForNavigation";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.UrlOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.UrlOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IWaitForPageLoadState extends grpc.MethodDefinition<playwright_pb.Request.PageLoadState, playwright_pb.Response.Empty> {
    path: "/Playwright/WaitForPageLoadState";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.PageLoadState>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.PageLoadState>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_ISetGeolocation extends grpc.MethodDefinition<playwright_pb.Request.Json, playwright_pb.Response.Empty> {
    path: "/Playwright/SetGeolocation";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Json>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Json>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGetDevice extends grpc.MethodDefinition<playwright_pb.Request.Device, playwright_pb.Response.Json> {
    path: "/Playwright/GetDevice";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Device>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Device>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IGetDevices extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.Json> {
    path: "/Playwright/GetDevices";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IAddLocatorHandlerCustom extends grpc.MethodDefinition<playwright_pb.Request.LocatorHandlerAddCustom, playwright_pb.Response.Empty> {
    path: "/Playwright/AddLocatorHandlerCustom";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.LocatorHandlerAddCustom>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.LocatorHandlerAddCustom>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IRemoveLocatorHandler extends grpc.MethodDefinition<playwright_pb.Request.LocatorHandlerRemove, playwright_pb.Response.Empty> {
    path: "/Playwright/RemoveLocatorHandler";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.LocatorHandlerRemove>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.LocatorHandlerRemove>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IHandleAlert extends grpc.MethodDefinition<playwright_pb.Request.AlertAction, playwright_pb.Response.Empty> {
    path: "/Playwright/HandleAlert";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.AlertAction>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.AlertAction>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IWaitForAlerts extends grpc.MethodDefinition<playwright_pb.Request.AlertActions, playwright_pb.Response.ListString> {
    path: "/Playwright/WaitForAlerts";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.AlertActions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.AlertActions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.ListString>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.ListString>;
}
interface IPlaywrightService_IMouseButton extends grpc.MethodDefinition<playwright_pb.Request.MouseButtonOptions, playwright_pb.Response.Empty> {
    path: "/Playwright/MouseButton";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.MouseButtonOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.MouseButtonOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IMouseMove extends grpc.MethodDefinition<playwright_pb.Request.Json, playwright_pb.Response.Empty> {
    path: "/Playwright/MouseMove";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Json>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Json>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IMouseWheel extends grpc.MethodDefinition<playwright_pb.Request.MouseWheel, playwright_pb.Response.Empty> {
    path: "/Playwright/MouseWheel";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.MouseWheel>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.MouseWheel>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IKeyboardKey extends grpc.MethodDefinition<playwright_pb.Request.KeyboardKeypress, playwright_pb.Response.Empty> {
    path: "/Playwright/KeyboardKey";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.KeyboardKeypress>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.KeyboardKeypress>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IKeyboardInput extends grpc.MethodDefinition<playwright_pb.Request.KeyboardInputOptions, playwright_pb.Response.Empty> {
    path: "/Playwright/KeyboardInput";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.KeyboardInputOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.KeyboardInputOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGetTableRowIndex extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.Int> {
    path: "/Playwright/GetTableRowIndex";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Int>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Int>;
}
interface IPlaywrightService_IGetTableCellIndex extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.Int> {
    path: "/Playwright/GetTableCellIndex";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Int>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Int>;
}
interface IPlaywrightService_IUploadFile extends grpc.MethodDefinition<playwright_pb.Request.FilePath, playwright_pb.Response.Empty> {
    path: "/Playwright/UploadFile";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.FilePath>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.FilePath>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IUploadFileBySelector extends grpc.MethodDefinition<playwright_pb.Request.FileBySelector, playwright_pb.Response.Empty> {
    path: "/Playwright/UploadFileBySelector";
    requestStream: true;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.FileBySelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.FileBySelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IScrollToElement extends grpc.MethodDefinition<playwright_pb.Request.ElementSelector, playwright_pb.Response.Empty> {
    path: "/Playwright/ScrollToElement";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElementSelector>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElementSelector>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_ISetOffline extends grpc.MethodDefinition<playwright_pb.Request.Bool, playwright_pb.Response.Empty> {
    path: "/Playwright/SetOffline";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Bool>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Bool>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IReload extends grpc.MethodDefinition<playwright_pb.Request.Json, playwright_pb.Response.Empty> {
    path: "/Playwright/Reload";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Json>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Json>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_ISwitchPage extends grpc.MethodDefinition<playwright_pb.Request.IdWithTimeout, playwright_pb.Response.String> {
    path: "/Playwright/SwitchPage";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.IdWithTimeout>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.IdWithTimeout>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_ISwitchContext extends grpc.MethodDefinition<playwright_pb.Request.Index, playwright_pb.Response.String> {
    path: "/Playwright/SwitchContext";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Index>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Index>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_ISwitchBrowser extends grpc.MethodDefinition<playwright_pb.Request.Index, playwright_pb.Response.String> {
    path: "/Playwright/SwitchBrowser";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Index>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Index>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_INewPage extends grpc.MethodDefinition<playwright_pb.Request.UrlOptions, playwright_pb.Response.NewPageResponse> {
    path: "/Playwright/NewPage";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.UrlOptions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.UrlOptions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.NewPageResponse>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.NewPageResponse>;
}
interface IPlaywrightService_INewContext extends grpc.MethodDefinition<playwright_pb.Request.Context, playwright_pb.Response.NewContextResponse> {
    path: "/Playwright/NewContext";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Context>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Context>;
    responseSerialize: grpc.serialize<playwright_pb.Response.NewContextResponse>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.NewContextResponse>;
}
interface IPlaywrightService_INewBrowser extends grpc.MethodDefinition<playwright_pb.Request.Browser, playwright_pb.Response.String> {
    path: "/Playwright/NewBrowser";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Browser>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Browser>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_ILaunchBrowserServer extends grpc.MethodDefinition<playwright_pb.Request.Browser, playwright_pb.Response.String> {
    path: "/Playwright/LaunchBrowserServer";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Browser>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Browser>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_ICloseBrowserServer extends grpc.MethodDefinition<playwright_pb.Request.ConnectBrowser, playwright_pb.Response.Empty> {
    path: "/Playwright/CloseBrowserServer";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ConnectBrowser>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ConnectBrowser>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_INewPersistentContext extends grpc.MethodDefinition<playwright_pb.Request.PersistentContext, playwright_pb.Response.NewPersistentContextResponse> {
    path: "/Playwright/NewPersistentContext";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.PersistentContext>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.PersistentContext>;
    responseSerialize: grpc.serialize<playwright_pb.Response.NewPersistentContextResponse>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.NewPersistentContextResponse>;
}
interface IPlaywrightService_ILaunchElectron extends grpc.MethodDefinition<playwright_pb.Request.ElectronLaunch, playwright_pb.Response.NewPersistentContextResponse> {
    path: "/Playwright/LaunchElectron";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ElectronLaunch>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ElectronLaunch>;
    responseSerialize: grpc.serialize<playwright_pb.Response.NewPersistentContextResponse>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.NewPersistentContextResponse>;
}
interface IPlaywrightService_ICloseElectron extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.Empty> {
    path: "/Playwright/CloseElectron";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IConnectToBrowser extends grpc.MethodDefinition<playwright_pb.Request.ConnectBrowser, playwright_pb.Response.String> {
    path: "/Playwright/ConnectToBrowser";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ConnectBrowser>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ConnectBrowser>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_ICloseBrowser extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.String> {
    path: "/Playwright/CloseBrowser";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_ICloseAllBrowsers extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.Empty> {
    path: "/Playwright/CloseAllBrowsers";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_ICloseContext extends grpc.MethodDefinition<playwright_pb.Request.Bool, playwright_pb.Response.Empty> {
    path: "/Playwright/CloseContext";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Bool>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Bool>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IClosePage extends grpc.MethodDefinition<playwright_pb.Request.ClosePage, playwright_pb.Response.PageReportResponse> {
    path: "/Playwright/ClosePage";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ClosePage>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ClosePage>;
    responseSerialize: grpc.serialize<playwright_pb.Response.PageReportResponse>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.PageReportResponse>;
}
interface IPlaywrightService_IOpenTraceGroup extends grpc.MethodDefinition<playwright_pb.Request.TraceGroup, playwright_pb.Response.Empty> {
    path: "/Playwright/OpenTraceGroup";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.TraceGroup>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.TraceGroup>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_ICloseTraceGroup extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.Empty> {
    path: "/Playwright/CloseTraceGroup";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGetConsoleLog extends grpc.MethodDefinition<playwright_pb.Request.Bool, playwright_pb.Response.Json> {
    path: "/Playwright/GetConsoleLog";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Bool>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Bool>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IGetErrorMessages extends grpc.MethodDefinition<playwright_pb.Request.Bool, playwright_pb.Response.Json> {
    path: "/Playwright/GetErrorMessages";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Bool>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Bool>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IGetBrowserCatalog extends grpc.MethodDefinition<playwright_pb.Request.Bool, playwright_pb.Response.Json> {
    path: "/Playwright/GetBrowserCatalog";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Bool>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Bool>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_IGetDownloadState extends grpc.MethodDefinition<playwright_pb.Request.DownloadID, playwright_pb.Response.Json> {
    path: "/Playwright/GetDownloadState";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.DownloadID>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.DownloadID>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_ICancelDownload extends grpc.MethodDefinition<playwright_pb.Request.DownloadID, playwright_pb.Response.Empty> {
    path: "/Playwright/CancelDownload";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.DownloadID>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.DownloadID>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_ISaveStorageState extends grpc.MethodDefinition<playwright_pb.Request.FilePath, playwright_pb.Response.Empty> {
    path: "/Playwright/SaveStorageState";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.FilePath>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.FilePath>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IGrantPermissions extends grpc.MethodDefinition<playwright_pb.Request.Permissions, playwright_pb.Response.Empty> {
    path: "/Playwright/GrantPermissions";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Permissions>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Permissions>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IExecutePlaywright extends grpc.MethodDefinition<playwright_pb.Request.Json, playwright_pb.Response.Empty> {
    path: "/Playwright/ExecutePlaywright";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Json>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Json>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IClearPermissions extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.Empty> {
    path: "/Playwright/ClearPermissions";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IInitializeExtension extends grpc.MethodDefinition<playwright_pb.Request.FilePath, playwright_pb.Response.Keywords> {
    path: "/Playwright/InitializeExtension";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.FilePath>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.FilePath>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Keywords>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Keywords>;
}
interface IPlaywrightService_ICallExtensionKeyword extends grpc.MethodDefinition<playwright_pb.Request.KeywordCall, playwright_pb.Response.Json> {
    path: "/Playwright/CallExtensionKeyword";
    requestStream: false;
    responseStream: true;
    requestSerialize: grpc.serialize<playwright_pb.Request.KeywordCall>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.KeywordCall>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Json>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Json>;
}
interface IPlaywrightService_ISetPeerId extends grpc.MethodDefinition<playwright_pb.Request.Index, playwright_pb.Response.String> {
    path: "/Playwright/SetPeerId";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Index>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Index>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IPdf extends grpc.MethodDefinition<playwright_pb.Request.Pdf, playwright_pb.Response.String> {
    path: "/Playwright/Pdf";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Pdf>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Pdf>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IEmulateMedia extends grpc.MethodDefinition<playwright_pb.Request.EmulateMedia, playwright_pb.Response.String> {
    path: "/Playwright/EmulateMedia";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.EmulateMedia>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.EmulateMedia>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_ISetTime extends grpc.MethodDefinition<playwright_pb.Request.ClockSetTime, playwright_pb.Response.Empty> {
    path: "/Playwright/SetTime";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ClockSetTime>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ClockSetTime>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IClockResume extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.Empty> {
    path: "/Playwright/ClockResume";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IClockPauseAt extends grpc.MethodDefinition<playwright_pb.Request.ClockSetTime, playwright_pb.Response.Empty> {
    path: "/Playwright/ClockPauseAt";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ClockSetTime>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ClockSetTime>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IAdvanceClock extends grpc.MethodDefinition<playwright_pb.Request.ClockAdvance, playwright_pb.Response.Empty> {
    path: "/Playwright/AdvanceClock";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.ClockAdvance>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.ClockAdvance>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IStartCoverage extends grpc.MethodDefinition<playwright_pb.Request.CoverageStart, playwright_pb.Response.Empty> {
    path: "/Playwright/StartCoverage";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.CoverageStart>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.CoverageStart>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}
interface IPlaywrightService_IStopCoverage extends grpc.MethodDefinition<playwright_pb.Request.Empty, playwright_pb.Response.String> {
    path: "/Playwright/StopCoverage";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.Empty>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.Empty>;
    responseSerialize: grpc.serialize<playwright_pb.Response.String>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.String>;
}
interface IPlaywrightService_IMergeCoverage extends grpc.MethodDefinition<playwright_pb.Request.CoverageMerge, playwright_pb.Response.Empty> {
    path: "/Playwright/MergeCoverage";
    requestStream: false;
    responseStream: false;
    requestSerialize: grpc.serialize<playwright_pb.Request.CoverageMerge>;
    requestDeserialize: grpc.deserialize<playwright_pb.Request.CoverageMerge>;
    responseSerialize: grpc.serialize<playwright_pb.Response.Empty>;
    responseDeserialize: grpc.deserialize<playwright_pb.Response.Empty>;
}

export const PlaywrightService: IPlaywrightService;

export interface IPlaywrightServer {
    ariaSnapShot: grpc.handleUnaryCall<playwright_pb.Request.AriaSnapShot, playwright_pb.Response.String>;
    addCookie: grpc.handleUnaryCall<playwright_pb.Request.Json, playwright_pb.Response.Empty>;
    getCookies: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Json>;
    deleteAllCookies: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Empty>;
    takeScreenshot: grpc.handleUnaryCall<playwright_pb.Request.ScreenshotOptions, playwright_pb.Response.String>;
    goTo: grpc.handleUnaryCall<playwright_pb.Request.UrlOptions, playwright_pb.Response.String>;
    goBack: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Empty>;
    goForward: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Empty>;
    getTitle: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.String>;
    getElementCount: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.Int>;
    typeText: grpc.handleUnaryCall<playwright_pb.Request.TypeText, playwright_pb.Response.Empty>;
    fillText: grpc.handleUnaryCall<playwright_pb.Request.FillText, playwright_pb.Response.Empty>;
    clearText: grpc.handleUnaryCall<playwright_pb.Request.ClearText, playwright_pb.Response.Empty>;
    getDomProperty: grpc.handleUnaryCall<playwright_pb.Request.ElementProperty, playwright_pb.Response.String>;
    getText: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.String>;
    getElementAttribute: grpc.handleUnaryCall<playwright_pb.Request.ElementProperty, playwright_pb.Response.String>;
    getBoolProperty: grpc.handleUnaryCall<playwright_pb.Request.ElementProperty, playwright_pb.Response.Bool>;
    getViewportSize: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Json>;
    getUrl: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.String>;
    getPageSource: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.String>;
    press: grpc.handleUnaryCall<playwright_pb.Request.PressKeys, playwright_pb.Response.Empty>;
    getSelectContent: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.Select>;
    selectOption: grpc.handleUnaryCall<playwright_pb.Request.SelectElementSelector, playwright_pb.Response.Select>;
    deselectOption: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.Empty>;
    checkCheckbox: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.Empty>;
    uncheckCheckbox: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.Empty>;
    health: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.String>;
    getElement: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.String>;
    getElements: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.Json>;
    getByX: grpc.handleUnaryCall<playwright_pb.Request.GetByOptions, playwright_pb.Response.Json>;
    getElementStates: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.Json>;
    setTimeout: grpc.handleUnaryCall<playwright_pb.Request.Timeout, playwright_pb.Response.Empty>;
    addStyleTag: grpc.handleUnaryCall<playwright_pb.Request.StyleTag, playwright_pb.Response.Empty>;
    highlightElements: grpc.handleUnaryCall<playwright_pb.Request.ElementSelectorWithDuration, playwright_pb.Response.Int>;
    download: grpc.handleUnaryCall<playwright_pb.Request.DownloadOptions, playwright_pb.Response.Json>;
    click: grpc.handleUnaryCall<playwright_pb.Request.ElementSelectorWithOptions, playwright_pb.Response.Empty>;
    tap: grpc.handleUnaryCall<playwright_pb.Request.ElementSelectorWithOptions, playwright_pb.Response.Empty>;
    hover: grpc.handleUnaryCall<playwright_pb.Request.ElementSelectorWithOptions, playwright_pb.Response.Empty>;
    focus: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.Empty>;
    waitForElementsState: grpc.handleUnaryCall<playwright_pb.Request.ElementSelectorWithOptions, playwright_pb.Response.Empty>;
    waitForFunction: grpc.handleUnaryCall<playwright_pb.Request.WaitForFunctionOptions, playwright_pb.Response.Json>;
    evaluateJavascript: grpc.handleUnaryCall<playwright_pb.Request.EvaluateAll, playwright_pb.Response.JavascriptExecutionResult>;
    recordSelector: grpc.handleUnaryCall<playwright_pb.Request.Label, playwright_pb.Response.JavascriptExecutionResult>;
    setViewportSize: grpc.handleUnaryCall<playwright_pb.Request.Viewport, playwright_pb.Response.Empty>;
    getStyle: grpc.handleUnaryCall<playwright_pb.Request.ElementStyle, playwright_pb.Response.Json>;
    getBoundingBox: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.Json>;
    httpRequest: grpc.handleUnaryCall<playwright_pb.Request.HttpRequest, playwright_pb.Response.Json>;
    waitForRequest: grpc.handleUnaryCall<playwright_pb.Request.HttpCapture, playwright_pb.Response.String>;
    waitForResponse: grpc.handleServerStreamingCall<playwright_pb.Request.HttpCapture, playwright_pb.Response.Json>;
    waitForDownload: grpc.handleUnaryCall<playwright_pb.Request.DownloadOptions, playwright_pb.Response.Json>;
    waitForNavigation: grpc.handleUnaryCall<playwright_pb.Request.UrlOptions, playwright_pb.Response.Empty>;
    waitForPageLoadState: grpc.handleUnaryCall<playwright_pb.Request.PageLoadState, playwright_pb.Response.Empty>;
    setGeolocation: grpc.handleUnaryCall<playwright_pb.Request.Json, playwright_pb.Response.Empty>;
    getDevice: grpc.handleUnaryCall<playwright_pb.Request.Device, playwright_pb.Response.Json>;
    getDevices: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Json>;
    addLocatorHandlerCustom: grpc.handleUnaryCall<playwright_pb.Request.LocatorHandlerAddCustom, playwright_pb.Response.Empty>;
    removeLocatorHandler: grpc.handleUnaryCall<playwright_pb.Request.LocatorHandlerRemove, playwright_pb.Response.Empty>;
    handleAlert: grpc.handleUnaryCall<playwright_pb.Request.AlertAction, playwright_pb.Response.Empty>;
    waitForAlerts: grpc.handleUnaryCall<playwright_pb.Request.AlertActions, playwright_pb.Response.ListString>;
    mouseButton: grpc.handleUnaryCall<playwright_pb.Request.MouseButtonOptions, playwright_pb.Response.Empty>;
    mouseMove: grpc.handleUnaryCall<playwright_pb.Request.Json, playwright_pb.Response.Empty>;
    mouseWheel: grpc.handleUnaryCall<playwright_pb.Request.MouseWheel, playwright_pb.Response.Empty>;
    keyboardKey: grpc.handleUnaryCall<playwright_pb.Request.KeyboardKeypress, playwright_pb.Response.Empty>;
    keyboardInput: grpc.handleUnaryCall<playwright_pb.Request.KeyboardInputOptions, playwright_pb.Response.Empty>;
    getTableRowIndex: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.Int>;
    getTableCellIndex: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.Int>;
    uploadFile: grpc.handleUnaryCall<playwright_pb.Request.FilePath, playwright_pb.Response.Empty>;
    uploadFileBySelector: grpc.handleClientStreamingCall<playwright_pb.Request.FileBySelector, playwright_pb.Response.Empty>;
    scrollToElement: grpc.handleUnaryCall<playwright_pb.Request.ElementSelector, playwright_pb.Response.Empty>;
    setOffline: grpc.handleUnaryCall<playwright_pb.Request.Bool, playwright_pb.Response.Empty>;
    reload: grpc.handleUnaryCall<playwright_pb.Request.Json, playwright_pb.Response.Empty>;
    switchPage: grpc.handleUnaryCall<playwright_pb.Request.IdWithTimeout, playwright_pb.Response.String>;
    switchContext: grpc.handleUnaryCall<playwright_pb.Request.Index, playwright_pb.Response.String>;
    switchBrowser: grpc.handleUnaryCall<playwright_pb.Request.Index, playwright_pb.Response.String>;
    newPage: grpc.handleUnaryCall<playwright_pb.Request.UrlOptions, playwright_pb.Response.NewPageResponse>;
    newContext: grpc.handleUnaryCall<playwright_pb.Request.Context, playwright_pb.Response.NewContextResponse>;
    newBrowser: grpc.handleUnaryCall<playwright_pb.Request.Browser, playwright_pb.Response.String>;
    launchBrowserServer: grpc.handleUnaryCall<playwright_pb.Request.Browser, playwright_pb.Response.String>;
    closeBrowserServer: grpc.handleUnaryCall<playwright_pb.Request.ConnectBrowser, playwright_pb.Response.Empty>;
    newPersistentContext: grpc.handleUnaryCall<playwright_pb.Request.PersistentContext, playwright_pb.Response.NewPersistentContextResponse>;
    launchElectron: grpc.handleUnaryCall<playwright_pb.Request.ElectronLaunch, playwright_pb.Response.NewPersistentContextResponse>;
    closeElectron: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Empty>;
    connectToBrowser: grpc.handleUnaryCall<playwright_pb.Request.ConnectBrowser, playwright_pb.Response.String>;
    closeBrowser: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.String>;
    closeAllBrowsers: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Empty>;
    closeContext: grpc.handleUnaryCall<playwright_pb.Request.Bool, playwright_pb.Response.Empty>;
    closePage: grpc.handleUnaryCall<playwright_pb.Request.ClosePage, playwright_pb.Response.PageReportResponse>;
    openTraceGroup: grpc.handleUnaryCall<playwright_pb.Request.TraceGroup, playwright_pb.Response.Empty>;
    closeTraceGroup: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Empty>;
    getConsoleLog: grpc.handleUnaryCall<playwright_pb.Request.Bool, playwright_pb.Response.Json>;
    getErrorMessages: grpc.handleUnaryCall<playwright_pb.Request.Bool, playwright_pb.Response.Json>;
    getBrowserCatalog: grpc.handleUnaryCall<playwright_pb.Request.Bool, playwright_pb.Response.Json>;
    getDownloadState: grpc.handleUnaryCall<playwright_pb.Request.DownloadID, playwright_pb.Response.Json>;
    cancelDownload: grpc.handleUnaryCall<playwright_pb.Request.DownloadID, playwright_pb.Response.Empty>;
    saveStorageState: grpc.handleUnaryCall<playwright_pb.Request.FilePath, playwright_pb.Response.Empty>;
    grantPermissions: grpc.handleUnaryCall<playwright_pb.Request.Permissions, playwright_pb.Response.Empty>;
    executePlaywright: grpc.handleUnaryCall<playwright_pb.Request.Json, playwright_pb.Response.Empty>;
    clearPermissions: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Empty>;
    initializeExtension: grpc.handleUnaryCall<playwright_pb.Request.FilePath, playwright_pb.Response.Keywords>;
    callExtensionKeyword: grpc.handleServerStreamingCall<playwright_pb.Request.KeywordCall, playwright_pb.Response.Json>;
    setPeerId: grpc.handleUnaryCall<playwright_pb.Request.Index, playwright_pb.Response.String>;
    pdf: grpc.handleUnaryCall<playwright_pb.Request.Pdf, playwright_pb.Response.String>;
    emulateMedia: grpc.handleUnaryCall<playwright_pb.Request.EmulateMedia, playwright_pb.Response.String>;
    setTime: grpc.handleUnaryCall<playwright_pb.Request.ClockSetTime, playwright_pb.Response.Empty>;
    clockResume: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.Empty>;
    clockPauseAt: grpc.handleUnaryCall<playwright_pb.Request.ClockSetTime, playwright_pb.Response.Empty>;
    advanceClock: grpc.handleUnaryCall<playwright_pb.Request.ClockAdvance, playwright_pb.Response.Empty>;
    startCoverage: grpc.handleUnaryCall<playwright_pb.Request.CoverageStart, playwright_pb.Response.Empty>;
    stopCoverage: grpc.handleUnaryCall<playwright_pb.Request.Empty, playwright_pb.Response.String>;
    mergeCoverage: grpc.handleUnaryCall<playwright_pb.Request.CoverageMerge, playwright_pb.Response.Empty>;
}

export interface IPlaywrightClient {
    ariaSnapShot(request: playwright_pb.Request.AriaSnapShot, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    ariaSnapShot(request: playwright_pb.Request.AriaSnapShot, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    ariaSnapShot(request: playwright_pb.Request.AriaSnapShot, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    addCookie(request: playwright_pb.Request.Json, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    addCookie(request: playwright_pb.Request.Json, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    addCookie(request: playwright_pb.Request.Json, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    getCookies(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getCookies(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getCookies(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    deleteAllCookies(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    deleteAllCookies(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    deleteAllCookies(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    takeScreenshot(request: playwright_pb.Request.ScreenshotOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    takeScreenshot(request: playwright_pb.Request.ScreenshotOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    takeScreenshot(request: playwright_pb.Request.ScreenshotOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    goTo(request: playwright_pb.Request.UrlOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    goTo(request: playwright_pb.Request.UrlOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    goTo(request: playwright_pb.Request.UrlOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    goBack(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    goBack(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    goBack(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    goForward(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    goForward(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    goForward(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    getTitle(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getTitle(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getTitle(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getElementCount(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    getElementCount(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    getElementCount(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    typeText(request: playwright_pb.Request.TypeText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    typeText(request: playwright_pb.Request.TypeText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    typeText(request: playwright_pb.Request.TypeText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    fillText(request: playwright_pb.Request.FillText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    fillText(request: playwright_pb.Request.FillText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    fillText(request: playwright_pb.Request.FillText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clearText(request: playwright_pb.Request.ClearText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clearText(request: playwright_pb.Request.ClearText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clearText(request: playwright_pb.Request.ClearText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    getDomProperty(request: playwright_pb.Request.ElementProperty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getDomProperty(request: playwright_pb.Request.ElementProperty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getDomProperty(request: playwright_pb.Request.ElementProperty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getText(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getText(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getText(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getElementAttribute(request: playwright_pb.Request.ElementProperty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getElementAttribute(request: playwright_pb.Request.ElementProperty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getElementAttribute(request: playwright_pb.Request.ElementProperty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getBoolProperty(request: playwright_pb.Request.ElementProperty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Bool) => void): grpc.ClientUnaryCall;
    getBoolProperty(request: playwright_pb.Request.ElementProperty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Bool) => void): grpc.ClientUnaryCall;
    getBoolProperty(request: playwright_pb.Request.ElementProperty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Bool) => void): grpc.ClientUnaryCall;
    getViewportSize(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getViewportSize(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getViewportSize(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getUrl(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getUrl(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getUrl(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getPageSource(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getPageSource(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getPageSource(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    press(request: playwright_pb.Request.PressKeys, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    press(request: playwright_pb.Request.PressKeys, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    press(request: playwright_pb.Request.PressKeys, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    getSelectContent(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Select) => void): grpc.ClientUnaryCall;
    getSelectContent(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Select) => void): grpc.ClientUnaryCall;
    getSelectContent(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Select) => void): grpc.ClientUnaryCall;
    selectOption(request: playwright_pb.Request.SelectElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Select) => void): grpc.ClientUnaryCall;
    selectOption(request: playwright_pb.Request.SelectElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Select) => void): grpc.ClientUnaryCall;
    selectOption(request: playwright_pb.Request.SelectElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Select) => void): grpc.ClientUnaryCall;
    deselectOption(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    deselectOption(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    deselectOption(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    checkCheckbox(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    checkCheckbox(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    checkCheckbox(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    uncheckCheckbox(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    uncheckCheckbox(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    uncheckCheckbox(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    health(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    health(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    health(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getElement(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getElement(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getElement(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    getElements(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getElements(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getElements(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getByX(request: playwright_pb.Request.GetByOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getByX(request: playwright_pb.Request.GetByOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getByX(request: playwright_pb.Request.GetByOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getElementStates(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getElementStates(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getElementStates(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    setTimeout(request: playwright_pb.Request.Timeout, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setTimeout(request: playwright_pb.Request.Timeout, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setTimeout(request: playwright_pb.Request.Timeout, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    addStyleTag(request: playwright_pb.Request.StyleTag, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    addStyleTag(request: playwright_pb.Request.StyleTag, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    addStyleTag(request: playwright_pb.Request.StyleTag, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    highlightElements(request: playwright_pb.Request.ElementSelectorWithDuration, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    highlightElements(request: playwright_pb.Request.ElementSelectorWithDuration, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    highlightElements(request: playwright_pb.Request.ElementSelectorWithDuration, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    download(request: playwright_pb.Request.DownloadOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    download(request: playwright_pb.Request.DownloadOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    download(request: playwright_pb.Request.DownloadOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    click(request: playwright_pb.Request.ElementSelectorWithOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    click(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    click(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    tap(request: playwright_pb.Request.ElementSelectorWithOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    tap(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    tap(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    hover(request: playwright_pb.Request.ElementSelectorWithOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    hover(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    hover(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    focus(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    focus(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    focus(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    waitForElementsState(request: playwright_pb.Request.ElementSelectorWithOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    waitForElementsState(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    waitForElementsState(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    waitForFunction(request: playwright_pb.Request.WaitForFunctionOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    waitForFunction(request: playwright_pb.Request.WaitForFunctionOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    waitForFunction(request: playwright_pb.Request.WaitForFunctionOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    evaluateJavascript(request: playwright_pb.Request.EvaluateAll, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.JavascriptExecutionResult) => void): grpc.ClientUnaryCall;
    evaluateJavascript(request: playwright_pb.Request.EvaluateAll, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.JavascriptExecutionResult) => void): grpc.ClientUnaryCall;
    evaluateJavascript(request: playwright_pb.Request.EvaluateAll, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.JavascriptExecutionResult) => void): grpc.ClientUnaryCall;
    recordSelector(request: playwright_pb.Request.Label, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.JavascriptExecutionResult) => void): grpc.ClientUnaryCall;
    recordSelector(request: playwright_pb.Request.Label, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.JavascriptExecutionResult) => void): grpc.ClientUnaryCall;
    recordSelector(request: playwright_pb.Request.Label, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.JavascriptExecutionResult) => void): grpc.ClientUnaryCall;
    setViewportSize(request: playwright_pb.Request.Viewport, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setViewportSize(request: playwright_pb.Request.Viewport, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setViewportSize(request: playwright_pb.Request.Viewport, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    getStyle(request: playwright_pb.Request.ElementStyle, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getStyle(request: playwright_pb.Request.ElementStyle, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getStyle(request: playwright_pb.Request.ElementStyle, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getBoundingBox(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getBoundingBox(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getBoundingBox(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    httpRequest(request: playwright_pb.Request.HttpRequest, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    httpRequest(request: playwright_pb.Request.HttpRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    httpRequest(request: playwright_pb.Request.HttpRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    waitForRequest(request: playwright_pb.Request.HttpCapture, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    waitForRequest(request: playwright_pb.Request.HttpCapture, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    waitForRequest(request: playwright_pb.Request.HttpCapture, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    waitForResponse(request: playwright_pb.Request.HttpCapture, options?: Partial<grpc.CallOptions>): grpc.ClientReadableStream<playwright_pb.Response.Json>;
    waitForResponse(request: playwright_pb.Request.HttpCapture, metadata?: grpc.Metadata, options?: Partial<grpc.CallOptions>): grpc.ClientReadableStream<playwright_pb.Response.Json>;
    waitForDownload(request: playwright_pb.Request.DownloadOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    waitForDownload(request: playwright_pb.Request.DownloadOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    waitForDownload(request: playwright_pb.Request.DownloadOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    waitForNavigation(request: playwright_pb.Request.UrlOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    waitForNavigation(request: playwright_pb.Request.UrlOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    waitForNavigation(request: playwright_pb.Request.UrlOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    waitForPageLoadState(request: playwright_pb.Request.PageLoadState, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    waitForPageLoadState(request: playwright_pb.Request.PageLoadState, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    waitForPageLoadState(request: playwright_pb.Request.PageLoadState, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setGeolocation(request: playwright_pb.Request.Json, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setGeolocation(request: playwright_pb.Request.Json, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setGeolocation(request: playwright_pb.Request.Json, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    getDevice(request: playwright_pb.Request.Device, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getDevice(request: playwright_pb.Request.Device, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getDevice(request: playwright_pb.Request.Device, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getDevices(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getDevices(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getDevices(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    addLocatorHandlerCustom(request: playwright_pb.Request.LocatorHandlerAddCustom, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    addLocatorHandlerCustom(request: playwright_pb.Request.LocatorHandlerAddCustom, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    addLocatorHandlerCustom(request: playwright_pb.Request.LocatorHandlerAddCustom, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    removeLocatorHandler(request: playwright_pb.Request.LocatorHandlerRemove, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    removeLocatorHandler(request: playwright_pb.Request.LocatorHandlerRemove, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    removeLocatorHandler(request: playwright_pb.Request.LocatorHandlerRemove, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    handleAlert(request: playwright_pb.Request.AlertAction, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    handleAlert(request: playwright_pb.Request.AlertAction, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    handleAlert(request: playwright_pb.Request.AlertAction, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    waitForAlerts(request: playwright_pb.Request.AlertActions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.ListString) => void): grpc.ClientUnaryCall;
    waitForAlerts(request: playwright_pb.Request.AlertActions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.ListString) => void): grpc.ClientUnaryCall;
    waitForAlerts(request: playwright_pb.Request.AlertActions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.ListString) => void): grpc.ClientUnaryCall;
    mouseButton(request: playwright_pb.Request.MouseButtonOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    mouseButton(request: playwright_pb.Request.MouseButtonOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    mouseButton(request: playwright_pb.Request.MouseButtonOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    mouseMove(request: playwright_pb.Request.Json, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    mouseMove(request: playwright_pb.Request.Json, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    mouseMove(request: playwright_pb.Request.Json, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    mouseWheel(request: playwright_pb.Request.MouseWheel, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    mouseWheel(request: playwright_pb.Request.MouseWheel, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    mouseWheel(request: playwright_pb.Request.MouseWheel, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    keyboardKey(request: playwright_pb.Request.KeyboardKeypress, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    keyboardKey(request: playwright_pb.Request.KeyboardKeypress, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    keyboardKey(request: playwright_pb.Request.KeyboardKeypress, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    keyboardInput(request: playwright_pb.Request.KeyboardInputOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    keyboardInput(request: playwright_pb.Request.KeyboardInputOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    keyboardInput(request: playwright_pb.Request.KeyboardInputOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    getTableRowIndex(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    getTableRowIndex(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    getTableRowIndex(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    getTableCellIndex(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    getTableCellIndex(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    getTableCellIndex(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    uploadFile(request: playwright_pb.Request.FilePath, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    uploadFile(request: playwright_pb.Request.FilePath, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    uploadFile(request: playwright_pb.Request.FilePath, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    uploadFileBySelector(callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientWritableStream<playwright_pb.Request.FileBySelector>;
    uploadFileBySelector(metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientWritableStream<playwright_pb.Request.FileBySelector>;
    uploadFileBySelector(options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientWritableStream<playwright_pb.Request.FileBySelector>;
    uploadFileBySelector(metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientWritableStream<playwright_pb.Request.FileBySelector>;
    scrollToElement(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    scrollToElement(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    scrollToElement(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setOffline(request: playwright_pb.Request.Bool, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setOffline(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setOffline(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    reload(request: playwright_pb.Request.Json, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    reload(request: playwright_pb.Request.Json, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    reload(request: playwright_pb.Request.Json, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    switchPage(request: playwright_pb.Request.IdWithTimeout, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    switchPage(request: playwright_pb.Request.IdWithTimeout, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    switchPage(request: playwright_pb.Request.IdWithTimeout, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    switchContext(request: playwright_pb.Request.Index, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    switchContext(request: playwright_pb.Request.Index, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    switchContext(request: playwright_pb.Request.Index, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    switchBrowser(request: playwright_pb.Request.Index, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    switchBrowser(request: playwright_pb.Request.Index, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    switchBrowser(request: playwright_pb.Request.Index, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    newPage(request: playwright_pb.Request.UrlOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPageResponse) => void): grpc.ClientUnaryCall;
    newPage(request: playwright_pb.Request.UrlOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPageResponse) => void): grpc.ClientUnaryCall;
    newPage(request: playwright_pb.Request.UrlOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPageResponse) => void): grpc.ClientUnaryCall;
    newContext(request: playwright_pb.Request.Context, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewContextResponse) => void): grpc.ClientUnaryCall;
    newContext(request: playwright_pb.Request.Context, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewContextResponse) => void): grpc.ClientUnaryCall;
    newContext(request: playwright_pb.Request.Context, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewContextResponse) => void): grpc.ClientUnaryCall;
    newBrowser(request: playwright_pb.Request.Browser, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    newBrowser(request: playwright_pb.Request.Browser, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    newBrowser(request: playwright_pb.Request.Browser, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    launchBrowserServer(request: playwright_pb.Request.Browser, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    launchBrowserServer(request: playwright_pb.Request.Browser, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    launchBrowserServer(request: playwright_pb.Request.Browser, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    closeBrowserServer(request: playwright_pb.Request.ConnectBrowser, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeBrowserServer(request: playwright_pb.Request.ConnectBrowser, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeBrowserServer(request: playwright_pb.Request.ConnectBrowser, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    newPersistentContext(request: playwright_pb.Request.PersistentContext, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPersistentContextResponse) => void): grpc.ClientUnaryCall;
    newPersistentContext(request: playwright_pb.Request.PersistentContext, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPersistentContextResponse) => void): grpc.ClientUnaryCall;
    newPersistentContext(request: playwright_pb.Request.PersistentContext, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPersistentContextResponse) => void): grpc.ClientUnaryCall;
    launchElectron(request: playwright_pb.Request.ElectronLaunch, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPersistentContextResponse) => void): grpc.ClientUnaryCall;
    launchElectron(request: playwright_pb.Request.ElectronLaunch, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPersistentContextResponse) => void): grpc.ClientUnaryCall;
    launchElectron(request: playwright_pb.Request.ElectronLaunch, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPersistentContextResponse) => void): grpc.ClientUnaryCall;
    closeElectron(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeElectron(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeElectron(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    connectToBrowser(request: playwright_pb.Request.ConnectBrowser, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    connectToBrowser(request: playwright_pb.Request.ConnectBrowser, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    connectToBrowser(request: playwright_pb.Request.ConnectBrowser, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    closeBrowser(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    closeBrowser(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    closeBrowser(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    closeAllBrowsers(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeAllBrowsers(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeAllBrowsers(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeContext(request: playwright_pb.Request.Bool, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeContext(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeContext(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closePage(request: playwright_pb.Request.ClosePage, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.PageReportResponse) => void): grpc.ClientUnaryCall;
    closePage(request: playwright_pb.Request.ClosePage, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.PageReportResponse) => void): grpc.ClientUnaryCall;
    closePage(request: playwright_pb.Request.ClosePage, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.PageReportResponse) => void): grpc.ClientUnaryCall;
    openTraceGroup(request: playwright_pb.Request.TraceGroup, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    openTraceGroup(request: playwright_pb.Request.TraceGroup, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    openTraceGroup(request: playwright_pb.Request.TraceGroup, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeTraceGroup(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeTraceGroup(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    closeTraceGroup(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    getConsoleLog(request: playwright_pb.Request.Bool, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getConsoleLog(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getConsoleLog(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getErrorMessages(request: playwright_pb.Request.Bool, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getErrorMessages(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getErrorMessages(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getBrowserCatalog(request: playwright_pb.Request.Bool, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getBrowserCatalog(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getBrowserCatalog(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getDownloadState(request: playwright_pb.Request.DownloadID, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getDownloadState(request: playwright_pb.Request.DownloadID, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    getDownloadState(request: playwright_pb.Request.DownloadID, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    cancelDownload(request: playwright_pb.Request.DownloadID, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    cancelDownload(request: playwright_pb.Request.DownloadID, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    cancelDownload(request: playwright_pb.Request.DownloadID, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    saveStorageState(request: playwright_pb.Request.FilePath, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    saveStorageState(request: playwright_pb.Request.FilePath, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    saveStorageState(request: playwright_pb.Request.FilePath, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    grantPermissions(request: playwright_pb.Request.Permissions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    grantPermissions(request: playwright_pb.Request.Permissions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    grantPermissions(request: playwright_pb.Request.Permissions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    executePlaywright(request: playwright_pb.Request.Json, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    executePlaywright(request: playwright_pb.Request.Json, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    executePlaywright(request: playwright_pb.Request.Json, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clearPermissions(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clearPermissions(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clearPermissions(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    initializeExtension(request: playwright_pb.Request.FilePath, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Keywords) => void): grpc.ClientUnaryCall;
    initializeExtension(request: playwright_pb.Request.FilePath, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Keywords) => void): grpc.ClientUnaryCall;
    initializeExtension(request: playwright_pb.Request.FilePath, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Keywords) => void): grpc.ClientUnaryCall;
    callExtensionKeyword(request: playwright_pb.Request.KeywordCall, options?: Partial<grpc.CallOptions>): grpc.ClientReadableStream<playwright_pb.Response.Json>;
    callExtensionKeyword(request: playwright_pb.Request.KeywordCall, metadata?: grpc.Metadata, options?: Partial<grpc.CallOptions>): grpc.ClientReadableStream<playwright_pb.Response.Json>;
    setPeerId(request: playwright_pb.Request.Index, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    setPeerId(request: playwright_pb.Request.Index, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    setPeerId(request: playwright_pb.Request.Index, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    pdf(request: playwright_pb.Request.Pdf, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    pdf(request: playwright_pb.Request.Pdf, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    pdf(request: playwright_pb.Request.Pdf, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    emulateMedia(request: playwright_pb.Request.EmulateMedia, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    emulateMedia(request: playwright_pb.Request.EmulateMedia, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    emulateMedia(request: playwright_pb.Request.EmulateMedia, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    setTime(request: playwright_pb.Request.ClockSetTime, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setTime(request: playwright_pb.Request.ClockSetTime, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    setTime(request: playwright_pb.Request.ClockSetTime, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clockResume(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clockResume(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clockResume(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clockPauseAt(request: playwright_pb.Request.ClockSetTime, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clockPauseAt(request: playwright_pb.Request.ClockSetTime, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    clockPauseAt(request: playwright_pb.Request.ClockSetTime, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    advanceClock(request: playwright_pb.Request.ClockAdvance, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    advanceClock(request: playwright_pb.Request.ClockAdvance, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    advanceClock(request: playwright_pb.Request.ClockAdvance, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    startCoverage(request: playwright_pb.Request.CoverageStart, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    startCoverage(request: playwright_pb.Request.CoverageStart, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    startCoverage(request: playwright_pb.Request.CoverageStart, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    stopCoverage(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    stopCoverage(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    stopCoverage(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    mergeCoverage(request: playwright_pb.Request.CoverageMerge, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    mergeCoverage(request: playwright_pb.Request.CoverageMerge, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    mergeCoverage(request: playwright_pb.Request.CoverageMerge, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
}

export class PlaywrightClient extends grpc.Client implements IPlaywrightClient {
    constructor(address: string, credentials: grpc.ChannelCredentials, options?: object);
    public ariaSnapShot(request: playwright_pb.Request.AriaSnapShot, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public ariaSnapShot(request: playwright_pb.Request.AriaSnapShot, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public ariaSnapShot(request: playwright_pb.Request.AriaSnapShot, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public addCookie(request: playwright_pb.Request.Json, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public addCookie(request: playwright_pb.Request.Json, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public addCookie(request: playwright_pb.Request.Json, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public getCookies(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getCookies(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getCookies(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public deleteAllCookies(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public deleteAllCookies(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public deleteAllCookies(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public takeScreenshot(request: playwright_pb.Request.ScreenshotOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public takeScreenshot(request: playwright_pb.Request.ScreenshotOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public takeScreenshot(request: playwright_pb.Request.ScreenshotOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public goTo(request: playwright_pb.Request.UrlOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public goTo(request: playwright_pb.Request.UrlOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public goTo(request: playwright_pb.Request.UrlOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public goBack(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public goBack(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public goBack(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public goForward(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public goForward(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public goForward(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public getTitle(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getTitle(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getTitle(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getElementCount(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    public getElementCount(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    public getElementCount(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    public typeText(request: playwright_pb.Request.TypeText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public typeText(request: playwright_pb.Request.TypeText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public typeText(request: playwright_pb.Request.TypeText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public fillText(request: playwright_pb.Request.FillText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public fillText(request: playwright_pb.Request.FillText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public fillText(request: playwright_pb.Request.FillText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clearText(request: playwright_pb.Request.ClearText, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clearText(request: playwright_pb.Request.ClearText, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clearText(request: playwright_pb.Request.ClearText, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public getDomProperty(request: playwright_pb.Request.ElementProperty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getDomProperty(request: playwright_pb.Request.ElementProperty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getDomProperty(request: playwright_pb.Request.ElementProperty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getText(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getText(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getText(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getElementAttribute(request: playwright_pb.Request.ElementProperty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getElementAttribute(request: playwright_pb.Request.ElementProperty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getElementAttribute(request: playwright_pb.Request.ElementProperty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getBoolProperty(request: playwright_pb.Request.ElementProperty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Bool) => void): grpc.ClientUnaryCall;
    public getBoolProperty(request: playwright_pb.Request.ElementProperty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Bool) => void): grpc.ClientUnaryCall;
    public getBoolProperty(request: playwright_pb.Request.ElementProperty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Bool) => void): grpc.ClientUnaryCall;
    public getViewportSize(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getViewportSize(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getViewportSize(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getUrl(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getUrl(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getUrl(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getPageSource(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getPageSource(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getPageSource(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public press(request: playwright_pb.Request.PressKeys, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public press(request: playwright_pb.Request.PressKeys, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public press(request: playwright_pb.Request.PressKeys, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public getSelectContent(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Select) => void): grpc.ClientUnaryCall;
    public getSelectContent(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Select) => void): grpc.ClientUnaryCall;
    public getSelectContent(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Select) => void): grpc.ClientUnaryCall;
    public selectOption(request: playwright_pb.Request.SelectElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Select) => void): grpc.ClientUnaryCall;
    public selectOption(request: playwright_pb.Request.SelectElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Select) => void): grpc.ClientUnaryCall;
    public selectOption(request: playwright_pb.Request.SelectElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Select) => void): grpc.ClientUnaryCall;
    public deselectOption(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public deselectOption(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public deselectOption(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public checkCheckbox(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public checkCheckbox(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public checkCheckbox(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public uncheckCheckbox(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public uncheckCheckbox(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public uncheckCheckbox(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public health(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public health(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public health(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getElement(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getElement(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getElement(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public getElements(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getElements(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getElements(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getByX(request: playwright_pb.Request.GetByOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getByX(request: playwright_pb.Request.GetByOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getByX(request: playwright_pb.Request.GetByOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getElementStates(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getElementStates(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getElementStates(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public setTimeout(request: playwright_pb.Request.Timeout, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setTimeout(request: playwright_pb.Request.Timeout, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setTimeout(request: playwright_pb.Request.Timeout, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public addStyleTag(request: playwright_pb.Request.StyleTag, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public addStyleTag(request: playwright_pb.Request.StyleTag, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public addStyleTag(request: playwright_pb.Request.StyleTag, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public highlightElements(request: playwright_pb.Request.ElementSelectorWithDuration, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    public highlightElements(request: playwright_pb.Request.ElementSelectorWithDuration, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    public highlightElements(request: playwright_pb.Request.ElementSelectorWithDuration, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    public download(request: playwright_pb.Request.DownloadOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public download(request: playwright_pb.Request.DownloadOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public download(request: playwright_pb.Request.DownloadOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public click(request: playwright_pb.Request.ElementSelectorWithOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public click(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public click(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public tap(request: playwright_pb.Request.ElementSelectorWithOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public tap(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public tap(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public hover(request: playwright_pb.Request.ElementSelectorWithOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public hover(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public hover(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public focus(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public focus(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public focus(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public waitForElementsState(request: playwright_pb.Request.ElementSelectorWithOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public waitForElementsState(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public waitForElementsState(request: playwright_pb.Request.ElementSelectorWithOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public waitForFunction(request: playwright_pb.Request.WaitForFunctionOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public waitForFunction(request: playwright_pb.Request.WaitForFunctionOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public waitForFunction(request: playwright_pb.Request.WaitForFunctionOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public evaluateJavascript(request: playwright_pb.Request.EvaluateAll, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.JavascriptExecutionResult) => void): grpc.ClientUnaryCall;
    public evaluateJavascript(request: playwright_pb.Request.EvaluateAll, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.JavascriptExecutionResult) => void): grpc.ClientUnaryCall;
    public evaluateJavascript(request: playwright_pb.Request.EvaluateAll, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.JavascriptExecutionResult) => void): grpc.ClientUnaryCall;
    public recordSelector(request: playwright_pb.Request.Label, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.JavascriptExecutionResult) => void): grpc.ClientUnaryCall;
    public recordSelector(request: playwright_pb.Request.Label, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.JavascriptExecutionResult) => void): grpc.ClientUnaryCall;
    public recordSelector(request: playwright_pb.Request.Label, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.JavascriptExecutionResult) => void): grpc.ClientUnaryCall;
    public setViewportSize(request: playwright_pb.Request.Viewport, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setViewportSize(request: playwright_pb.Request.Viewport, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setViewportSize(request: playwright_pb.Request.Viewport, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public getStyle(request: playwright_pb.Request.ElementStyle, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getStyle(request: playwright_pb.Request.ElementStyle, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getStyle(request: playwright_pb.Request.ElementStyle, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getBoundingBox(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getBoundingBox(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getBoundingBox(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public httpRequest(request: playwright_pb.Request.HttpRequest, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public httpRequest(request: playwright_pb.Request.HttpRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public httpRequest(request: playwright_pb.Request.HttpRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public waitForRequest(request: playwright_pb.Request.HttpCapture, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public waitForRequest(request: playwright_pb.Request.HttpCapture, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public waitForRequest(request: playwright_pb.Request.HttpCapture, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public waitForResponse(request: playwright_pb.Request.HttpCapture, options?: Partial<grpc.CallOptions>): grpc.ClientReadableStream<playwright_pb.Response.Json>;
    public waitForResponse(request: playwright_pb.Request.HttpCapture, metadata?: grpc.Metadata, options?: Partial<grpc.CallOptions>): grpc.ClientReadableStream<playwright_pb.Response.Json>;
    public waitForDownload(request: playwright_pb.Request.DownloadOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public waitForDownload(request: playwright_pb.Request.DownloadOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public waitForDownload(request: playwright_pb.Request.DownloadOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public waitForNavigation(request: playwright_pb.Request.UrlOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public waitForNavigation(request: playwright_pb.Request.UrlOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public waitForNavigation(request: playwright_pb.Request.UrlOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public waitForPageLoadState(request: playwright_pb.Request.PageLoadState, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public waitForPageLoadState(request: playwright_pb.Request.PageLoadState, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public waitForPageLoadState(request: playwright_pb.Request.PageLoadState, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setGeolocation(request: playwright_pb.Request.Json, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setGeolocation(request: playwright_pb.Request.Json, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setGeolocation(request: playwright_pb.Request.Json, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public getDevice(request: playwright_pb.Request.Device, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getDevice(request: playwright_pb.Request.Device, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getDevice(request: playwright_pb.Request.Device, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getDevices(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getDevices(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getDevices(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public addLocatorHandlerCustom(request: playwright_pb.Request.LocatorHandlerAddCustom, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public addLocatorHandlerCustom(request: playwright_pb.Request.LocatorHandlerAddCustom, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public addLocatorHandlerCustom(request: playwright_pb.Request.LocatorHandlerAddCustom, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public removeLocatorHandler(request: playwright_pb.Request.LocatorHandlerRemove, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public removeLocatorHandler(request: playwright_pb.Request.LocatorHandlerRemove, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public removeLocatorHandler(request: playwright_pb.Request.LocatorHandlerRemove, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public handleAlert(request: playwright_pb.Request.AlertAction, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public handleAlert(request: playwright_pb.Request.AlertAction, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public handleAlert(request: playwright_pb.Request.AlertAction, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public waitForAlerts(request: playwright_pb.Request.AlertActions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.ListString) => void): grpc.ClientUnaryCall;
    public waitForAlerts(request: playwright_pb.Request.AlertActions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.ListString) => void): grpc.ClientUnaryCall;
    public waitForAlerts(request: playwright_pb.Request.AlertActions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.ListString) => void): grpc.ClientUnaryCall;
    public mouseButton(request: playwright_pb.Request.MouseButtonOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public mouseButton(request: playwright_pb.Request.MouseButtonOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public mouseButton(request: playwright_pb.Request.MouseButtonOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public mouseMove(request: playwright_pb.Request.Json, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public mouseMove(request: playwright_pb.Request.Json, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public mouseMove(request: playwright_pb.Request.Json, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public mouseWheel(request: playwright_pb.Request.MouseWheel, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public mouseWheel(request: playwright_pb.Request.MouseWheel, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public mouseWheel(request: playwright_pb.Request.MouseWheel, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public keyboardKey(request: playwright_pb.Request.KeyboardKeypress, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public keyboardKey(request: playwright_pb.Request.KeyboardKeypress, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public keyboardKey(request: playwright_pb.Request.KeyboardKeypress, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public keyboardInput(request: playwright_pb.Request.KeyboardInputOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public keyboardInput(request: playwright_pb.Request.KeyboardInputOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public keyboardInput(request: playwright_pb.Request.KeyboardInputOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public getTableRowIndex(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    public getTableRowIndex(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    public getTableRowIndex(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    public getTableCellIndex(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    public getTableCellIndex(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    public getTableCellIndex(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Int) => void): grpc.ClientUnaryCall;
    public uploadFile(request: playwright_pb.Request.FilePath, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public uploadFile(request: playwright_pb.Request.FilePath, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public uploadFile(request: playwright_pb.Request.FilePath, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public uploadFileBySelector(callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientWritableStream<playwright_pb.Request.FileBySelector>;
    public uploadFileBySelector(metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientWritableStream<playwright_pb.Request.FileBySelector>;
    public uploadFileBySelector(options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientWritableStream<playwright_pb.Request.FileBySelector>;
    public uploadFileBySelector(metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientWritableStream<playwright_pb.Request.FileBySelector>;
    public scrollToElement(request: playwright_pb.Request.ElementSelector, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public scrollToElement(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public scrollToElement(request: playwright_pb.Request.ElementSelector, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setOffline(request: playwright_pb.Request.Bool, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setOffline(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setOffline(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public reload(request: playwright_pb.Request.Json, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public reload(request: playwright_pb.Request.Json, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public reload(request: playwright_pb.Request.Json, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public switchPage(request: playwright_pb.Request.IdWithTimeout, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public switchPage(request: playwright_pb.Request.IdWithTimeout, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public switchPage(request: playwright_pb.Request.IdWithTimeout, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public switchContext(request: playwright_pb.Request.Index, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public switchContext(request: playwright_pb.Request.Index, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public switchContext(request: playwright_pb.Request.Index, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public switchBrowser(request: playwright_pb.Request.Index, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public switchBrowser(request: playwright_pb.Request.Index, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public switchBrowser(request: playwright_pb.Request.Index, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public newPage(request: playwright_pb.Request.UrlOptions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPageResponse) => void): grpc.ClientUnaryCall;
    public newPage(request: playwright_pb.Request.UrlOptions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPageResponse) => void): grpc.ClientUnaryCall;
    public newPage(request: playwright_pb.Request.UrlOptions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPageResponse) => void): grpc.ClientUnaryCall;
    public newContext(request: playwright_pb.Request.Context, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewContextResponse) => void): grpc.ClientUnaryCall;
    public newContext(request: playwright_pb.Request.Context, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewContextResponse) => void): grpc.ClientUnaryCall;
    public newContext(request: playwright_pb.Request.Context, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewContextResponse) => void): grpc.ClientUnaryCall;
    public newBrowser(request: playwright_pb.Request.Browser, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public newBrowser(request: playwright_pb.Request.Browser, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public newBrowser(request: playwright_pb.Request.Browser, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public launchBrowserServer(request: playwright_pb.Request.Browser, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public launchBrowserServer(request: playwright_pb.Request.Browser, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public launchBrowserServer(request: playwright_pb.Request.Browser, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public closeBrowserServer(request: playwright_pb.Request.ConnectBrowser, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeBrowserServer(request: playwright_pb.Request.ConnectBrowser, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeBrowserServer(request: playwright_pb.Request.ConnectBrowser, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public newPersistentContext(request: playwright_pb.Request.PersistentContext, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPersistentContextResponse) => void): grpc.ClientUnaryCall;
    public newPersistentContext(request: playwright_pb.Request.PersistentContext, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPersistentContextResponse) => void): grpc.ClientUnaryCall;
    public newPersistentContext(request: playwright_pb.Request.PersistentContext, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPersistentContextResponse) => void): grpc.ClientUnaryCall;
    public launchElectron(request: playwright_pb.Request.ElectronLaunch, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPersistentContextResponse) => void): grpc.ClientUnaryCall;
    public launchElectron(request: playwright_pb.Request.ElectronLaunch, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPersistentContextResponse) => void): grpc.ClientUnaryCall;
    public launchElectron(request: playwright_pb.Request.ElectronLaunch, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.NewPersistentContextResponse) => void): grpc.ClientUnaryCall;
    public closeElectron(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeElectron(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeElectron(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public connectToBrowser(request: playwright_pb.Request.ConnectBrowser, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public connectToBrowser(request: playwright_pb.Request.ConnectBrowser, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public connectToBrowser(request: playwright_pb.Request.ConnectBrowser, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public closeBrowser(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public closeBrowser(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public closeBrowser(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public closeAllBrowsers(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeAllBrowsers(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeAllBrowsers(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeContext(request: playwright_pb.Request.Bool, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeContext(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeContext(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closePage(request: playwright_pb.Request.ClosePage, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.PageReportResponse) => void): grpc.ClientUnaryCall;
    public closePage(request: playwright_pb.Request.ClosePage, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.PageReportResponse) => void): grpc.ClientUnaryCall;
    public closePage(request: playwright_pb.Request.ClosePage, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.PageReportResponse) => void): grpc.ClientUnaryCall;
    public openTraceGroup(request: playwright_pb.Request.TraceGroup, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public openTraceGroup(request: playwright_pb.Request.TraceGroup, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public openTraceGroup(request: playwright_pb.Request.TraceGroup, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeTraceGroup(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeTraceGroup(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public closeTraceGroup(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public getConsoleLog(request: playwright_pb.Request.Bool, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getConsoleLog(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getConsoleLog(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getErrorMessages(request: playwright_pb.Request.Bool, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getErrorMessages(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getErrorMessages(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getBrowserCatalog(request: playwright_pb.Request.Bool, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getBrowserCatalog(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getBrowserCatalog(request: playwright_pb.Request.Bool, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getDownloadState(request: playwright_pb.Request.DownloadID, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getDownloadState(request: playwright_pb.Request.DownloadID, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public getDownloadState(request: playwright_pb.Request.DownloadID, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Json) => void): grpc.ClientUnaryCall;
    public cancelDownload(request: playwright_pb.Request.DownloadID, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public cancelDownload(request: playwright_pb.Request.DownloadID, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public cancelDownload(request: playwright_pb.Request.DownloadID, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public saveStorageState(request: playwright_pb.Request.FilePath, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public saveStorageState(request: playwright_pb.Request.FilePath, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public saveStorageState(request: playwright_pb.Request.FilePath, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public grantPermissions(request: playwright_pb.Request.Permissions, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public grantPermissions(request: playwright_pb.Request.Permissions, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public grantPermissions(request: playwright_pb.Request.Permissions, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public executePlaywright(request: playwright_pb.Request.Json, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public executePlaywright(request: playwright_pb.Request.Json, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public executePlaywright(request: playwright_pb.Request.Json, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clearPermissions(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clearPermissions(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clearPermissions(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public initializeExtension(request: playwright_pb.Request.FilePath, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Keywords) => void): grpc.ClientUnaryCall;
    public initializeExtension(request: playwright_pb.Request.FilePath, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Keywords) => void): grpc.ClientUnaryCall;
    public initializeExtension(request: playwright_pb.Request.FilePath, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Keywords) => void): grpc.ClientUnaryCall;
    public callExtensionKeyword(request: playwright_pb.Request.KeywordCall, options?: Partial<grpc.CallOptions>): grpc.ClientReadableStream<playwright_pb.Response.Json>;
    public callExtensionKeyword(request: playwright_pb.Request.KeywordCall, metadata?: grpc.Metadata, options?: Partial<grpc.CallOptions>): grpc.ClientReadableStream<playwright_pb.Response.Json>;
    public setPeerId(request: playwright_pb.Request.Index, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public setPeerId(request: playwright_pb.Request.Index, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public setPeerId(request: playwright_pb.Request.Index, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public pdf(request: playwright_pb.Request.Pdf, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public pdf(request: playwright_pb.Request.Pdf, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public pdf(request: playwright_pb.Request.Pdf, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public emulateMedia(request: playwright_pb.Request.EmulateMedia, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public emulateMedia(request: playwright_pb.Request.EmulateMedia, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public emulateMedia(request: playwright_pb.Request.EmulateMedia, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public setTime(request: playwright_pb.Request.ClockSetTime, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setTime(request: playwright_pb.Request.ClockSetTime, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public setTime(request: playwright_pb.Request.ClockSetTime, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clockResume(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clockResume(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clockResume(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clockPauseAt(request: playwright_pb.Request.ClockSetTime, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clockPauseAt(request: playwright_pb.Request.ClockSetTime, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public clockPauseAt(request: playwright_pb.Request.ClockSetTime, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public advanceClock(request: playwright_pb.Request.ClockAdvance, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public advanceClock(request: playwright_pb.Request.ClockAdvance, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public advanceClock(request: playwright_pb.Request.ClockAdvance, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public startCoverage(request: playwright_pb.Request.CoverageStart, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public startCoverage(request: playwright_pb.Request.CoverageStart, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public startCoverage(request: playwright_pb.Request.CoverageStart, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public stopCoverage(request: playwright_pb.Request.Empty, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public stopCoverage(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public stopCoverage(request: playwright_pb.Request.Empty, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.String) => void): grpc.ClientUnaryCall;
    public mergeCoverage(request: playwright_pb.Request.CoverageMerge, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public mergeCoverage(request: playwright_pb.Request.CoverageMerge, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
    public mergeCoverage(request: playwright_pb.Request.CoverageMerge, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: playwright_pb.Response.Empty) => void): grpc.ClientUnaryCall;
}
