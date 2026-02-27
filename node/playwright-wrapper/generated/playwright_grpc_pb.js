// GENERATED CODE -- DO NOT EDIT!
'use strict';

var grpc = require('@grpc/grpc-js');
var playwright_pb = require('./playwright_pb.js');

function serialize_message(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Empty(buffer_arg) {
  return playwright_pb.Request.Empty.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_AlertAction(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_AlertAction(buffer_arg) {
  return playwright_pb.Request.AlertAction.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_AlertActions(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_AlertActions(buffer_arg) {
  return playwright_pb.Request.AlertActions.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_AriaSnapShot(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_AriaSnapShot(buffer_arg) {
  return playwright_pb.Request.AriaSnapShot.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_Bool(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Bool(buffer_arg) {
  return playwright_pb.Request.Bool.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_Browser(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Browser(buffer_arg) {
  return playwright_pb.Request.Browser.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_ClearText(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_ClearText(buffer_arg) {
  return playwright_pb.Request.ClearText.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_ClockAdvance(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_ClockAdvance(buffer_arg) {
  return playwright_pb.Request.ClockAdvance.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_ClockSetTime(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_ClockSetTime(buffer_arg) {
  return playwright_pb.Request.ClockSetTime.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_ClosePage(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_ClosePage(buffer_arg) {
  return playwright_pb.Request.ClosePage.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_ConnectBrowser(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_ConnectBrowser(buffer_arg) {
  return playwright_pb.Request.ConnectBrowser.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_Context(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Context(buffer_arg) {
  return playwright_pb.Request.Context.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_CoverageMerge(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_CoverageMerge(buffer_arg) {
  return playwright_pb.Request.CoverageMerge.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_CoverageStart(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_CoverageStart(buffer_arg) {
  return playwright_pb.Request.CoverageStart.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_Device(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Device(buffer_arg) {
  return playwright_pb.Request.Device.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_DownloadID(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_DownloadID(buffer_arg) {
  return playwright_pb.Request.DownloadID.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_DownloadOptions(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_DownloadOptions(buffer_arg) {
  return playwright_pb.Request.DownloadOptions.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_ElectronLaunch(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_ElectronLaunch(buffer_arg) {
  return playwright_pb.Request.ElectronLaunch.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_ElementProperty(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_ElementProperty(buffer_arg) {
  return playwright_pb.Request.ElementProperty.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_ElementSelector(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_ElementSelector(buffer_arg) {
  return playwright_pb.Request.ElementSelector.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_ElementSelectorWithDuration(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_ElementSelectorWithDuration(buffer_arg) {
  return playwright_pb.Request.ElementSelectorWithDuration.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_ElementSelectorWithOptions(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_ElementSelectorWithOptions(buffer_arg) {
  return playwright_pb.Request.ElementSelectorWithOptions.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_ElementStyle(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_ElementStyle(buffer_arg) {
  return playwright_pb.Request.ElementStyle.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_Empty(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Empty(buffer_arg) {
  return playwright_pb.Request.Empty.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_EmulateMedia(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_EmulateMedia(buffer_arg) {
  return playwright_pb.Request.EmulateMedia.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_EvaluateAll(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_EvaluateAll(buffer_arg) {
  return playwright_pb.Request.EvaluateAll.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_FileBySelector(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_FileBySelector(buffer_arg) {
  return playwright_pb.Request.FileBySelector.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_FilePath(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_FilePath(buffer_arg) {
  return playwright_pb.Request.FilePath.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_FillText(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_FillText(buffer_arg) {
  return playwright_pb.Request.FillText.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_GetByOptions(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_GetByOptions(buffer_arg) {
  return playwright_pb.Request.GetByOptions.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_HttpCapture(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_HttpCapture(buffer_arg) {
  return playwright_pb.Request.HttpCapture.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_HttpRequest(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_HttpRequest(buffer_arg) {
  return playwright_pb.Request.HttpRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_IdWithTimeout(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_IdWithTimeout(buffer_arg) {
  return playwright_pb.Request.IdWithTimeout.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_Index(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Index(buffer_arg) {
  return playwright_pb.Request.Index.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_Json(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Json(buffer_arg) {
  return playwright_pb.Request.Json.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_KeyboardInputOptions(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_KeyboardInputOptions(buffer_arg) {
  return playwright_pb.Request.KeyboardInputOptions.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_KeyboardKeypress(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_KeyboardKeypress(buffer_arg) {
  return playwright_pb.Request.KeyboardKeypress.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_KeywordCall(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_KeywordCall(buffer_arg) {
  return playwright_pb.Request.KeywordCall.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_Label(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Label(buffer_arg) {
  return playwright_pb.Request.Label.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_LocatorHandlerAddCustom(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_LocatorHandlerAddCustom(buffer_arg) {
  return playwright_pb.Request.LocatorHandlerAddCustom.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_LocatorHandlerRemove(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_LocatorHandlerRemove(buffer_arg) {
  return playwright_pb.Request.LocatorHandlerRemove.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_MouseButtonOptions(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_MouseButtonOptions(buffer_arg) {
  return playwright_pb.Request.MouseButtonOptions.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_MouseWheel(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_MouseWheel(buffer_arg) {
  return playwright_pb.Request.MouseWheel.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_PageLoadState(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_PageLoadState(buffer_arg) {
  return playwright_pb.Request.PageLoadState.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_Pdf(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Pdf(buffer_arg) {
  return playwright_pb.Request.Pdf.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_Permissions(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Permissions(buffer_arg) {
  return playwright_pb.Request.Permissions.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_PersistentContext(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_PersistentContext(buffer_arg) {
  return playwright_pb.Request.PersistentContext.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_PressKeys(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_PressKeys(buffer_arg) {
  return playwright_pb.Request.PressKeys.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_ScreenshotOptions(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_ScreenshotOptions(buffer_arg) {
  return playwright_pb.Request.ScreenshotOptions.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_SelectElementSelector(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_SelectElementSelector(buffer_arg) {
  return playwright_pb.Request.SelectElementSelector.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_StyleTag(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_StyleTag(buffer_arg) {
  return playwright_pb.Request.StyleTag.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_Timeout(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Timeout(buffer_arg) {
  return playwright_pb.Request.Timeout.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_TraceGroup(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_TraceGroup(buffer_arg) {
  return playwright_pb.Request.TraceGroup.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_TypeText(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_TypeText(buffer_arg) {
  return playwright_pb.Request.TypeText.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_UrlOptions(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_UrlOptions(buffer_arg) {
  return playwright_pb.Request.UrlOptions.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_Viewport(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Viewport(buffer_arg) {
  return playwright_pb.Request.Viewport.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_WaitForFunctionOptions(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_WaitForFunctionOptions(buffer_arg) {
  return playwright_pb.Request.WaitForFunctionOptions.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_Bool(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_Bool(buffer_arg) {
  return playwright_pb.Response.Bool.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_Empty(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_Empty(buffer_arg) {
  return playwright_pb.Response.Empty.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_Int(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_Int(buffer_arg) {
  return playwright_pb.Response.Int.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_JavascriptExecutionResult(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_JavascriptExecutionResult(buffer_arg) {
  return playwright_pb.Response.JavascriptExecutionResult.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_Json(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_Json(buffer_arg) {
  return playwright_pb.Response.Json.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_Keywords(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_Keywords(buffer_arg) {
  return playwright_pb.Response.Keywords.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_ListString(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_ListString(buffer_arg) {
  return playwright_pb.Response.ListString.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_NewContextResponse(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_NewContextResponse(buffer_arg) {
  return playwright_pb.Response.NewContextResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_NewPageResponse(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_NewPageResponse(buffer_arg) {
  return playwright_pb.Response.NewPageResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_NewPersistentContextResponse(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_NewPersistentContextResponse(buffer_arg) {
  return playwright_pb.Response.NewPersistentContextResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_PageReportResponse(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_PageReportResponse(buffer_arg) {
  return playwright_pb.Response.PageReportResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_Select(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_Select(buffer_arg) {
  return playwright_pb.Response.Select.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_String(arg) {
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_String(buffer_arg) {
  return playwright_pb.Response.String.deserializeBinary(new Uint8Array(buffer_arg));
}

var PlaywrightService = exports.PlaywrightService = {
  ariaSnapShot: {
    path: '/Playwright/AriaSnapShot',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.AriaSnapShot,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_AriaSnapShot,
    requestDeserialize: deserialize_Request_AriaSnapShot,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  addCookie: {
    path: '/Playwright/AddCookie',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Json,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Json,
    requestDeserialize: deserialize_Request_Json,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  getCookies: {
    path: '/Playwright/GetCookies',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  deleteAllCookies: {
    path: '/Playwright/DeleteAllCookies',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  takeScreenshot: {
    path: '/Playwright/TakeScreenshot',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ScreenshotOptions,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_ScreenshotOptions,
    requestDeserialize: deserialize_Request_ScreenshotOptions,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  goTo: {
    path: '/Playwright/GoTo',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.UrlOptions,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_UrlOptions,
    requestDeserialize: deserialize_Request_UrlOptions,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  goBack: {
    path: '/Playwright/GoBack',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  goForward: {
    path: '/Playwright/GoForward',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  getTitle: {
    path: '/Playwright/GetTitle',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  getElementCount: {
    path: '/Playwright/GetElementCount',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.Int,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_Int,
    responseDeserialize: deserialize_Response_Int,
  },
  typeText: {
    path: '/Playwright/TypeText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.TypeText,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_TypeText,
    requestDeserialize: deserialize_Request_TypeText,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  fillText: {
    path: '/Playwright/FillText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.FillText,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_FillText,
    requestDeserialize: deserialize_Request_FillText,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  clearText: {
    path: '/Playwright/ClearText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ClearText,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ClearText,
    requestDeserialize: deserialize_Request_ClearText,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  getDomProperty: {
    path: '/Playwright/GetDomProperty',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementProperty,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_ElementProperty,
    requestDeserialize: deserialize_Request_ElementProperty,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  getText: {
    path: '/Playwright/GetText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  getElementAttribute: {
    path: '/Playwright/GetElementAttribute',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementProperty,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_ElementProperty,
    requestDeserialize: deserialize_Request_ElementProperty,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  getBoolProperty: {
    path: '/Playwright/GetBoolProperty',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementProperty,
    responseType: playwright_pb.Response.Bool,
    requestSerialize: serialize_Request_ElementProperty,
    requestDeserialize: deserialize_Request_ElementProperty,
    responseSerialize: serialize_Response_Bool,
    responseDeserialize: deserialize_Response_Bool,
  },
  getViewportSize: {
    path: '/Playwright/GetViewportSize',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  getUrl: {
    path: '/Playwright/GetUrl',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  getPageSource: {
    path: '/Playwright/GetPageSource',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  press: {
    path: '/Playwright/Press',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.PressKeys,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_PressKeys,
    requestDeserialize: deserialize_Request_PressKeys,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  getSelectContent: {
    path: '/Playwright/GetSelectContent',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.Select,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_Select,
    responseDeserialize: deserialize_Response_Select,
  },
  selectOption: {
    path: '/Playwright/SelectOption',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.SelectElementSelector,
    responseType: playwright_pb.Response.Select,
    requestSerialize: serialize_Request_SelectElementSelector,
    requestDeserialize: deserialize_Request_SelectElementSelector,
    responseSerialize: serialize_Response_Select,
    responseDeserialize: deserialize_Response_Select,
  },
  deselectOption: {
    path: '/Playwright/DeselectOption',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  checkCheckbox: {
    path: '/Playwright/CheckCheckbox',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  uncheckCheckbox: {
    path: '/Playwright/UncheckCheckbox',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  health: {
    path: '/Playwright/Health',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  getElement: {
    path: '/Playwright/GetElement',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  getElements: {
    path: '/Playwright/GetElements',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  getByX: {
    path: '/Playwright/GetByX',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.GetByOptions,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_GetByOptions,
    requestDeserialize: deserialize_Request_GetByOptions,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  getElementStates: {
    path: '/Playwright/GetElementStates',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  setTimeout: {
    path: '/Playwright/SetTimeout',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Timeout,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Timeout,
    requestDeserialize: deserialize_Request_Timeout,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  addStyleTag: {
    path: '/Playwright/AddStyleTag',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.StyleTag,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_StyleTag,
    requestDeserialize: deserialize_Request_StyleTag,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  highlightElements: {
    path: '/Playwright/HighlightElements',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelectorWithDuration,
    responseType: playwright_pb.Response.Int,
    requestSerialize: serialize_Request_ElementSelectorWithDuration,
    requestDeserialize: deserialize_Request_ElementSelectorWithDuration,
    responseSerialize: serialize_Response_Int,
    responseDeserialize: deserialize_Response_Int,
  },
  download: {
    path: '/Playwright/Download',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.DownloadOptions,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_DownloadOptions,
    requestDeserialize: deserialize_Request_DownloadOptions,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  click: {
    path: '/Playwright/Click',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelectorWithOptions,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ElementSelectorWithOptions,
    requestDeserialize: deserialize_Request_ElementSelectorWithOptions,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  tap: {
    path: '/Playwright/Tap',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelectorWithOptions,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ElementSelectorWithOptions,
    requestDeserialize: deserialize_Request_ElementSelectorWithOptions,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  hover: {
    path: '/Playwright/Hover',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelectorWithOptions,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ElementSelectorWithOptions,
    requestDeserialize: deserialize_Request_ElementSelectorWithOptions,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  focus: {
    path: '/Playwright/Focus',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  waitForElementsState: {
    path: '/Playwright/WaitForElementsState',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelectorWithOptions,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ElementSelectorWithOptions,
    requestDeserialize: deserialize_Request_ElementSelectorWithOptions,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  waitForFunction: {
    path: '/Playwright/WaitForFunction',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.WaitForFunctionOptions,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_WaitForFunctionOptions,
    requestDeserialize: deserialize_Request_WaitForFunctionOptions,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  evaluateJavascript: {
    path: '/Playwright/EvaluateJavascript',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.EvaluateAll,
    responseType: playwright_pb.Response.JavascriptExecutionResult,
    requestSerialize: serialize_Request_EvaluateAll,
    requestDeserialize: deserialize_Request_EvaluateAll,
    responseSerialize: serialize_Response_JavascriptExecutionResult,
    responseDeserialize: deserialize_Response_JavascriptExecutionResult,
  },
  recordSelector: {
    path: '/Playwright/RecordSelector',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Label,
    responseType: playwright_pb.Response.JavascriptExecutionResult,
    requestSerialize: serialize_Request_Label,
    requestDeserialize: deserialize_Request_Label,
    responseSerialize: serialize_Response_JavascriptExecutionResult,
    responseDeserialize: deserialize_Response_JavascriptExecutionResult,
  },
  setViewportSize: {
    path: '/Playwright/SetViewportSize',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Viewport,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Viewport,
    requestDeserialize: deserialize_Request_Viewport,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  getStyle: {
    path: '/Playwright/GetStyle',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementStyle,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_ElementStyle,
    requestDeserialize: deserialize_Request_ElementStyle,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  getBoundingBox: {
    path: '/Playwright/GetBoundingBox',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  httpRequest: {
    path: '/Playwright/HttpRequest',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.HttpRequest,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_HttpRequest,
    requestDeserialize: deserialize_Request_HttpRequest,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  waitForRequest: {
    path: '/Playwright/WaitForRequest',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.HttpCapture,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_HttpCapture,
    requestDeserialize: deserialize_Request_HttpCapture,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  waitForDownload: {
    path: '/Playwright/WaitForDownload',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.DownloadOptions,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_DownloadOptions,
    requestDeserialize: deserialize_Request_DownloadOptions,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  waitForNavigation: {
    path: '/Playwright/WaitForNavigation',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.UrlOptions,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_UrlOptions,
    requestDeserialize: deserialize_Request_UrlOptions,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  waitForPageLoadState: {
    path: '/Playwright/WaitForPageLoadState',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.PageLoadState,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_PageLoadState,
    requestDeserialize: deserialize_Request_PageLoadState,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  setGeolocation: {
    path: '/Playwright/SetGeolocation',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Json,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Json,
    requestDeserialize: deserialize_Request_Json,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  getDevice: {
    path: '/Playwright/GetDevice',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Device,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_Device,
    requestDeserialize: deserialize_Request_Device,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  getDevices: {
    path: '/Playwright/GetDevices',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  addLocatorHandlerCustom: {
    path: '/Playwright/AddLocatorHandlerCustom',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.LocatorHandlerAddCustom,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_LocatorHandlerAddCustom,
    requestDeserialize: deserialize_Request_LocatorHandlerAddCustom,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  removeLocatorHandler: {
    path: '/Playwright/RemoveLocatorHandler',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.LocatorHandlerRemove,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_LocatorHandlerRemove,
    requestDeserialize: deserialize_Request_LocatorHandlerRemove,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  handleAlert: {
    path: '/Playwright/HandleAlert',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.AlertAction,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_AlertAction,
    requestDeserialize: deserialize_Request_AlertAction,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  waitForAlerts: {
    path: '/Playwright/WaitForAlerts',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.AlertActions,
    responseType: playwright_pb.Response.ListString,
    requestSerialize: serialize_Request_AlertActions,
    requestDeserialize: deserialize_Request_AlertActions,
    responseSerialize: serialize_Response_ListString,
    responseDeserialize: deserialize_Response_ListString,
  },
  mouseButton: {
    path: '/Playwright/MouseButton',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.MouseButtonOptions,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_MouseButtonOptions,
    requestDeserialize: deserialize_Request_MouseButtonOptions,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  mouseMove: {
    path: '/Playwright/MouseMove',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Json,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Json,
    requestDeserialize: deserialize_Request_Json,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  mouseWheel: {
    path: '/Playwright/MouseWheel',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.MouseWheel,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_MouseWheel,
    requestDeserialize: deserialize_Request_MouseWheel,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  keyboardKey: {
    path: '/Playwright/KeyboardKey',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.KeyboardKeypress,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_KeyboardKeypress,
    requestDeserialize: deserialize_Request_KeyboardKeypress,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  keyboardInput: {
    path: '/Playwright/KeyboardInput',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.KeyboardInputOptions,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_KeyboardInputOptions,
    requestDeserialize: deserialize_Request_KeyboardInputOptions,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  getTableRowIndex: {
    path: '/Playwright/GetTableRowIndex',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.Int,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_Int,
    responseDeserialize: deserialize_Response_Int,
  },
  getTableCellIndex: {
    path: '/Playwright/GetTableCellIndex',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.Int,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_Int,
    responseDeserialize: deserialize_Response_Int,
  },
  uploadFile: {
    path: '/Playwright/UploadFile',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.FilePath,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_FilePath,
    requestDeserialize: deserialize_Request_FilePath,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  scrollToElement: {
    path: '/Playwright/ScrollToElement',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElementSelector,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ElementSelector,
    requestDeserialize: deserialize_Request_ElementSelector,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  setOffline: {
    path: '/Playwright/SetOffline',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Bool,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Bool,
    requestDeserialize: deserialize_Request_Bool,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  reload: {
    path: '/Playwright/Reload',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Json,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Json,
    requestDeserialize: deserialize_Request_Json,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  switchPage: {
    path: '/Playwright/SwitchPage',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.IdWithTimeout,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_IdWithTimeout,
    requestDeserialize: deserialize_Request_IdWithTimeout,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  switchContext: {
    path: '/Playwright/SwitchContext',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Index,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_Index,
    requestDeserialize: deserialize_Request_Index,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  switchBrowser: {
    path: '/Playwright/SwitchBrowser',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Index,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_Index,
    requestDeserialize: deserialize_Request_Index,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  newPage: {
    path: '/Playwright/NewPage',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.UrlOptions,
    responseType: playwright_pb.Response.NewPageResponse,
    requestSerialize: serialize_Request_UrlOptions,
    requestDeserialize: deserialize_Request_UrlOptions,
    responseSerialize: serialize_Response_NewPageResponse,
    responseDeserialize: deserialize_Response_NewPageResponse,
  },
  newContext: {
    path: '/Playwright/NewContext',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Context,
    responseType: playwright_pb.Response.NewContextResponse,
    requestSerialize: serialize_Request_Context,
    requestDeserialize: deserialize_Request_Context,
    responseSerialize: serialize_Response_NewContextResponse,
    responseDeserialize: deserialize_Response_NewContextResponse,
  },
  newBrowser: {
    path: '/Playwright/NewBrowser',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Browser,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_Browser,
    requestDeserialize: deserialize_Request_Browser,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  launchBrowserServer: {
    path: '/Playwright/LaunchBrowserServer',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Browser,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_Browser,
    requestDeserialize: deserialize_Request_Browser,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  closeBrowserServer: {
    path: '/Playwright/CloseBrowserServer',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ConnectBrowser,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ConnectBrowser,
    requestDeserialize: deserialize_Request_ConnectBrowser,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  newPersistentContext: {
    path: '/Playwright/NewPersistentContext',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.PersistentContext,
    responseType: playwright_pb.Response.NewPersistentContextResponse,
    requestSerialize: serialize_Request_PersistentContext,
    requestDeserialize: deserialize_Request_PersistentContext,
    responseSerialize: serialize_Response_NewPersistentContextResponse,
    responseDeserialize: deserialize_Response_NewPersistentContextResponse,
  },
  launchElectron: {
    path: '/Playwright/LaunchElectron',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ElectronLaunch,
    responseType: playwright_pb.Response.NewPersistentContextResponse,
    requestSerialize: serialize_Request_ElectronLaunch,
    requestDeserialize: deserialize_Request_ElectronLaunch,
    responseSerialize: serialize_Response_NewPersistentContextResponse,
    responseDeserialize: deserialize_Response_NewPersistentContextResponse,
  },
  closeElectron: {
    path: '/Playwright/CloseElectron',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  openElectronDevTools: {
    path: '/Playwright/OpenElectronDevTools',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  connectToBrowser: {
    path: '/Playwright/ConnectToBrowser',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ConnectBrowser,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_ConnectBrowser,
    requestDeserialize: deserialize_Request_ConnectBrowser,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  closeBrowser: {
    path: '/Playwright/CloseBrowser',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  closeAllBrowsers: {
    path: '/Playwright/CloseAllBrowsers',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  closeContext: {
    path: '/Playwright/CloseContext',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Bool,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Bool,
    requestDeserialize: deserialize_Request_Bool,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  closePage: {
    path: '/Playwright/ClosePage',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ClosePage,
    responseType: playwright_pb.Response.PageReportResponse,
    requestSerialize: serialize_Request_ClosePage,
    requestDeserialize: deserialize_Request_ClosePage,
    responseSerialize: serialize_Response_PageReportResponse,
    responseDeserialize: deserialize_Response_PageReportResponse,
  },
  openTraceGroup: {
    path: '/Playwright/OpenTraceGroup',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.TraceGroup,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_TraceGroup,
    requestDeserialize: deserialize_Request_TraceGroup,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  closeTraceGroup: {
    path: '/Playwright/CloseTraceGroup',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  getConsoleLog: {
    path: '/Playwright/GetConsoleLog',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Bool,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_Bool,
    requestDeserialize: deserialize_Request_Bool,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  getErrorMessages: {
    path: '/Playwright/GetErrorMessages',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Bool,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_Bool,
    requestDeserialize: deserialize_Request_Bool,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  getBrowserCatalog: {
    path: '/Playwright/GetBrowserCatalog',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Bool,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_Bool,
    requestDeserialize: deserialize_Request_Bool,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  getDownloadState: {
    path: '/Playwright/GetDownloadState',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.DownloadID,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_DownloadID,
    requestDeserialize: deserialize_Request_DownloadID,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  cancelDownload: {
    path: '/Playwright/CancelDownload',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.DownloadID,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_DownloadID,
    requestDeserialize: deserialize_Request_DownloadID,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  saveStorageState: {
    path: '/Playwright/SaveStorageState',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.FilePath,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_FilePath,
    requestDeserialize: deserialize_Request_FilePath,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  grantPermissions: {
    path: '/Playwright/GrantPermissions',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Permissions,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Permissions,
    requestDeserialize: deserialize_Request_Permissions,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  executePlaywright: {
    path: '/Playwright/ExecutePlaywright',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Json,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Json,
    requestDeserialize: deserialize_Request_Json,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  clearPermissions: {
    path: '/Playwright/ClearPermissions',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  initializeExtension: {
    path: '/Playwright/InitializeExtension',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.FilePath,
    responseType: playwright_pb.Response.Keywords,
    requestSerialize: serialize_Request_FilePath,
    requestDeserialize: deserialize_Request_FilePath,
    responseSerialize: serialize_Response_Keywords,
    responseDeserialize: deserialize_Response_Keywords,
  },
  setPeerId: {
    path: '/Playwright/SetPeerId',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Index,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_Index,
    requestDeserialize: deserialize_Request_Index,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  pdf: {
    path: '/Playwright/Pdf',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Pdf,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_Pdf,
    requestDeserialize: deserialize_Request_Pdf,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  emulateMedia: {
    path: '/Playwright/EmulateMedia',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.EmulateMedia,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_EmulateMedia,
    requestDeserialize: deserialize_Request_EmulateMedia,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  setTime: {
    path: '/Playwright/SetTime',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ClockSetTime,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ClockSetTime,
    requestDeserialize: deserialize_Request_ClockSetTime,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  clockResume: {
    path: '/Playwright/ClockResume',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  clockPauseAt: {
    path: '/Playwright/ClockPauseAt',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ClockSetTime,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ClockSetTime,
    requestDeserialize: deserialize_Request_ClockSetTime,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  advanceClock: {
    path: '/Playwright/AdvanceClock',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.ClockAdvance,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_ClockAdvance,
    requestDeserialize: deserialize_Request_ClockAdvance,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  startCoverage: {
    path: '/Playwright/StartCoverage',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.CoverageStart,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_CoverageStart,
    requestDeserialize: deserialize_Request_CoverageStart,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  stopCoverage: {
    path: '/Playwright/StopCoverage',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  mergeCoverage: {
    path: '/Playwright/MergeCoverage',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.CoverageMerge,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_CoverageMerge,
    requestDeserialize: deserialize_Request_CoverageMerge,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  waitForResponse: {
    path: '/Playwright/WaitForResponse',
    requestStream: false,
    responseStream: true,
    requestType: playwright_pb.Request.HttpCapture,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_HttpCapture,
    requestDeserialize: deserialize_Request_HttpCapture,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  callExtensionKeyword: {
    path: '/Playwright/CallExtensionKeyword',
    requestStream: false,
    responseStream: true,
    requestType: playwright_pb.Request.KeywordCall,
    responseType: playwright_pb.Response.Json,
    requestSerialize: serialize_Request_KeywordCall,
    requestDeserialize: deserialize_Request_KeywordCall,
    responseSerialize: serialize_Response_Json,
    responseDeserialize: deserialize_Response_Json,
  },
  uploadFileBySelector: {
    path: '/Playwright/UploadFileBySelector',
    requestStream: true,
    responseStream: false,
    requestType: playwright_pb.Request.FileBySelector,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_FileBySelector,
    requestDeserialize: deserialize_Request_FileBySelector,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
};

exports.PlaywrightClient = grpc.makeGenericClientConstructor(PlaywrightService, 'Playwright', {});
