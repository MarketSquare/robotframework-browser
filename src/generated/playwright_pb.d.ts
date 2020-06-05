// package: 
// file: playwright.proto

/* tslint:disable */
/* eslint-disable */

import * as jspb from "google-protobuf";

export class Empty extends jspb.Message { 

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): Empty.AsObject;
    static toObject(includeInstance: boolean, msg: Empty): Empty.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: Empty, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): Empty;
    static deserializeBinaryFromReader(message: Empty, reader: jspb.BinaryReader): Empty;
}

export namespace Empty {
    export type AsObject = {
    }
}

export class openBrowserRequest extends jspb.Message { 
    getUrl(): string;
    setUrl(value: string): openBrowserRequest;

    getBrowser(): string;
    setBrowser(value: string): openBrowserRequest;


    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): openBrowserRequest.AsObject;
    static toObject(includeInstance: boolean, msg: openBrowserRequest): openBrowserRequest.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: openBrowserRequest, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): openBrowserRequest;
    static deserializeBinaryFromReader(message: openBrowserRequest, reader: jspb.BinaryReader): openBrowserRequest;
}

export namespace openBrowserRequest {
    export type AsObject = {
        url: string,
        browser: string,
    }
}

export class Response extends jspb.Message { 
    getLog(): string;
    setLog(value: string): Response;


    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): Response.AsObject;
    static toObject(includeInstance: boolean, msg: Response): Response.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: Response, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): Response;
    static deserializeBinaryFromReader(message: Response, reader: jspb.BinaryReader): Response;
}

export namespace Response {
    export type AsObject = {
        log: string,
    }
}
