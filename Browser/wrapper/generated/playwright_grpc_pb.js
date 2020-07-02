// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var playwright_pb = require('./playwright_pb.js');

function serialize_Empty(arg) {
  if (!(arg instanceof playwright_pb.Empty)) {
    throw new Error('Expected argument of type Empty');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Empty(buffer_arg) {
  return playwright_pb.Empty.deserializeBinary(new Uint8Array(buffer_arg));
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

function serialize_clearTextRequest(arg) {
  if (!(arg instanceof playwright_pb.clearTextRequest)) {
    throw new Error('Expected argument of type clearTextRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_clearTextRequest(buffer_arg) {
  return playwright_pb.clearTextRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_fillTextRequest(arg) {
  if (!(arg instanceof playwright_pb.fillTextRequest)) {
    throw new Error('Expected argument of type fillTextRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_fillTextRequest(buffer_arg) {
  return playwright_pb.fillTextRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_getDomPropertyRequest(arg) {
  if (!(arg instanceof playwright_pb.getDomPropertyRequest)) {
    throw new Error('Expected argument of type getDomPropertyRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_getDomPropertyRequest(buffer_arg) {
  return playwright_pb.getDomPropertyRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_goToRequest(arg) {
  if (!(arg instanceof playwright_pb.goToRequest)) {
    throw new Error('Expected argument of type goToRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_goToRequest(buffer_arg) {
  return playwright_pb.goToRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_inputTextRequest(arg) {
  if (!(arg instanceof playwright_pb.inputTextRequest)) {
    throw new Error('Expected argument of type inputTextRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_inputTextRequest(buffer_arg) {
  return playwright_pb.inputTextRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_openBrowserRequest(arg) {
  if (!(arg instanceof playwright_pb.openBrowserRequest)) {
    throw new Error('Expected argument of type openBrowserRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_openBrowserRequest(buffer_arg) {
  return playwright_pb.openBrowserRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_pressRequest(arg) {
  if (!(arg instanceof playwright_pb.pressRequest)) {
    throw new Error('Expected argument of type pressRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_pressRequest(buffer_arg) {
  return playwright_pb.pressRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_screenshotRequest(arg) {
  if (!(arg instanceof playwright_pb.screenshotRequest)) {
    throw new Error('Expected argument of type screenshotRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_screenshotRequest(buffer_arg) {
  return playwright_pb.screenshotRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_selectorRequest(arg) {
  if (!(arg instanceof playwright_pb.selectorRequest)) {
    throw new Error('Expected argument of type selectorRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_selectorRequest(buffer_arg) {
  return playwright_pb.selectorRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_typeTextRequest(arg) {
  if (!(arg instanceof playwright_pb.typeTextRequest)) {
    throw new Error('Expected argument of type typeTextRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_typeTextRequest(buffer_arg) {
  return playwright_pb.typeTextRequest.deserializeBinary(new Uint8Array(buffer_arg));
}


var PlaywrightService = exports.PlaywrightService = {
  screenshot: {
    path: '/Playwright/Screenshot',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.screenshotRequest,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_screenshotRequest,
    requestDeserialize: deserialize_screenshotRequest,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  openBrowser: {
    path: '/Playwright/OpenBrowser',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.openBrowserRequest,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_openBrowserRequest,
    requestDeserialize: deserialize_openBrowserRequest,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  closeBrowser: {
    path: '/Playwright/CloseBrowser',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Empty,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Empty,
    requestDeserialize: deserialize_Empty,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Opens the url in currently open Playwright page 
goTo: {
    path: '/Playwright/GoTo',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.goToRequest,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_goToRequest,
    requestDeserialize: deserialize_goToRequest,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Gets title of currently open Playwright page 
getTitle: {
    path: '/Playwright/GetTitle',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Empty,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Empty,
    requestDeserialize: deserialize_Empty,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  // Wraps playwrights page.fill to input text into input specified with selector 
inputText: {
    path: '/Playwright/InputText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.inputTextRequest,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_inputTextRequest,
    requestDeserialize: deserialize_inputTextRequest,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Wraps playwrights page.type to type text into input specified with selector 
typeText: {
    path: '/Playwright/TypeText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.typeTextRequest,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_typeTextRequest,
    requestDeserialize: deserialize_typeTextRequest,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Wraps playwrights page.fill to fill text of input specified with selector 
fillText: {
    path: '/Playwright/FillText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.fillTextRequest,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_fillTextRequest,
    requestDeserialize: deserialize_fillTextRequest,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Wraps playwrights page.fill with empty text to clear input specified with selector 
clearText: {
    path: '/Playwright/ClearText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.clearTextRequest,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_clearTextRequest,
    requestDeserialize: deserialize_clearTextRequest,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Gets the DOM property 'property' of selector specified element 
getDomProperty: {
    path: '/Playwright/GetDomProperty',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.getDomPropertyRequest,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_getDomPropertyRequest,
    requestDeserialize: deserialize_getDomPropertyRequest,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  // Gets the boolean DOM property 'property' of selector specified element 
getBoolProperty: {
    path: '/Playwright/GetBoolProperty',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.getDomPropertyRequest,
    responseType: playwright_pb.Response.Bool,
    requestSerialize: serialize_getDomPropertyRequest,
    requestDeserialize: deserialize_getDomPropertyRequest,
    responseSerialize: serialize_Response_Bool,
    responseDeserialize: deserialize_Response_Bool,
  },
  // Wraps playwrights page.textContent, returns textcontent of element by selector 
getTextContent: {
    path: '/Playwright/GetTextContent',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.selectorRequest,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_selectorRequest,
    requestDeserialize: deserialize_selectorRequest,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  // *Returns current playwright page url
getUrl: {
    path: '/Playwright/GetUrl',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Empty,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Empty,
    requestDeserialize: deserialize_Empty,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
  // Clicks element specified by selector 
click: {
    path: '/Playwright/Click',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.selectorRequest,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_selectorRequest,
    requestDeserialize: deserialize_selectorRequest,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Inputs a list of keypresses to element specified by selector 
press: {
    path: '/Playwright/Press',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.pressRequest,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_pressRequest,
    requestDeserialize: deserialize_pressRequest,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Checks checkbox specified by selector 
checkCheckbox: {
    path: '/Playwright/CheckCheckbox',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.selectorRequest,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_selectorRequest,
    requestDeserialize: deserialize_selectorRequest,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Unchecks checkbox specified by selector 
uncheckCheckbox: {
    path: '/Playwright/UncheckCheckbox',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.selectorRequest,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_selectorRequest,
    requestDeserialize: deserialize_selectorRequest,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Health check endpoint for the service 
health: {
    path: '/Playwright/Health',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Empty,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_Empty,
    requestDeserialize: deserialize_Empty,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
};

exports.PlaywrightClient = grpc.makeGenericClientConstructor(PlaywrightService);
