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

function serialize_selectorRequest(arg) {
  if (!(arg instanceof playwright_pb.selectorRequest)) {
    throw new Error('Expected argument of type selectorRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_selectorRequest(buffer_arg) {
  return playwright_pb.selectorRequest.deserializeBinary(new Uint8Array(buffer_arg));
}


var PlaywrightService = exports.PlaywrightService = {
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
  getText: {
    path: '/Playwright/GetText',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.selectorRequest,
    responseType: playwright_pb.Response.String,
    requestSerialize: serialize_selectorRequest,
    requestDeserialize: deserialize_selectorRequest,
    responseSerialize: serialize_Response_String,
    responseDeserialize: deserialize_Response_String,
  },
};

exports.PlaywrightClient = grpc.makeGenericClientConstructor(PlaywrightService);
