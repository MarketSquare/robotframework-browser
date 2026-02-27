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

    export class AriaSnapShot extends jspb.Message { 
        getLocator(): string;
        setLocator(value: string): AriaSnapShot;
        getStrict(): boolean;
        setStrict(value: boolean): AriaSnapShot;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): AriaSnapShot.AsObject;
        static toObject(includeInstance: boolean, msg: AriaSnapShot): AriaSnapShot.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: AriaSnapShot, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): AriaSnapShot;
        static deserializeBinaryFromReader(message: AriaSnapShot, reader: jspb.BinaryReader): AriaSnapShot;
    }

    export namespace AriaSnapShot {
        export type AsObject = {
            locator: string,
            strict: boolean,
        }
    }

    export class ClosePage extends jspb.Message { 
        getRunbeforeunload(): boolean;
        setRunbeforeunload(value: boolean): ClosePage;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ClosePage.AsObject;
        static toObject(includeInstance: boolean, msg: ClosePage): ClosePage.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ClosePage, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ClosePage;
        static deserializeBinaryFromReader(message: ClosePage, reader: jspb.BinaryReader): ClosePage;
    }

    export namespace ClosePage {
        export type AsObject = {
            runbeforeunload: boolean,
        }
    }

    export class ClockSetTime extends jspb.Message { 
        getTime(): number;
        setTime(value: number): ClockSetTime;
        getSettype(): string;
        setSettype(value: string): ClockSetTime;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ClockSetTime.AsObject;
        static toObject(includeInstance: boolean, msg: ClockSetTime): ClockSetTime.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ClockSetTime, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ClockSetTime;
        static deserializeBinaryFromReader(message: ClockSetTime, reader: jspb.BinaryReader): ClockSetTime;
    }

    export namespace ClockSetTime {
        export type AsObject = {
            time: number,
            settype: string,
        }
    }

    export class ClockAdvance extends jspb.Message { 
        getTime(): number;
        setTime(value: number): ClockAdvance;
        getAdvancetype(): string;
        setAdvancetype(value: string): ClockAdvance;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ClockAdvance.AsObject;
        static toObject(includeInstance: boolean, msg: ClockAdvance): ClockAdvance.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ClockAdvance, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ClockAdvance;
        static deserializeBinaryFromReader(message: ClockAdvance, reader: jspb.BinaryReader): ClockAdvance;
    }

    export namespace ClockAdvance {
        export type AsObject = {
            time: number,
            advancetype: string,
        }
    }

    export class CoverageStart extends jspb.Message { 
        getCoveragetype(): string;
        setCoveragetype(value: string): CoverageStart;
        getResetonnavigation(): boolean;
        setResetonnavigation(value: boolean): CoverageStart;
        getReportanonymousscripts(): boolean;
        setReportanonymousscripts(value: boolean): CoverageStart;
        getConfigfile(): string;
        setConfigfile(value: string): CoverageStart;
        getCoveragedir(): string;
        setCoveragedir(value: string): CoverageStart;
        getRaw(): boolean;
        setRaw(value: boolean): CoverageStart;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): CoverageStart.AsObject;
        static toObject(includeInstance: boolean, msg: CoverageStart): CoverageStart.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: CoverageStart, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): CoverageStart;
        static deserializeBinaryFromReader(message: CoverageStart, reader: jspb.BinaryReader): CoverageStart;
    }

    export namespace CoverageStart {
        export type AsObject = {
            coveragetype: string,
            resetonnavigation: boolean,
            reportanonymousscripts: boolean,
            configfile: string,
            coveragedir: string,
            raw: boolean,
        }
    }

    export class CoverageMerge extends jspb.Message { 
        getInputFolder(): string;
        setInputFolder(value: string): CoverageMerge;
        getOutputFolder(): string;
        setOutputFolder(value: string): CoverageMerge;
        getConfig(): string;
        setConfig(value: string): CoverageMerge;
        getName(): string;
        setName(value: string): CoverageMerge;
        clearReportsList(): void;
        getReportsList(): Array<string>;
        setReportsList(value: Array<string>): CoverageMerge;
        addReports(value: string, index?: number): string;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): CoverageMerge.AsObject;
        static toObject(includeInstance: boolean, msg: CoverageMerge): CoverageMerge.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: CoverageMerge, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): CoverageMerge;
        static deserializeBinaryFromReader(message: CoverageMerge, reader: jspb.BinaryReader): CoverageMerge;
    }

    export namespace CoverageMerge {
        export type AsObject = {
            inputFolder: string,
            outputFolder: string,
            config: string,
            name: string,
            reportsList: Array<string>,
        }
    }

    export class TraceGroup extends jspb.Message { 
        getName(): string;
        setName(value: string): TraceGroup;
        getFile(): string;
        setFile(value: string): TraceGroup;
        getLine(): number;
        setLine(value: number): TraceGroup;
        getColumn(): number;
        setColumn(value: number): TraceGroup;
        getContextid(): string;
        setContextid(value: string): TraceGroup;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): TraceGroup.AsObject;
        static toObject(includeInstance: boolean, msg: TraceGroup): TraceGroup.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: TraceGroup, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): TraceGroup;
        static deserializeBinaryFromReader(message: TraceGroup, reader: jspb.BinaryReader): TraceGroup;
    }

    export namespace TraceGroup {
        export type AsObject = {
            name: string,
            file: string,
            line: number,
            column: number,
            contextid: string,
        }
    }

    export class Label extends jspb.Message { 
        getLabel(): string;
        setLabel(value: string): Label;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Label.AsObject;
        static toObject(includeInstance: boolean, msg: Label): Label.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Label, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Label;
        static deserializeBinaryFromReader(message: Label, reader: jspb.BinaryReader): Label;
    }

    export namespace Label {
        export type AsObject = {
            label: string,
        }
    }

    export class GetByOptions extends jspb.Message { 
        getStrategy(): string;
        setStrategy(value: string): GetByOptions;
        getText(): string;
        setText(value: string): GetByOptions;
        getOptions(): string;
        setOptions(value: string): GetByOptions;
        getStrict(): boolean;
        setStrict(value: boolean): GetByOptions;
        getAll(): boolean;
        setAll(value: boolean): GetByOptions;
        getFrameselector(): string;
        setFrameselector(value: string): GetByOptions;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): GetByOptions.AsObject;
        static toObject(includeInstance: boolean, msg: GetByOptions): GetByOptions.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: GetByOptions, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): GetByOptions;
        static deserializeBinaryFromReader(message: GetByOptions, reader: jspb.BinaryReader): GetByOptions;
    }

    export namespace GetByOptions {
        export type AsObject = {
            strategy: string,
            text: string,
            options: string,
            strict: boolean,
            all: boolean,
            frameselector: string,
        }
    }

    export class Pdf extends jspb.Message { 
        getDisplayheaderfooter(): boolean;
        setDisplayheaderfooter(value: boolean): Pdf;
        getFootertemplate(): string;
        setFootertemplate(value: string): Pdf;
        getFormat(): string;
        setFormat(value: string): Pdf;
        getHeadertemplate(): string;
        setHeadertemplate(value: string): Pdf;
        getHeight(): string;
        setHeight(value: string): Pdf;
        getLandscape(): boolean;
        setLandscape(value: boolean): Pdf;
        getMargin(): string;
        setMargin(value: string): Pdf;
        getOutline(): boolean;
        setOutline(value: boolean): Pdf;
        getPageranges(): string;
        setPageranges(value: string): Pdf;
        getPath(): string;
        setPath(value: string): Pdf;
        getPrefercsspagesize(): boolean;
        setPrefercsspagesize(value: boolean): Pdf;
        getPrintbackground(): boolean;
        setPrintbackground(value: boolean): Pdf;
        getScale(): number;
        setScale(value: number): Pdf;
        getTagged(): boolean;
        setTagged(value: boolean): Pdf;
        getWidth(): string;
        setWidth(value: string): Pdf;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Pdf.AsObject;
        static toObject(includeInstance: boolean, msg: Pdf): Pdf.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Pdf, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Pdf;
        static deserializeBinaryFromReader(message: Pdf, reader: jspb.BinaryReader): Pdf;
    }

    export namespace Pdf {
        export type AsObject = {
            displayheaderfooter: boolean,
            footertemplate: string,
            format: string,
            headertemplate: string,
            height: string,
            landscape: boolean,
            margin: string,
            outline: boolean,
            pageranges: string,
            path: string,
            prefercsspagesize: boolean,
            printbackground: boolean,
            scale: number,
            tagged: boolean,
            width: string,
        }
    }

    export class EmulateMedia extends jspb.Message { 
        getColorscheme(): string;
        setColorscheme(value: string): EmulateMedia;
        getForcedcolors(): string;
        setForcedcolors(value: string): EmulateMedia;
        getMedia(): string;
        setMedia(value: string): EmulateMedia;
        getReducedmotion(): string;
        setReducedmotion(value: string): EmulateMedia;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): EmulateMedia.AsObject;
        static toObject(includeInstance: boolean, msg: EmulateMedia): EmulateMedia.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: EmulateMedia, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): EmulateMedia;
        static deserializeBinaryFromReader(message: EmulateMedia, reader: jspb.BinaryReader): EmulateMedia;
    }

    export namespace EmulateMedia {
        export type AsObject = {
            colorscheme: string,
            forcedcolors: string,
            media: string,
            reducedmotion: string,
        }
    }

    export class ScreenshotOptions extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): ScreenshotOptions;
        getMask(): string;
        setMask(value: string): ScreenshotOptions;
        getOptions(): string;
        setOptions(value: string): ScreenshotOptions;
        getStrict(): boolean;
        setStrict(value: boolean): ScreenshotOptions;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ScreenshotOptions.AsObject;
        static toObject(includeInstance: boolean, msg: ScreenshotOptions): ScreenshotOptions.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ScreenshotOptions, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ScreenshotOptions;
        static deserializeBinaryFromReader(message: ScreenshotOptions, reader: jspb.BinaryReader): ScreenshotOptions;
    }

    export namespace ScreenshotOptions {
        export type AsObject = {
            selector: string,
            mask: string,
            options: string,
            strict: boolean,
        }
    }

    export class KeywordCall extends jspb.Message { 
        getName(): string;
        setName(value: string): KeywordCall;
        getArguments(): string;
        setArguments(value: string): KeywordCall;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): KeywordCall.AsObject;
        static toObject(includeInstance: boolean, msg: KeywordCall): KeywordCall.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: KeywordCall, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): KeywordCall;
        static deserializeBinaryFromReader(message: KeywordCall, reader: jspb.BinaryReader): KeywordCall;
    }

    export namespace KeywordCall {
        export type AsObject = {
            name: string,
            arguments: string,
        }
    }

    export class FilePath extends jspb.Message { 
        getPath(): string;
        setPath(value: string): FilePath;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): FilePath.AsObject;
        static toObject(includeInstance: boolean, msg: FilePath): FilePath.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: FilePath, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): FilePath;
        static deserializeBinaryFromReader(message: FilePath, reader: jspb.BinaryReader): FilePath;
    }

    export namespace FilePath {
        export type AsObject = {
            path: string,
        }
    }

    export class FileBySelector extends jspb.Message { 
        clearPathList(): void;
        getPathList(): Array<string>;
        setPathList(value: Array<string>): FileBySelector;
        addPath(value: string, index?: number): string;
        getSelector(): string;
        setSelector(value: string): FileBySelector;
        getStrict(): boolean;
        setStrict(value: boolean): FileBySelector;
        getName(): string;
        setName(value: string): FileBySelector;
        getMimetype(): string;
        setMimetype(value: string): FileBySelector;
        getBuffer(): string;
        setBuffer(value: string): FileBySelector;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): FileBySelector.AsObject;
        static toObject(includeInstance: boolean, msg: FileBySelector): FileBySelector.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: FileBySelector, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): FileBySelector;
        static deserializeBinaryFromReader(message: FileBySelector, reader: jspb.BinaryReader): FileBySelector;
    }

    export namespace FileBySelector {
        export type AsObject = {
            pathList: Array<string>,
            selector: string,
            strict: boolean,
            name: string,
            mimetype: string,
            buffer: string,
        }
    }

    export class LocatorHandlerAddCustom extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): LocatorHandlerAddCustom;
        getNowaitafter(): boolean;
        setNowaitafter(value: boolean): LocatorHandlerAddCustom;
        getTimes(): string;
        setTimes(value: string): LocatorHandlerAddCustom;
        clearHandlerspecsList(): void;
        getHandlerspecsList(): Array<Request.LocatorHandlerAddCustomAction>;
        setHandlerspecsList(value: Array<Request.LocatorHandlerAddCustomAction>): LocatorHandlerAddCustom;
        addHandlerspecs(value?: Request.LocatorHandlerAddCustomAction, index?: number): Request.LocatorHandlerAddCustomAction;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): LocatorHandlerAddCustom.AsObject;
        static toObject(includeInstance: boolean, msg: LocatorHandlerAddCustom): LocatorHandlerAddCustom.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: LocatorHandlerAddCustom, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): LocatorHandlerAddCustom;
        static deserializeBinaryFromReader(message: LocatorHandlerAddCustom, reader: jspb.BinaryReader): LocatorHandlerAddCustom;
    }

    export namespace LocatorHandlerAddCustom {
        export type AsObject = {
            selector: string,
            nowaitafter: boolean,
            times: string,
            handlerspecsList: Array<Request.LocatorHandlerAddCustomAction.AsObject>,
        }
    }

    export class LocatorHandlerAddCustomAction extends jspb.Message { 
        getAction(): string;
        setAction(value: string): LocatorHandlerAddCustomAction;
        getSelector(): string;
        setSelector(value: string): LocatorHandlerAddCustomAction;
        getValue(): string;
        setValue(value: string): LocatorHandlerAddCustomAction;
        getOptionsasjson(): string;
        setOptionsasjson(value: string): LocatorHandlerAddCustomAction;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): LocatorHandlerAddCustomAction.AsObject;
        static toObject(includeInstance: boolean, msg: LocatorHandlerAddCustomAction): LocatorHandlerAddCustomAction.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: LocatorHandlerAddCustomAction, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): LocatorHandlerAddCustomAction;
        static deserializeBinaryFromReader(message: LocatorHandlerAddCustomAction, reader: jspb.BinaryReader): LocatorHandlerAddCustomAction;
    }

    export namespace LocatorHandlerAddCustomAction {
        export type AsObject = {
            action: string,
            selector: string,
            value: string,
            optionsasjson: string,
        }
    }

    export class LocatorHandlerRemove extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): LocatorHandlerRemove;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): LocatorHandlerRemove.AsObject;
        static toObject(includeInstance: boolean, msg: LocatorHandlerRemove): LocatorHandlerRemove.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: LocatorHandlerRemove, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): LocatorHandlerRemove;
        static deserializeBinaryFromReader(message: LocatorHandlerRemove, reader: jspb.BinaryReader): LocatorHandlerRemove;
    }

    export namespace LocatorHandlerRemove {
        export type AsObject = {
            selector: string,
        }
    }

    export class Json extends jspb.Message { 
        getBody(): string;
        setBody(value: string): Json;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Json.AsObject;
        static toObject(includeInstance: boolean, msg: Json): Json.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Json, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Json;
        static deserializeBinaryFromReader(message: Json, reader: jspb.BinaryReader): Json;
    }

    export namespace Json {
        export type AsObject = {
            body: string,
        }
    }

    export class MouseButtonOptions extends jspb.Message { 
        getAction(): string;
        setAction(value: string): MouseButtonOptions;
        getJson(): string;
        setJson(value: string): MouseButtonOptions;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): MouseButtonOptions.AsObject;
        static toObject(includeInstance: boolean, msg: MouseButtonOptions): MouseButtonOptions.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: MouseButtonOptions, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): MouseButtonOptions;
        static deserializeBinaryFromReader(message: MouseButtonOptions, reader: jspb.BinaryReader): MouseButtonOptions;
    }

    export namespace MouseButtonOptions {
        export type AsObject = {
            action: string,
            json: string,
        }
    }

    export class MouseWheel extends jspb.Message { 
        getDeltax(): number;
        setDeltax(value: number): MouseWheel;
        getDeltay(): number;
        setDeltay(value: number): MouseWheel;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): MouseWheel.AsObject;
        static toObject(includeInstance: boolean, msg: MouseWheel): MouseWheel.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: MouseWheel, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): MouseWheel;
        static deserializeBinaryFromReader(message: MouseWheel, reader: jspb.BinaryReader): MouseWheel;
    }

    export namespace MouseWheel {
        export type AsObject = {
            deltax: number,
            deltay: number,
        }
    }

    export class KeyboardKeypress extends jspb.Message { 
        getAction(): string;
        setAction(value: string): KeyboardKeypress;
        getKey(): string;
        setKey(value: string): KeyboardKeypress;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): KeyboardKeypress.AsObject;
        static toObject(includeInstance: boolean, msg: KeyboardKeypress): KeyboardKeypress.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: KeyboardKeypress, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): KeyboardKeypress;
        static deserializeBinaryFromReader(message: KeyboardKeypress, reader: jspb.BinaryReader): KeyboardKeypress;
    }

    export namespace KeyboardKeypress {
        export type AsObject = {
            action: string,
            key: string,
        }
    }

    export class KeyboardInputOptions extends jspb.Message { 
        getAction(): string;
        setAction(value: string): KeyboardInputOptions;
        getInput(): string;
        setInput(value: string): KeyboardInputOptions;
        getDelay(): number;
        setDelay(value: number): KeyboardInputOptions;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): KeyboardInputOptions.AsObject;
        static toObject(includeInstance: boolean, msg: KeyboardInputOptions): KeyboardInputOptions.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: KeyboardInputOptions, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): KeyboardInputOptions;
        static deserializeBinaryFromReader(message: KeyboardInputOptions, reader: jspb.BinaryReader): KeyboardInputOptions;
    }

    export namespace KeyboardInputOptions {
        export type AsObject = {
            action: string,
            input: string,
            delay: number,
        }
    }

    export class Browser extends jspb.Message { 
        getBrowser(): string;
        setBrowser(value: string): Browser;
        getRawoptions(): string;
        setRawoptions(value: string): Browser;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Browser.AsObject;
        static toObject(includeInstance: boolean, msg: Browser): Browser.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Browser, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Browser;
        static deserializeBinaryFromReader(message: Browser, reader: jspb.BinaryReader): Browser;
    }

    export namespace Browser {
        export type AsObject = {
            browser: string,
            rawoptions: string,
        }
    }

    export class Context extends jspb.Message { 
        getRawoptions(): string;
        setRawoptions(value: string): Context;
        getDefaulttimeout(): number;
        setDefaulttimeout(value: number): Context;
        getTracefile(): string;
        setTracefile(value: string): Context;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Context.AsObject;
        static toObject(includeInstance: boolean, msg: Context): Context.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Context, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Context;
        static deserializeBinaryFromReader(message: Context, reader: jspb.BinaryReader): Context;
    }

    export namespace Context {
        export type AsObject = {
            rawoptions: string,
            defaulttimeout: number,
            tracefile: string,
        }
    }

    export class PersistentContext extends jspb.Message { 
        getBrowser(): string;
        setBrowser(value: string): PersistentContext;
        getRawoptions(): string;
        setRawoptions(value: string): PersistentContext;
        getDefaulttimeout(): number;
        setDefaulttimeout(value: number): PersistentContext;
        getTracefile(): string;
        setTracefile(value: string): PersistentContext;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): PersistentContext.AsObject;
        static toObject(includeInstance: boolean, msg: PersistentContext): PersistentContext.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: PersistentContext, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): PersistentContext;
        static deserializeBinaryFromReader(message: PersistentContext, reader: jspb.BinaryReader): PersistentContext;
    }

    export namespace PersistentContext {
        export type AsObject = {
            browser: string,
            rawoptions: string,
            defaulttimeout: number,
            tracefile: string,
        }
    }

    export class ElectronLaunch extends jspb.Message { 
        getExecutablePath(): string;
        setExecutablePath(value: string): ElectronLaunch;
        clearArgsList(): void;
        getArgsList(): Array<string>;
        setArgsList(value: Array<string>): ElectronLaunch;
        addArgs(value: string, index?: number): string;

        getEnvMap(): jspb.Map<string, string>;
        clearEnvMap(): void;
        getTimeout(): number;
        setTimeout(value: number): ElectronLaunch;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ElectronLaunch.AsObject;
        static toObject(includeInstance: boolean, msg: ElectronLaunch): ElectronLaunch.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ElectronLaunch, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ElectronLaunch;
        static deserializeBinaryFromReader(message: ElectronLaunch, reader: jspb.BinaryReader): ElectronLaunch;
    }

    export namespace ElectronLaunch {
        export type AsObject = {
            executablePath: string,
            argsList: Array<string>,

            envMap: Array<[string, string]>,
            timeout: number,
        }
    }

    export class Permissions extends jspb.Message { 
        clearPermissionsList(): void;
        getPermissionsList(): Array<string>;
        setPermissionsList(value: Array<string>): Permissions;
        addPermissions(value: string, index?: number): string;
        getOrigin(): string;
        setOrigin(value: string): Permissions;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Permissions.AsObject;
        static toObject(includeInstance: boolean, msg: Permissions): Permissions.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Permissions, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Permissions;
        static deserializeBinaryFromReader(message: Permissions, reader: jspb.BinaryReader): Permissions;
    }

    export namespace Permissions {
        export type AsObject = {
            permissionsList: Array<string>,
            origin: string,
        }
    }

    export class Url extends jspb.Message { 
        getUrl(): string;
        setUrl(value: string): Url;
        getDefaulttimeout(): number;
        setDefaulttimeout(value: number): Url;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Url.AsObject;
        static toObject(includeInstance: boolean, msg: Url): Url.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Url, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Url;
        static deserializeBinaryFromReader(message: Url, reader: jspb.BinaryReader): Url;
    }

    export namespace Url {
        export type AsObject = {
            url: string,
            defaulttimeout: number,
        }
    }

    export class DownloadOptions extends jspb.Message { 
        getUrl(): string;
        setUrl(value: string): DownloadOptions;
        getPath(): string;
        setPath(value: string): DownloadOptions;
        getWaitforfinish(): boolean;
        setWaitforfinish(value: boolean): DownloadOptions;
        getDownloadtimeout(): number;
        setDownloadtimeout(value: number): DownloadOptions;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): DownloadOptions.AsObject;
        static toObject(includeInstance: boolean, msg: DownloadOptions): DownloadOptions.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: DownloadOptions, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): DownloadOptions;
        static deserializeBinaryFromReader(message: DownloadOptions, reader: jspb.BinaryReader): DownloadOptions;
    }

    export namespace DownloadOptions {
        export type AsObject = {
            url: string,
            path: string,
            waitforfinish: boolean,
            downloadtimeout: number,
        }
    }

    export class DownloadID extends jspb.Message { 
        getId(): string;
        setId(value: string): DownloadID;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): DownloadID.AsObject;
        static toObject(includeInstance: boolean, msg: DownloadID): DownloadID.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: DownloadID, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): DownloadID;
        static deserializeBinaryFromReader(message: DownloadID, reader: jspb.BinaryReader): DownloadID;
    }

    export namespace DownloadID {
        export type AsObject = {
            id: string,
        }
    }

    export class UrlOptions extends jspb.Message { 

        hasUrl(): boolean;
        clearUrl(): void;
        getUrl(): Request.Url | undefined;
        setUrl(value?: Request.Url): UrlOptions;
        getWaituntil(): string;
        setWaituntil(value: string): UrlOptions;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): UrlOptions.AsObject;
        static toObject(includeInstance: boolean, msg: UrlOptions): UrlOptions.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: UrlOptions, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): UrlOptions;
        static deserializeBinaryFromReader(message: UrlOptions, reader: jspb.BinaryReader): UrlOptions;
    }

    export namespace UrlOptions {
        export type AsObject = {
            url?: Request.Url.AsObject,
            waituntil: string,
        }
    }

    export class PageLoadState extends jspb.Message { 
        getState(): string;
        setState(value: string): PageLoadState;
        getTimeout(): number;
        setTimeout(value: number): PageLoadState;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): PageLoadState.AsObject;
        static toObject(includeInstance: boolean, msg: PageLoadState): PageLoadState.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: PageLoadState, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): PageLoadState;
        static deserializeBinaryFromReader(message: PageLoadState, reader: jspb.BinaryReader): PageLoadState;
    }

    export namespace PageLoadState {
        export type AsObject = {
            state: string,
            timeout: number,
        }
    }

    export class ConnectBrowser extends jspb.Message { 
        getBrowser(): string;
        setBrowser(value: string): ConnectBrowser;
        getUrl(): string;
        setUrl(value: string): ConnectBrowser;
        getConnectcdp(): boolean;
        setConnectcdp(value: boolean): ConnectBrowser;
        getTimeout(): number;
        setTimeout(value: number): ConnectBrowser;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ConnectBrowser.AsObject;
        static toObject(includeInstance: boolean, msg: ConnectBrowser): ConnectBrowser.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ConnectBrowser, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ConnectBrowser;
        static deserializeBinaryFromReader(message: ConnectBrowser, reader: jspb.BinaryReader): ConnectBrowser;
    }

    export namespace ConnectBrowser {
        export type AsObject = {
            browser: string,
            url: string,
            connectcdp: boolean,
            timeout: number,
        }
    }

    export class TextInput extends jspb.Message { 
        getInput(): string;
        setInput(value: string): TextInput;
        getSelector(): string;
        setSelector(value: string): TextInput;
        getType(): boolean;
        setType(value: boolean): TextInput;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): TextInput.AsObject;
        static toObject(includeInstance: boolean, msg: TextInput): TextInput.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: TextInput, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): TextInput;
        static deserializeBinaryFromReader(message: TextInput, reader: jspb.BinaryReader): TextInput;
    }

    export namespace TextInput {
        export type AsObject = {
            input: string,
            selector: string,
            type: boolean,
        }
    }

    export class ElementProperty extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): ElementProperty;
        getProperty(): string;
        setProperty(value: string): ElementProperty;
        getStrict(): boolean;
        setStrict(value: boolean): ElementProperty;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ElementProperty.AsObject;
        static toObject(includeInstance: boolean, msg: ElementProperty): ElementProperty.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ElementProperty, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ElementProperty;
        static deserializeBinaryFromReader(message: ElementProperty, reader: jspb.BinaryReader): ElementProperty;
    }

    export namespace ElementProperty {
        export type AsObject = {
            selector: string,
            property: string,
            strict: boolean,
        }
    }

    export class TypeText extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): TypeText;
        getText(): string;
        setText(value: string): TypeText;
        getDelay(): number;
        setDelay(value: number): TypeText;
        getClear(): boolean;
        setClear(value: boolean): TypeText;
        getStrict(): boolean;
        setStrict(value: boolean): TypeText;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): TypeText.AsObject;
        static toObject(includeInstance: boolean, msg: TypeText): TypeText.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: TypeText, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): TypeText;
        static deserializeBinaryFromReader(message: TypeText, reader: jspb.BinaryReader): TypeText;
    }

    export namespace TypeText {
        export type AsObject = {
            selector: string,
            text: string,
            delay: number,
            clear: boolean,
            strict: boolean,
        }
    }

    export class FillText extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): FillText;
        getText(): string;
        setText(value: string): FillText;
        getStrict(): boolean;
        setStrict(value: boolean): FillText;
        getForce(): boolean;
        setForce(value: boolean): FillText;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): FillText.AsObject;
        static toObject(includeInstance: boolean, msg: FillText): FillText.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: FillText, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): FillText;
        static deserializeBinaryFromReader(message: FillText, reader: jspb.BinaryReader): FillText;
    }

    export namespace FillText {
        export type AsObject = {
            selector: string,
            text: string,
            strict: boolean,
            force: boolean,
        }
    }

    export class ClearText extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): ClearText;
        getStrict(): boolean;
        setStrict(value: boolean): ClearText;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ClearText.AsObject;
        static toObject(includeInstance: boolean, msg: ClearText): ClearText.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ClearText, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ClearText;
        static deserializeBinaryFromReader(message: ClearText, reader: jspb.BinaryReader): ClearText;
    }

    export namespace ClearText {
        export type AsObject = {
            selector: string,
            strict: boolean,
        }
    }

    export class PressKeys extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): PressKeys;
        getStrict(): boolean;
        setStrict(value: boolean): PressKeys;
        clearKeyList(): void;
        getKeyList(): Array<string>;
        setKeyList(value: Array<string>): PressKeys;
        addKey(value: string, index?: number): string;
        getPressdelay(): number;
        setPressdelay(value: number): PressKeys;
        getKeydelay(): number;
        setKeydelay(value: number): PressKeys;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): PressKeys.AsObject;
        static toObject(includeInstance: boolean, msg: PressKeys): PressKeys.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: PressKeys, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): PressKeys;
        static deserializeBinaryFromReader(message: PressKeys, reader: jspb.BinaryReader): PressKeys;
    }

    export namespace PressKeys {
        export type AsObject = {
            selector: string,
            strict: boolean,
            keyList: Array<string>,
            pressdelay: number,
            keydelay: number,
        }
    }

    export class ElementSelector extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): ElementSelector;
        getStrict(): boolean;
        setStrict(value: boolean): ElementSelector;
        getForce(): boolean;
        setForce(value: boolean): ElementSelector;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ElementSelector.AsObject;
        static toObject(includeInstance: boolean, msg: ElementSelector): ElementSelector.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ElementSelector, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ElementSelector;
        static deserializeBinaryFromReader(message: ElementSelector, reader: jspb.BinaryReader): ElementSelector;
    }

    export namespace ElementSelector {
        export type AsObject = {
            selector: string,
            strict: boolean,
            force: boolean,
        }
    }

    export class Timeout extends jspb.Message { 
        getTimeout(): number;
        setTimeout(value: number): Timeout;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Timeout.AsObject;
        static toObject(includeInstance: boolean, msg: Timeout): Timeout.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Timeout, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Timeout;
        static deserializeBinaryFromReader(message: Timeout, reader: jspb.BinaryReader): Timeout;
    }

    export namespace Timeout {
        export type AsObject = {
            timeout: number,
        }
    }

    export class Index extends jspb.Message { 
        getIndex(): string;
        setIndex(value: string): Index;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Index.AsObject;
        static toObject(includeInstance: boolean, msg: Index): Index.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Index, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Index;
        static deserializeBinaryFromReader(message: Index, reader: jspb.BinaryReader): Index;
    }

    export namespace Index {
        export type AsObject = {
            index: string,
        }
    }

    export class IdWithTimeout extends jspb.Message { 
        getId(): string;
        setId(value: string): IdWithTimeout;
        getTimeout(): number;
        setTimeout(value: number): IdWithTimeout;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): IdWithTimeout.AsObject;
        static toObject(includeInstance: boolean, msg: IdWithTimeout): IdWithTimeout.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: IdWithTimeout, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): IdWithTimeout;
        static deserializeBinaryFromReader(message: IdWithTimeout, reader: jspb.BinaryReader): IdWithTimeout;
    }

    export namespace IdWithTimeout {
        export type AsObject = {
            id: string,
            timeout: number,
        }
    }

    export class StyleTag extends jspb.Message { 
        getContent(): string;
        setContent(value: string): StyleTag;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): StyleTag.AsObject;
        static toObject(includeInstance: boolean, msg: StyleTag): StyleTag.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: StyleTag, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): StyleTag;
        static deserializeBinaryFromReader(message: StyleTag, reader: jspb.BinaryReader): StyleTag;
    }

    export namespace StyleTag {
        export type AsObject = {
            content: string,
        }
    }

    export class ElementSelectorWithOptions extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): ElementSelectorWithOptions;
        getOptions(): string;
        setOptions(value: string): ElementSelectorWithOptions;
        getStrict(): boolean;
        setStrict(value: boolean): ElementSelectorWithOptions;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ElementSelectorWithOptions.AsObject;
        static toObject(includeInstance: boolean, msg: ElementSelectorWithOptions): ElementSelectorWithOptions.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ElementSelectorWithOptions, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ElementSelectorWithOptions;
        static deserializeBinaryFromReader(message: ElementSelectorWithOptions, reader: jspb.BinaryReader): ElementSelectorWithOptions;
    }

    export namespace ElementSelectorWithOptions {
        export type AsObject = {
            selector: string,
            options: string,
            strict: boolean,
        }
    }

    export class ElementSelectorWithDuration extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): ElementSelectorWithDuration;
        getDuration(): number;
        setDuration(value: number): ElementSelectorWithDuration;
        getWidth(): string;
        setWidth(value: string): ElementSelectorWithDuration;
        getStyle(): string;
        setStyle(value: string): ElementSelectorWithDuration;
        getColor(): string;
        setColor(value: string): ElementSelectorWithDuration;
        getStrict(): boolean;
        setStrict(value: boolean): ElementSelectorWithDuration;
        getMode(): string;
        setMode(value: string): ElementSelectorWithDuration;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ElementSelectorWithDuration.AsObject;
        static toObject(includeInstance: boolean, msg: ElementSelectorWithDuration): ElementSelectorWithDuration.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ElementSelectorWithDuration, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ElementSelectorWithDuration;
        static deserializeBinaryFromReader(message: ElementSelectorWithDuration, reader: jspb.BinaryReader): ElementSelectorWithDuration;
    }

    export namespace ElementSelectorWithDuration {
        export type AsObject = {
            selector: string,
            duration: number,
            width: string,
            style: string,
            color: string,
            strict: boolean,
            mode: string,
        }
    }

    export class SelectElementSelector extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): SelectElementSelector;
        getMatcherjson(): string;
        setMatcherjson(value: string): SelectElementSelector;
        getStrict(): boolean;
        setStrict(value: boolean): SelectElementSelector;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): SelectElementSelector.AsObject;
        static toObject(includeInstance: boolean, msg: SelectElementSelector): SelectElementSelector.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: SelectElementSelector, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): SelectElementSelector;
        static deserializeBinaryFromReader(message: SelectElementSelector, reader: jspb.BinaryReader): SelectElementSelector;
    }

    export namespace SelectElementSelector {
        export type AsObject = {
            selector: string,
            matcherjson: string,
            strict: boolean,
        }
    }

    export class WaitForFunctionOptions extends jspb.Message { 
        getScript(): string;
        setScript(value: string): WaitForFunctionOptions;
        getSelector(): string;
        setSelector(value: string): WaitForFunctionOptions;
        getOptions(): string;
        setOptions(value: string): WaitForFunctionOptions;
        getStrict(): boolean;
        setStrict(value: boolean): WaitForFunctionOptions;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): WaitForFunctionOptions.AsObject;
        static toObject(includeInstance: boolean, msg: WaitForFunctionOptions): WaitForFunctionOptions.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: WaitForFunctionOptions, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): WaitForFunctionOptions;
        static deserializeBinaryFromReader(message: WaitForFunctionOptions, reader: jspb.BinaryReader): WaitForFunctionOptions;
    }

    export namespace WaitForFunctionOptions {
        export type AsObject = {
            script: string,
            selector: string,
            options: string,
            strict: boolean,
        }
    }

    export class PlaywrightObject extends jspb.Message { 
        getInfo(): string;
        setInfo(value: string): PlaywrightObject;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): PlaywrightObject.AsObject;
        static toObject(includeInstance: boolean, msg: PlaywrightObject): PlaywrightObject.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: PlaywrightObject, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): PlaywrightObject;
        static deserializeBinaryFromReader(message: PlaywrightObject, reader: jspb.BinaryReader): PlaywrightObject;
    }

    export namespace PlaywrightObject {
        export type AsObject = {
            info: string,
        }
    }

    export class Viewport extends jspb.Message { 
        getWidth(): number;
        setWidth(value: number): Viewport;
        getHeight(): number;
        setHeight(value: number): Viewport;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Viewport.AsObject;
        static toObject(includeInstance: boolean, msg: Viewport): Viewport.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Viewport, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Viewport;
        static deserializeBinaryFromReader(message: Viewport, reader: jspb.BinaryReader): Viewport;
    }

    export namespace Viewport {
        export type AsObject = {
            width: number,
            height: number,
        }
    }

    export class HttpRequest extends jspb.Message { 
        getUrl(): string;
        setUrl(value: string): HttpRequest;
        getMethod(): string;
        setMethod(value: string): HttpRequest;
        getBody(): string;
        setBody(value: string): HttpRequest;
        getHeaders(): string;
        setHeaders(value: string): HttpRequest;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): HttpRequest.AsObject;
        static toObject(includeInstance: boolean, msg: HttpRequest): HttpRequest.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: HttpRequest, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): HttpRequest;
        static deserializeBinaryFromReader(message: HttpRequest, reader: jspb.BinaryReader): HttpRequest;
    }

    export namespace HttpRequest {
        export type AsObject = {
            url: string,
            method: string,
            body: string,
            headers: string,
        }
    }

    export class HttpCapture extends jspb.Message { 
        getUrlorpredicate(): string;
        setUrlorpredicate(value: string): HttpCapture;
        getTimeout(): number;
        setTimeout(value: number): HttpCapture;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): HttpCapture.AsObject;
        static toObject(includeInstance: boolean, msg: HttpCapture): HttpCapture.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: HttpCapture, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): HttpCapture;
        static deserializeBinaryFromReader(message: HttpCapture, reader: jspb.BinaryReader): HttpCapture;
    }

    export namespace HttpCapture {
        export type AsObject = {
            urlorpredicate: string,
            timeout: number,
        }
    }

    export class Device extends jspb.Message { 
        getName(): string;
        setName(value: string): Device;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Device.AsObject;
        static toObject(includeInstance: boolean, msg: Device): Device.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Device, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Device;
        static deserializeBinaryFromReader(message: Device, reader: jspb.BinaryReader): Device;
    }

    export namespace Device {
        export type AsObject = {
            name: string,
        }
    }

    export class AlertAction extends jspb.Message { 
        getAlertaction(): string;
        setAlertaction(value: string): AlertAction;
        getPromptinput(): string;
        setPromptinput(value: string): AlertAction;
        getTimeout(): number;
        setTimeout(value: number): AlertAction;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): AlertAction.AsObject;
        static toObject(includeInstance: boolean, msg: AlertAction): AlertAction.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: AlertAction, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): AlertAction;
        static deserializeBinaryFromReader(message: AlertAction, reader: jspb.BinaryReader): AlertAction;
    }

    export namespace AlertAction {
        export type AsObject = {
            alertaction: string,
            promptinput: string,
            timeout: number,
        }
    }

    export class AlertActions extends jspb.Message { 
        clearItemsList(): void;
        getItemsList(): Array<Request.AlertAction>;
        setItemsList(value: Array<Request.AlertAction>): AlertActions;
        addItems(value?: Request.AlertAction, index?: number): Request.AlertAction;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): AlertActions.AsObject;
        static toObject(includeInstance: boolean, msg: AlertActions): AlertActions.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: AlertActions, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): AlertActions;
        static deserializeBinaryFromReader(message: AlertActions, reader: jspb.BinaryReader): AlertActions;
    }

    export namespace AlertActions {
        export type AsObject = {
            itemsList: Array<Request.AlertAction.AsObject>,
        }
    }

    export class Bool extends jspb.Message { 
        getValue(): boolean;
        setValue(value: boolean): Bool;

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
            value: boolean,
        }
    }

    export class EvaluateAll extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): EvaluateAll;
        getScript(): string;
        setScript(value: string): EvaluateAll;
        getArg(): string;
        setArg(value: string): EvaluateAll;
        getAllelements(): boolean;
        setAllelements(value: boolean): EvaluateAll;
        getStrict(): boolean;
        setStrict(value: boolean): EvaluateAll;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): EvaluateAll.AsObject;
        static toObject(includeInstance: boolean, msg: EvaluateAll): EvaluateAll.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: EvaluateAll, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): EvaluateAll;
        static deserializeBinaryFromReader(message: EvaluateAll, reader: jspb.BinaryReader): EvaluateAll;
    }

    export namespace EvaluateAll {
        export type AsObject = {
            selector: string,
            script: string,
            arg: string,
            allelements: boolean,
            strict: boolean,
        }
    }

    export class ElementStyle extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): ElementStyle;
        getPseudo(): string;
        setPseudo(value: string): ElementStyle;
        getStylekey(): string;
        setStylekey(value: string): ElementStyle;
        getStrict(): boolean;
        setStrict(value: boolean): ElementStyle;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ElementStyle.AsObject;
        static toObject(includeInstance: boolean, msg: ElementStyle): ElementStyle.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ElementStyle, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ElementStyle;
        static deserializeBinaryFromReader(message: ElementStyle, reader: jspb.BinaryReader): ElementStyle;
    }

    export namespace ElementStyle {
        export type AsObject = {
            selector: string,
            pseudo: string,
            stylekey: string,
            strict: boolean,
        }
    }

}

export class Types extends jspb.Message { 

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): Types.AsObject;
    static toObject(includeInstance: boolean, msg: Types): Types.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: Types, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): Types;
    static deserializeBinaryFromReader(message: Types, reader: jspb.BinaryReader): Types;
}

export namespace Types {
    export type AsObject = {
    }


    export class SelectEntry extends jspb.Message { 
        getValue(): string;
        setValue(value: string): SelectEntry;
        getLabel(): string;
        setLabel(value: string): SelectEntry;
        getIndex(): number;
        setIndex(value: number): SelectEntry;
        getSelected(): boolean;
        setSelected(value: boolean): SelectEntry;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): SelectEntry.AsObject;
        static toObject(includeInstance: boolean, msg: SelectEntry): SelectEntry.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: SelectEntry, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): SelectEntry;
        static deserializeBinaryFromReader(message: SelectEntry, reader: jspb.BinaryReader): SelectEntry;
    }

    export namespace SelectEntry {
        export type AsObject = {
            value: string,
            label: string,
            index: number,
            selected: boolean,
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

    export class ListString extends jspb.Message { 
        clearItemsList(): void;
        getItemsList(): Array<string>;
        setItemsList(value: Array<string>): ListString;
        addItems(value: string, index?: number): string;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): ListString.AsObject;
        static toObject(includeInstance: boolean, msg: ListString): ListString.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: ListString, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): ListString;
        static deserializeBinaryFromReader(message: ListString, reader: jspb.BinaryReader): ListString;
    }

    export namespace ListString {
        export type AsObject = {
            itemsList: Array<string>,
        }
    }

    export class Keywords extends jspb.Message { 
        getLog(): string;
        setLog(value: string): Keywords;
        clearKeywordsList(): void;
        getKeywordsList(): Array<string>;
        setKeywordsList(value: Array<string>): Keywords;
        addKeywords(value: string, index?: number): string;
        clearKeyworddocumentationsList(): void;
        getKeyworddocumentationsList(): Array<string>;
        setKeyworddocumentationsList(value: Array<string>): Keywords;
        addKeyworddocumentations(value: string, index?: number): string;
        clearKeywordargumentsList(): void;
        getKeywordargumentsList(): Array<string>;
        setKeywordargumentsList(value: Array<string>): Keywords;
        addKeywordarguments(value: string, index?: number): string;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Keywords.AsObject;
        static toObject(includeInstance: boolean, msg: Keywords): Keywords.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Keywords, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Keywords;
        static deserializeBinaryFromReader(message: Keywords, reader: jspb.BinaryReader): Keywords;
    }

    export namespace Keywords {
        export type AsObject = {
            log: string,
            keywordsList: Array<string>,
            keyworddocumentationsList: Array<string>,
            keywordargumentsList: Array<string>,
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

    export class Int extends jspb.Message { 
        getLog(): string;
        setLog(value: string): Int;
        getBody(): number;
        setBody(value: number): Int;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Int.AsObject;
        static toObject(includeInstance: boolean, msg: Int): Int.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Int, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Int;
        static deserializeBinaryFromReader(message: Int, reader: jspb.BinaryReader): Int;
    }

    export namespace Int {
        export type AsObject = {
            log: string,
            body: number,
        }
    }

    export class Select extends jspb.Message { 
        clearEntryList(): void;
        getEntryList(): Array<Types.SelectEntry>;
        setEntryList(value: Array<Types.SelectEntry>): Select;
        addEntry(value?: Types.SelectEntry, index?: number): Types.SelectEntry;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Select.AsObject;
        static toObject(includeInstance: boolean, msg: Select): Select.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Select, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Select;
        static deserializeBinaryFromReader(message: Select, reader: jspb.BinaryReader): Select;
    }

    export namespace Select {
        export type AsObject = {
            entryList: Array<Types.SelectEntry.AsObject>,
        }
    }

    export class Json extends jspb.Message { 
        getLog(): string;
        setLog(value: string): Json;
        getJson(): string;
        setJson(value: string): Json;
        getBodypart(): string;
        setBodypart(value: string): Json;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Json.AsObject;
        static toObject(includeInstance: boolean, msg: Json): Json.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Json, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Json;
        static deserializeBinaryFromReader(message: Json, reader: jspb.BinaryReader): Json;
    }

    export namespace Json {
        export type AsObject = {
            log: string,
            json: string,
            bodypart: string,
        }
    }

    export class JavascriptExecutionResult extends jspb.Message { 
        getLog(): string;
        setLog(value: string): JavascriptExecutionResult;
        getResult(): string;
        setResult(value: string): JavascriptExecutionResult;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): JavascriptExecutionResult.AsObject;
        static toObject(includeInstance: boolean, msg: JavascriptExecutionResult): JavascriptExecutionResult.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: JavascriptExecutionResult, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): JavascriptExecutionResult;
        static deserializeBinaryFromReader(message: JavascriptExecutionResult, reader: jspb.BinaryReader): JavascriptExecutionResult;
    }

    export namespace JavascriptExecutionResult {
        export type AsObject = {
            log: string,
            result: string,
        }
    }

    export class NewContextResponse extends jspb.Message { 
        getId(): string;
        setId(value: string): NewContextResponse;
        getLog(): string;
        setLog(value: string): NewContextResponse;
        getContextoptions(): string;
        setContextoptions(value: string): NewContextResponse;
        getNewbrowser(): boolean;
        setNewbrowser(value: boolean): NewContextResponse;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): NewContextResponse.AsObject;
        static toObject(includeInstance: boolean, msg: NewContextResponse): NewContextResponse.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: NewContextResponse, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): NewContextResponse;
        static deserializeBinaryFromReader(message: NewContextResponse, reader: jspb.BinaryReader): NewContextResponse;
    }

    export namespace NewContextResponse {
        export type AsObject = {
            id: string,
            log: string,
            contextoptions: string,
            newbrowser: boolean,
        }
    }

    export class NewPersistentContextResponse extends jspb.Message { 
        getId(): string;
        setId(value: string): NewPersistentContextResponse;
        getLog(): string;
        setLog(value: string): NewPersistentContextResponse;
        getContextoptions(): string;
        setContextoptions(value: string): NewPersistentContextResponse;
        getNewbrowser(): boolean;
        setNewbrowser(value: boolean): NewPersistentContextResponse;
        getVideo(): string;
        setVideo(value: string): NewPersistentContextResponse;
        getPageid(): string;
        setPageid(value: string): NewPersistentContextResponse;
        getBrowserid(): string;
        setBrowserid(value: string): NewPersistentContextResponse;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): NewPersistentContextResponse.AsObject;
        static toObject(includeInstance: boolean, msg: NewPersistentContextResponse): NewPersistentContextResponse.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: NewPersistentContextResponse, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): NewPersistentContextResponse;
        static deserializeBinaryFromReader(message: NewPersistentContextResponse, reader: jspb.BinaryReader): NewPersistentContextResponse;
    }

    export namespace NewPersistentContextResponse {
        export type AsObject = {
            id: string,
            log: string,
            contextoptions: string,
            newbrowser: boolean,
            video: string,
            pageid: string,
            browserid: string,
        }
    }

    export class NewPageResponse extends jspb.Message { 
        getLog(): string;
        setLog(value: string): NewPageResponse;
        getBody(): string;
        setBody(value: string): NewPageResponse;
        getVideo(): string;
        setVideo(value: string): NewPageResponse;
        getNewbrowser(): boolean;
        setNewbrowser(value: boolean): NewPageResponse;
        getNewcontext(): boolean;
        setNewcontext(value: boolean): NewPageResponse;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): NewPageResponse.AsObject;
        static toObject(includeInstance: boolean, msg: NewPageResponse): NewPageResponse.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: NewPageResponse, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): NewPageResponse;
        static deserializeBinaryFromReader(message: NewPageResponse, reader: jspb.BinaryReader): NewPageResponse;
    }

    export namespace NewPageResponse {
        export type AsObject = {
            log: string,
            body: string,
            video: string,
            newbrowser: boolean,
            newcontext: boolean,
        }
    }

    export class PageReportResponse extends jspb.Message { 
        getLog(): string;
        setLog(value: string): PageReportResponse;
        getErrors(): string;
        setErrors(value: string): PageReportResponse;
        getConsole(): string;
        setConsole(value: string): PageReportResponse;
        getPageid(): string;
        setPageid(value: string): PageReportResponse;

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): PageReportResponse.AsObject;
        static toObject(includeInstance: boolean, msg: PageReportResponse): PageReportResponse.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: PageReportResponse, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): PageReportResponse;
        static deserializeBinaryFromReader(message: PageReportResponse, reader: jspb.BinaryReader): PageReportResponse;
    }

    export namespace PageReportResponse {
        export type AsObject = {
            log: string,
            errors: string,
            console: string,
            pageid: string,
        }
    }

}
