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

function serialize_Response(arg) {
  if (!(arg instanceof playwright_pb.Response)) {
    throw new Error('Expected argument of type Response');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_Response(buffer_arg) {
  return playwright_pb.Response.deserializeBinary(new Uint8Array(buffer_arg));
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


var PlaywrightService = exports.PlaywrightService = {
  openBrowser: {
    path: '/Playwright/OpenBrowser',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.openBrowserRequest,
    responseType: playwright_pb.Response,
    requestSerialize: serialize_openBrowserRequest,
    requestDeserialize: deserialize_openBrowserRequest,
    responseSerialize: serialize_Response,
    responseDeserialize: deserialize_Response,
  },
  closeBrowser: {
    path: '/Playwright/CloseBrowser',
    requestStream: false,
    responseStream: false,
    requestType: playwright_pb.Empty,
    responseType: playwright_pb.Response,
    requestSerialize: serialize_Empty,
    requestDeserialize: deserialize_Empty,
    responseSerialize: serialize_Response,
    responseDeserialize: deserialize_Response,
  },
};

exports.PlaywrightClient = grpc.makeGenericClientConstructor(PlaywrightService);
