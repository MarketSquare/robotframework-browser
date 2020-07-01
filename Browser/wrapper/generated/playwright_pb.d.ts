// package: 
// file: playwright.proto

/* tslint:disable */
/* eslint-disable */

import * as jspb from "google-protobuf";

export class Request extends jspb.Message { 

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): Request.AsObject;
    static toObject(includeInstance: boolean, msg: Request): Request.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: Request, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): Request;
    static deserializeBinaryFromReader(message: Request, reader: jspb.BinaryReader): Request;
}

export namespace Request {
    export type AsObject = {
    }


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

    export class screenshot extends jspb.Message { 
        getPath(): string;
        setPath(value: string): screenshot;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): screenshot.AsObject;
        static toObject(includeInstance: boolean, msg: screenshot): screenshot.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: screenshot, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): screenshot;
        static deserializeBinaryFromReader(message: screenshot, reader: jspb.BinaryReader): screenshot;
    }

    export namespace screenshot {
        export type AsObject = {
            path: string,
        }
    }

    export class openBrowser extends jspb.Message { 
        getUrl(): string;
        setUrl(value: string): openBrowser;

        getBrowser(): string;
        setBrowser(value: string): openBrowser;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): openBrowser.AsObject;
        static toObject(includeInstance: boolean, msg: openBrowser): openBrowser.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: openBrowser, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): openBrowser;
        static deserializeBinaryFromReader(message: openBrowser, reader: jspb.BinaryReader): openBrowser;
    }

    export namespace openBrowser {
        export type AsObject = {
            url: string,
            browser: string,
        }
    }

    export class goTo extends jspb.Message { 
        getUrl(): string;
        setUrl(value: string): goTo;

        getTimeout(): number;
        setTimeout(value: number): goTo;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): goTo.AsObject;
        static toObject(includeInstance: boolean, msg: goTo): goTo.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: goTo, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): goTo;
        static deserializeBinaryFromReader(message: goTo, reader: jspb.BinaryReader): goTo;
    }

    export namespace goTo {
        export type AsObject = {
            url: string,
            timeout: number,
        }
    }

    export class inputText extends jspb.Message { 
        getInput(): string;
        setInput(value: string): inputText;

        getSelector(): string;
        setSelector(value: string): inputText;

        getType(): boolean;
        setType(value: boolean): inputText;

        getTimeout(): number;
        setTimeout(value: number): inputText;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): inputText.AsObject;
        static toObject(includeInstance: boolean, msg: inputText): inputText.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: inputText, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): inputText;
        static deserializeBinaryFromReader(message: inputText, reader: jspb.BinaryReader): inputText;
    }

    export namespace inputText {
        export type AsObject = {
            input: string,
            selector: string,
            type: boolean,
            timeout: number,
        }
    }

    export class getDomProperty extends jspb.Message { 
        getProperty(): string;
        setProperty(value: string): getDomProperty;

        getSelector(): string;
        setSelector(value: string): getDomProperty;

        getTimeout(): number;
        setTimeout(value: number): getDomProperty;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): getDomProperty.AsObject;
        static toObject(includeInstance: boolean, msg: getDomProperty): getDomProperty.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: getDomProperty, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): getDomProperty;
        static deserializeBinaryFromReader(message: getDomProperty, reader: jspb.BinaryReader): getDomProperty;
    }

    export namespace getDomProperty {
        export type AsObject = {
            property: string,
            selector: string,
            timeout: number,
        }
    }

    export class press extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): press;

        clearKeyList(): void;
        getKeyList(): Array<string>;
        setKeyList(value: Array<string>): press;
        addKey(value: string, index?: number): string;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): press.AsObject;
        static toObject(includeInstance: boolean, msg: press): press.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: press, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): press;
        static deserializeBinaryFromReader(message: press, reader: jspb.BinaryReader): press;
    }

    export namespace press {
        export type AsObject = {
            selector: string,
            keyList: Array<string>,
        }
    }

    export class selector extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): selector;

        getTimeout(): number;
        setTimeout(value: number): selector;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): selector.AsObject;
        static toObject(includeInstance: boolean, msg: selector): selector.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: selector, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): selector;
        static deserializeBinaryFromReader(message: selector, reader: jspb.BinaryReader): selector;
    }

    export namespace selector {
        export type AsObject = {
            selector: string,
            timeout: number,
        }
    }

}

export class Response extends jspb.Message { 

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
    }


    export class Empty extends jspb.Message { 
        getLog(): string;
        setLog(value: string): Empty;


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
            log: string,
        }
    }

    export class String extends jspb.Message { 
        getLog(): string;
        setLog(value: string): String;

        getBody(): string;
        setBody(value: string): String;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): String.AsObject;
        static toObject(includeInstance: boolean, msg: String): String.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: String, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): String;
        static deserializeBinaryFromReader(message: String, reader: jspb.BinaryReader): String;
    }

    export namespace String {
        export type AsObject = {
            log: string,
            body: string,
        }
    }

    export class Bool extends jspb.Message { 
        getLog(): string;
        setLog(value: string): Bool;

        getBody(): boolean;
        setBody(value: boolean): Bool;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Bool.AsObject;
        static toObject(includeInstance: boolean, msg: Bool): Bool.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Bool, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Bool;
        static deserializeBinaryFromReader(message: Bool, reader: jspb.BinaryReader): Bool;
    }

    export namespace Bool {
        export type AsObject = {
            log: string,
            body: boolean,
        }
    }

}
