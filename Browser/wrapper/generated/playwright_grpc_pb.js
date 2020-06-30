// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var playwright_pb = require('./playwright_pb.js');

function serialize_Request_Empty(arg) {
  if (!(arg instanceof playwright_pb.Request.Empty)) {
    throw new Error('Expected argument of type Request.Empty');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_Empty(buffer_arg) {
  return playwright_pb.Request.Empty.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_getDomProperty(arg) {
  if (!(arg instanceof playwright_pb.Request.getDomProperty)) {
    throw new Error('Expected argument of type Request.getDomProperty');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_getDomProperty(buffer_arg) {
  return playwright_pb.Request.getDomProperty.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_goTo(arg) {
  if (!(arg instanceof playwright_pb.Request.goTo)) {
    throw new Error('Expected argument of type Request.goTo');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_goTo(buffer_arg) {
  return playwright_pb.Request.goTo.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_inputText(arg) {
  if (!(arg instanceof playwright_pb.Request.inputText)) {
    throw new Error('Expected argument of type Request.inputText');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_inputText(buffer_arg) {
  return playwright_pb.Request.inputText.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_openBrowser(arg) {
  if (!(arg instanceof playwright_pb.Request.openBrowser)) {
    throw new Error('Expected argument of type Request.openBrowser');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_openBrowser(buffer_arg) {
  return playwright_pb.Request.openBrowser.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_screenshot(arg) {
  if (!(arg instanceof playwright_pb.Request.screenshot)) {
    throw new Error('Expected argument of type Request.screenshot');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_screenshot(buffer_arg) {
  return playwright_pb.Request.screenshot.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_selector(arg) {
  if (!(arg instanceof playwright_pb.Request.selector)) {
    throw new Error('Expected argument of type Request.selector');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_selector(buffer_arg) {
  return playwright_pb.Request.selector.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_Bool(arg) {
  if (!(arg instanceof playwright_pb.Response.Bool)) {
    throw new Error('Expected argument of type Response.Bool');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_Bool(buffer_arg) {
  return playwright_pb.Response.Bool.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_Empty(arg) {
  if (!(arg instanceof playwright_pb.Response.Empty)) {
    throw new Error('Expected argument of type Response.Empty');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_Empty(buffer_arg) {
  return playwright_pb.Response.Empty.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Response_String(arg) {
  if (!(arg instanceof playwright_pb.Response.String)) {
    throw new Error('Expected argument of type Response.String');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response_String(buffer_arg) {
  return playwright_pb.Response.String.deserializeBinary(new Uint8Array(buffer_arg));
}


var PlaywrightService = exports.PlaywrightService = {
  screenshot: {
    path: '/Playwright/Screenshot',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.screenshot,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_screenshot,
    requestDeserialize: deserialize_Request_screenshot,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  openBrowser: {
    path: '/Playwright/OpenBrowser',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.openBrowser,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_openBrowser,
    requestDeserialize: deserialize_Request_openBrowser,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  closeBrowser: {
    path: '/Playwright/CloseBrowser',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.Empty,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_Empty,
    requestDeserialize: deserialize_Request_Empty,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Opens the url in currently open Playwright page 
goTo: {
    path: '/Playwright/GoTo',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.goTo,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_goTo,
    requestDeserialize: deserialize_Request_goTo,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Gets title of currently open Playwright page 
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
  // Wraps playwrights page.fill to input text into input specified with selector 
inputText: {
    path: '/Playwright/InputText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.inputText,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_inputText,
    requestDeserialize: deserialize_Request_inputText,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Gets the DOM property 'property' of selector specified element 
getDomProperty: {
    path: '/Playwright/GetDomProperty',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.getDomProperty,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_getDomProperty,
    requestDeserialize: deserialize_Request_getDomProperty,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  // Gets the boolean DOM property 'property' of selector specified element 
getBoolProperty: {
    path: '/Playwright/GetBoolProperty',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.getDomProperty,
    responseType: playwright_pb.Response.Bool,
    requestSerialize: serialize_Request_getDomProperty,
    requestDeserialize: deserialize_Request_getDomProperty,
    responseSerialize: serialize_Response_Bool,
    responseDeserialize: deserialize_Response_Bool,
  },
  // Wraps playwrights page.textContent, returns textcontent of element by selector 
getTextContent: {
    path: '/Playwright/GetTextContent',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.selector,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Request_selector,
    requestDeserialize: deserialize_Request_selector,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  // *Returns current playwright page url
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
  // Clicks button specified by selector 
clickButton: {
    path: '/Playwright/ClickButton',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.selector,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_selector,
    requestDeserialize: deserialize_Request_selector,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Checks checkbox specified by selector 
checkCheckbox: {
    path: '/Playwright/CheckCheckbox',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.selector,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_selector,
    requestDeserialize: deserialize_Request_selector,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Unchecks checkbox specified by selector 
uncheckCheckbox: {
    path: '/Playwright/UncheckCheckbox',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.selector,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_selector,
    requestDeserialize: deserialize_Request_selector,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Health check endpoint for the service 
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
};

exports.PlaywrightClient = grpc.makeGenericClientConstructor(PlaywrightService);
