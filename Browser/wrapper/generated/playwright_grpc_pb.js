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

function serialize_Request_addStyleTag(arg) {
  if (!(arg instanceof playwright_pb.Request.addStyleTag)) {
    throw new Error('Expected argument of type Request.addStyleTag');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_addStyleTag(buffer_arg) {
  return playwright_pb.Request.addStyleTag.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_clearText(arg) {
  if (!(arg instanceof playwright_pb.Request.clearText)) {
    throw new Error('Expected argument of type Request.clearText');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_clearText(buffer_arg) {
  return playwright_pb.Request.clearText.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_fillText(arg) {
  if (!(arg instanceof playwright_pb.Request.fillText)) {
    throw new Error('Expected argument of type Request.fillText');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_fillText(buffer_arg) {
  return playwright_pb.Request.fillText.deserializeBinary(new Uint8Array(buffer_arg));
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

function serialize_Request_press(arg) {
  if (!(arg instanceof playwright_pb.Request.press)) {
    throw new Error('Expected argument of type Request.press');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_press(buffer_arg) {
  return playwright_pb.Request.press.deserializeBinary(new Uint8Array(buffer_arg));
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

function serialize_Request_timeout(arg) {
  if (!(arg instanceof playwright_pb.Request.timeout)) {
    throw new Error('Expected argument of type Request.timeout');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_timeout(buffer_arg) {
  return playwright_pb.Request.timeout.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Request_typeText(arg) {
  if (!(arg instanceof playwright_pb.Request.typeText)) {
    throw new Error('Expected argument of type Request.typeText');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Request_typeText(buffer_arg) {
  return playwright_pb.Request.typeText.deserializeBinary(new Uint8Array(buffer_arg));
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
  // Navigate to the next page in history 
goBack: {
    path: '/Playwright/GoBack',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.goTo,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_goTo,
    requestDeserialize: deserialize_Request_goTo,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Navigate to the previous page in history. 
goForward: {
    path: '/Playwright/GoForward',
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
  // Wraps playwrights page.type to type text into input specified with selector 
typeText: {
    path: '/Playwright/TypeText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.typeText,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_typeText,
    requestDeserialize: deserialize_Request_typeText,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Wraps playwrights page.fill to fill text of input specified with selector 
fillText: {
    path: '/Playwright/FillText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.fillText,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_fillText,
    requestDeserialize: deserialize_Request_fillText,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Wraps playwrights page.fill with empty text to clear input specified with selector 
clearText: {
    path: '/Playwright/ClearText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.clearText,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_clearText,
    requestDeserialize: deserialize_Request_clearText,
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
  // Clicks element specified by selector 
click: {
    path: '/Playwright/Click',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.selector,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_selector,
    requestDeserialize: deserialize_Request_selector,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Inputs a list of keypresses to element specified by selector 
press: {
    path: '/Playwright/Press',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.press,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_press,
    requestDeserialize: deserialize_Request_press,
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
  // Set's  playwright timeout 
setTimeout: {
    path: '/Playwright/SetTimeout',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.timeout,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_timeout,
    requestDeserialize: deserialize_Request_timeout,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
  // Adds a <style> to head of side. 
addStyleTag: {
    path: '/Playwright/AddStyleTag',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Request.addStyleTag,
    responseType: playwright_pb.Response.Empty,
    requestSerialize: serialize_Request_addStyleTag,
    requestDeserialize: deserialize_Request_addStyleTag,
    responseSerialize: serialize_Response_Empty,
    responseDeserialize: deserialize_Response_Empty,
  },
};

exports.PlaywrightClient = grpc.makeGenericClientConstructor(PlaywrightService);
