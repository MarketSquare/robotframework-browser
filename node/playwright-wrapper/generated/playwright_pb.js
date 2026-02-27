// source: playwright.proto
/**
 * @fileoverview
 * @enhanceable
 * @suppress {missingRequire} reports error on implicit type usages.
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!
/* eslint-disable */
// @ts-nocheck

var jspb = require('google-protobuf');
var goog = jspb;
var global =
    (typeof globalThis !== 'undefined' && globalThis) ||
    (typeof window !== 'undefined' && window) ||
    (typeof global !== 'undefined' && global) ||
    (typeof self !== 'undefined' && self) ||
    (function () { return this; }).call(null) ||
    Function('return this')();

goog.exportSymbol('proto.Request', null, global);
goog.exportSymbol('proto.Request.AlertAction', null, global);
goog.exportSymbol('proto.Request.AlertActions', null, global);
goog.exportSymbol('proto.Request.AriaSnapShot', null, global);
goog.exportSymbol('proto.Request.Bool', null, global);
goog.exportSymbol('proto.Request.Browser', null, global);
goog.exportSymbol('proto.Request.ClearText', null, global);
goog.exportSymbol('proto.Request.ClockAdvance', null, global);
goog.exportSymbol('proto.Request.ClockSetTime', null, global);
goog.exportSymbol('proto.Request.ClosePage', null, global);
goog.exportSymbol('proto.Request.ConnectBrowser', null, global);
goog.exportSymbol('proto.Request.Context', null, global);
goog.exportSymbol('proto.Request.CoverageMerge', null, global);
goog.exportSymbol('proto.Request.CoverageStart', null, global);
goog.exportSymbol('proto.Request.Device', null, global);
goog.exportSymbol('proto.Request.DownloadID', null, global);
goog.exportSymbol('proto.Request.DownloadOptions', null, global);
goog.exportSymbol('proto.Request.ElectronLaunch', null, global);
goog.exportSymbol('proto.Request.ElementProperty', null, global);
goog.exportSymbol('proto.Request.ElementSelector', null, global);
goog.exportSymbol('proto.Request.ElementSelectorWithDuration', null, global);
goog.exportSymbol('proto.Request.ElementSelectorWithOptions', null, global);
goog.exportSymbol('proto.Request.ElementStyle', null, global);
goog.exportSymbol('proto.Request.Empty', null, global);
goog.exportSymbol('proto.Request.EmulateMedia', null, global);
goog.exportSymbol('proto.Request.EvaluateAll', null, global);
goog.exportSymbol('proto.Request.FileBySelector', null, global);
goog.exportSymbol('proto.Request.FilePath', null, global);
goog.exportSymbol('proto.Request.FillText', null, global);
goog.exportSymbol('proto.Request.GetByOptions', null, global);
goog.exportSymbol('proto.Request.HttpCapture', null, global);
goog.exportSymbol('proto.Request.HttpRequest', null, global);
goog.exportSymbol('proto.Request.IdWithTimeout', null, global);
goog.exportSymbol('proto.Request.Index', null, global);
goog.exportSymbol('proto.Request.Json', null, global);
goog.exportSymbol('proto.Request.KeyboardInputOptions', null, global);
goog.exportSymbol('proto.Request.KeyboardKeypress', null, global);
goog.exportSymbol('proto.Request.KeywordCall', null, global);
goog.exportSymbol('proto.Request.Label', null, global);
goog.exportSymbol('proto.Request.LocatorHandlerAddCustom', null, global);
goog.exportSymbol('proto.Request.LocatorHandlerAddCustomAction', null, global);
goog.exportSymbol('proto.Request.LocatorHandlerRemove', null, global);
goog.exportSymbol('proto.Request.MouseButtonOptions', null, global);
goog.exportSymbol('proto.Request.MouseWheel', null, global);
goog.exportSymbol('proto.Request.PageLoadState', null, global);
goog.exportSymbol('proto.Request.Pdf', null, global);
goog.exportSymbol('proto.Request.Permissions', null, global);
goog.exportSymbol('proto.Request.PersistentContext', null, global);
goog.exportSymbol('proto.Request.PlaywrightObject', null, global);
goog.exportSymbol('proto.Request.PressKeys', null, global);
goog.exportSymbol('proto.Request.ScreenshotOptions', null, global);
goog.exportSymbol('proto.Request.SelectElementSelector', null, global);
goog.exportSymbol('proto.Request.StyleTag', null, global);
goog.exportSymbol('proto.Request.TextInput', null, global);
goog.exportSymbol('proto.Request.Timeout', null, global);
goog.exportSymbol('proto.Request.TraceGroup', null, global);
goog.exportSymbol('proto.Request.TypeText', null, global);
goog.exportSymbol('proto.Request.Url', null, global);
goog.exportSymbol('proto.Request.UrlOptions', null, global);
goog.exportSymbol('proto.Request.Viewport', null, global);
goog.exportSymbol('proto.Request.WaitForFunctionOptions', null, global);
goog.exportSymbol('proto.Response', null, global);
goog.exportSymbol('proto.Response.Bool', null, global);
goog.exportSymbol('proto.Response.Empty', null, global);
goog.exportSymbol('proto.Response.Int', null, global);
goog.exportSymbol('proto.Response.JavascriptExecutionResult', null, global);
goog.exportSymbol('proto.Response.Json', null, global);
goog.exportSymbol('proto.Response.Keywords', null, global);
goog.exportSymbol('proto.Response.ListString', null, global);
goog.exportSymbol('proto.Response.NewContextResponse', null, global);
goog.exportSymbol('proto.Response.NewPageResponse', null, global);
goog.exportSymbol('proto.Response.NewPersistentContextResponse', null, global);
goog.exportSymbol('proto.Response.PageReportResponse', null, global);
goog.exportSymbol('proto.Response.Select', null, global);
goog.exportSymbol('proto.Response.String', null, global);
goog.exportSymbol('proto.Types', null, global);
goog.exportSymbol('proto.Types.SelectEntry', null, global);
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.displayName = 'proto.Request';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Empty = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.Empty, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Empty.displayName = 'proto.Request.Empty';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.AriaSnapShot = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.AriaSnapShot, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.AriaSnapShot.displayName = 'proto.Request.AriaSnapShot';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.ClosePage = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.ClosePage, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.ClosePage.displayName = 'proto.Request.ClosePage';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.ClockSetTime = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.ClockSetTime, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.ClockSetTime.displayName = 'proto.Request.ClockSetTime';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.ClockAdvance = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.ClockAdvance, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.ClockAdvance.displayName = 'proto.Request.ClockAdvance';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.CoverageStart = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.CoverageStart, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.CoverageStart.displayName = 'proto.Request.CoverageStart';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.CoverageMerge = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.CoverageMerge.repeatedFields_, null);
};
goog.inherits(proto.Request.CoverageMerge, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.CoverageMerge.displayName = 'proto.Request.CoverageMerge';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.TraceGroup = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.TraceGroup, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.TraceGroup.displayName = 'proto.Request.TraceGroup';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Label = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.Label, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Label.displayName = 'proto.Request.Label';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.GetByOptions = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.GetByOptions, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.GetByOptions.displayName = 'proto.Request.GetByOptions';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Pdf = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.Pdf, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Pdf.displayName = 'proto.Request.Pdf';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.EmulateMedia = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.EmulateMedia, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.EmulateMedia.displayName = 'proto.Request.EmulateMedia';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.ScreenshotOptions = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.ScreenshotOptions, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.ScreenshotOptions.displayName = 'proto.Request.ScreenshotOptions';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.KeywordCall = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.KeywordCall, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.KeywordCall.displayName = 'proto.Request.KeywordCall';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.FilePath = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.FilePath, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.FilePath.displayName = 'proto.Request.FilePath';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.FileBySelector = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.FileBySelector.repeatedFields_, null);
};
goog.inherits(proto.Request.FileBySelector, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.FileBySelector.displayName = 'proto.Request.FileBySelector';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.LocatorHandlerAddCustom = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.LocatorHandlerAddCustom.repeatedFields_, null);
};
goog.inherits(proto.Request.LocatorHandlerAddCustom, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.LocatorHandlerAddCustom.displayName = 'proto.Request.LocatorHandlerAddCustom';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.LocatorHandlerAddCustomAction = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.LocatorHandlerAddCustomAction, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.LocatorHandlerAddCustomAction.displayName = 'proto.Request.LocatorHandlerAddCustomAction';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.LocatorHandlerRemove = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.LocatorHandlerRemove, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.LocatorHandlerRemove.displayName = 'proto.Request.LocatorHandlerRemove';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Json = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.Json, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Json.displayName = 'proto.Request.Json';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.MouseButtonOptions = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.MouseButtonOptions, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.MouseButtonOptions.displayName = 'proto.Request.MouseButtonOptions';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.MouseWheel = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.MouseWheel, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.MouseWheel.displayName = 'proto.Request.MouseWheel';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.KeyboardKeypress = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.KeyboardKeypress, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.KeyboardKeypress.displayName = 'proto.Request.KeyboardKeypress';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.KeyboardInputOptions = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.KeyboardInputOptions, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.KeyboardInputOptions.displayName = 'proto.Request.KeyboardInputOptions';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Browser = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.Browser, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Browser.displayName = 'proto.Request.Browser';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Context = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.Context, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Context.displayName = 'proto.Request.Context';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.PersistentContext = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.PersistentContext, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.PersistentContext.displayName = 'proto.Request.PersistentContext';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.ElectronLaunch = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.ElectronLaunch.repeatedFields_, null);
};
goog.inherits(proto.Request.ElectronLaunch, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.ElectronLaunch.displayName = 'proto.Request.ElectronLaunch';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Permissions = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.Permissions.repeatedFields_, null);
};
goog.inherits(proto.Request.Permissions, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Permissions.displayName = 'proto.Request.Permissions';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Url = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.Url, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Url.displayName = 'proto.Request.Url';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.DownloadOptions = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.DownloadOptions, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.DownloadOptions.displayName = 'proto.Request.DownloadOptions';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.DownloadID = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.DownloadID, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.DownloadID.displayName = 'proto.Request.DownloadID';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.UrlOptions = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.UrlOptions, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.UrlOptions.displayName = 'proto.Request.UrlOptions';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.PageLoadState = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.PageLoadState, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.PageLoadState.displayName = 'proto.Request.PageLoadState';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.ConnectBrowser = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.ConnectBrowser, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.ConnectBrowser.displayName = 'proto.Request.ConnectBrowser';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.TextInput = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.TextInput, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.TextInput.displayName = 'proto.Request.TextInput';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.ElementProperty = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.ElementProperty, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.ElementProperty.displayName = 'proto.Request.ElementProperty';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.TypeText = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.TypeText, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.TypeText.displayName = 'proto.Request.TypeText';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.FillText = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.FillText, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.FillText.displayName = 'proto.Request.FillText';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.ClearText = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.ClearText, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.ClearText.displayName = 'proto.Request.ClearText';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.PressKeys = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.PressKeys.repeatedFields_, null);
};
goog.inherits(proto.Request.PressKeys, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.PressKeys.displayName = 'proto.Request.PressKeys';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.ElementSelector = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.ElementSelector, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.ElementSelector.displayName = 'proto.Request.ElementSelector';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Timeout = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.Timeout, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Timeout.displayName = 'proto.Request.Timeout';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Index = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.Index, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Index.displayName = 'proto.Request.Index';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.IdWithTimeout = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.IdWithTimeout, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.IdWithTimeout.displayName = 'proto.Request.IdWithTimeout';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.StyleTag = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.StyleTag, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.StyleTag.displayName = 'proto.Request.StyleTag';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.ElementSelectorWithOptions = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.ElementSelectorWithOptions, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.ElementSelectorWithOptions.displayName = 'proto.Request.ElementSelectorWithOptions';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.ElementSelectorWithDuration = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.ElementSelectorWithDuration, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.ElementSelectorWithDuration.displayName = 'proto.Request.ElementSelectorWithDuration';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.SelectElementSelector = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.SelectElementSelector, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.SelectElementSelector.displayName = 'proto.Request.SelectElementSelector';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.WaitForFunctionOptions = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.WaitForFunctionOptions, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.WaitForFunctionOptions.displayName = 'proto.Request.WaitForFunctionOptions';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.PlaywrightObject = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.PlaywrightObject, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.PlaywrightObject.displayName = 'proto.Request.PlaywrightObject';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Viewport = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.Viewport, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Viewport.displayName = 'proto.Request.Viewport';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.HttpRequest = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.HttpRequest, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.HttpRequest.displayName = 'proto.Request.HttpRequest';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.HttpCapture = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.HttpCapture, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.HttpCapture.displayName = 'proto.Request.HttpCapture';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Device = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.Device, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Device.displayName = 'proto.Request.Device';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.AlertAction = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.AlertAction, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.AlertAction.displayName = 'proto.Request.AlertAction';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.AlertActions = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.AlertActions.repeatedFields_, null);
};
goog.inherits(proto.Request.AlertActions, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.AlertActions.displayName = 'proto.Request.AlertActions';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.Bool = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.Bool, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.Bool.displayName = 'proto.Request.Bool';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.EvaluateAll = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.EvaluateAll, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.EvaluateAll.displayName = 'proto.Request.EvaluateAll';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Request.ElementStyle = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Request.ElementStyle, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Request.ElementStyle.displayName = 'proto.Request.ElementStyle';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Types = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Types, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Types.displayName = 'proto.Types';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Types.SelectEntry = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Types.SelectEntry, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Types.SelectEntry.displayName = 'proto.Types.SelectEntry';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Response, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.displayName = 'proto.Response';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.Empty = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Response.Empty, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.Empty.displayName = 'proto.Response.Empty';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.String = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Response.String, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.String.displayName = 'proto.Response.String';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.ListString = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.Response.ListString.repeatedFields_, null);
};
goog.inherits(proto.Response.ListString, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.ListString.displayName = 'proto.Response.ListString';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.Keywords = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.Response.Keywords.repeatedFields_, null);
};
goog.inherits(proto.Response.Keywords, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.Keywords.displayName = 'proto.Response.Keywords';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.Bool = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Response.Bool, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.Bool.displayName = 'proto.Response.Bool';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.Int = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Response.Int, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.Int.displayName = 'proto.Response.Int';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.Select = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.Response.Select.repeatedFields_, null);
};
goog.inherits(proto.Response.Select, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.Select.displayName = 'proto.Response.Select';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.Json = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Response.Json, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.Json.displayName = 'proto.Response.Json';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.JavascriptExecutionResult = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Response.JavascriptExecutionResult, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.JavascriptExecutionResult.displayName = 'proto.Response.JavascriptExecutionResult';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.NewContextResponse = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Response.NewContextResponse, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.NewContextResponse.displayName = 'proto.Response.NewContextResponse';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.NewPersistentContextResponse = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Response.NewPersistentContextResponse, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.NewPersistentContextResponse.displayName = 'proto.Response.NewPersistentContextResponse';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.NewPageResponse = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Response.NewPageResponse, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.NewPageResponse.displayName = 'proto.Response.NewPageResponse';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.Response.PageReportResponse = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.Response.PageReportResponse, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.Response.PageReportResponse.displayName = 'proto.Response.PageReportResponse';
}



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.toObject = function(includeInstance, msg) {
  var f, obj = {

  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request}
 */
proto.Request.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request;
  return proto.Request.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request}
 */
proto.Request.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Empty.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Empty.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Empty} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Empty.toObject = function(includeInstance, msg) {
  var f, obj = {

  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Empty}
 */
proto.Request.Empty.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Empty;
  return proto.Request.Empty.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Empty} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Empty}
 */
proto.Request.Empty.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Empty.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Empty.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Empty} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Empty.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.AriaSnapShot.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.AriaSnapShot.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.AriaSnapShot} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.AriaSnapShot.toObject = function(includeInstance, msg) {
  var f, obj = {
locator: jspb.Message.getFieldWithDefault(msg, 1, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 2, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.AriaSnapShot}
 */
proto.Request.AriaSnapShot.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.AriaSnapShot;
  return proto.Request.AriaSnapShot.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.AriaSnapShot} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.AriaSnapShot}
 */
proto.Request.AriaSnapShot.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setLocator(value);
      break;
    case 2:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.AriaSnapShot.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.AriaSnapShot.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.AriaSnapShot} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.AriaSnapShot.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getLocator();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      2,
      f
    );
  }
};


/**
 * optional string locator = 1;
 * @return {string}
 */
proto.Request.AriaSnapShot.prototype.getLocator = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.AriaSnapShot} returns this
 */
proto.Request.AriaSnapShot.prototype.setLocator = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional bool strict = 2;
 * @return {boolean}
 */
proto.Request.AriaSnapShot.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 2, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.AriaSnapShot} returns this
 */
proto.Request.AriaSnapShot.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.ClosePage.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.ClosePage.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.ClosePage} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ClosePage.toObject = function(includeInstance, msg) {
  var f, obj = {
runbeforeunload: jspb.Message.getBooleanFieldWithDefault(msg, 1, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.ClosePage}
 */
proto.Request.ClosePage.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.ClosePage;
  return proto.Request.ClosePage.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.ClosePage} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.ClosePage}
 */
proto.Request.ClosePage.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setRunbeforeunload(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.ClosePage.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.ClosePage.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.ClosePage} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ClosePage.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getRunbeforeunload();
  if (f) {
    writer.writeBool(
      1,
      f
    );
  }
};


/**
 * optional bool runBeforeUnload = 1;
 * @return {boolean}
 */
proto.Request.ClosePage.prototype.getRunbeforeunload = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 1, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.ClosePage} returns this
 */
proto.Request.ClosePage.prototype.setRunbeforeunload = function(value) {
  return jspb.Message.setProto3BooleanField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.ClockSetTime.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.ClockSetTime.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.ClockSetTime} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ClockSetTime.toObject = function(includeInstance, msg) {
  var f, obj = {
time: jspb.Message.getFieldWithDefault(msg, 1, 0),
settype: jspb.Message.getFieldWithDefault(msg, 2, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.ClockSetTime}
 */
proto.Request.ClockSetTime.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.ClockSetTime;
  return proto.Request.ClockSetTime.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.ClockSetTime} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.ClockSetTime}
 */
proto.Request.ClockSetTime.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setTime(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setSettype(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.ClockSetTime.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.ClockSetTime.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.ClockSetTime} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ClockSetTime.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getTime();
  if (f !== 0) {
    writer.writeInt32(
      1,
      f
    );
  }
  f = message.getSettype();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
};


/**
 * optional int32 time = 1;
 * @return {number}
 */
proto.Request.ClockSetTime.prototype.getTime = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 1, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.ClockSetTime} returns this
 */
proto.Request.ClockSetTime.prototype.setTime = function(value) {
  return jspb.Message.setProto3IntField(this, 1, value);
};


/**
 * optional string setType = 2;
 * @return {string}
 */
proto.Request.ClockSetTime.prototype.getSettype = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ClockSetTime} returns this
 */
proto.Request.ClockSetTime.prototype.setSettype = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.ClockAdvance.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.ClockAdvance.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.ClockAdvance} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ClockAdvance.toObject = function(includeInstance, msg) {
  var f, obj = {
time: jspb.Message.getFieldWithDefault(msg, 1, 0),
advancetype: jspb.Message.getFieldWithDefault(msg, 2, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.ClockAdvance}
 */
proto.Request.ClockAdvance.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.ClockAdvance;
  return proto.Request.ClockAdvance.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.ClockAdvance} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.ClockAdvance}
 */
proto.Request.ClockAdvance.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setTime(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setAdvancetype(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.ClockAdvance.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.ClockAdvance.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.ClockAdvance} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ClockAdvance.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getTime();
  if (f !== 0) {
    writer.writeInt32(
      1,
      f
    );
  }
  f = message.getAdvancetype();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
};


/**
 * optional int32 time = 1;
 * @return {number}
 */
proto.Request.ClockAdvance.prototype.getTime = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 1, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.ClockAdvance} returns this
 */
proto.Request.ClockAdvance.prototype.setTime = function(value) {
  return jspb.Message.setProto3IntField(this, 1, value);
};


/**
 * optional string advanceType = 2;
 * @return {string}
 */
proto.Request.ClockAdvance.prototype.getAdvancetype = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ClockAdvance} returns this
 */
proto.Request.ClockAdvance.prototype.setAdvancetype = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.CoverageStart.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.CoverageStart.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.CoverageStart} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.CoverageStart.toObject = function(includeInstance, msg) {
  var f, obj = {
coveragetype: jspb.Message.getFieldWithDefault(msg, 1, ""),
resetonnavigation: jspb.Message.getBooleanFieldWithDefault(msg, 2, false),
reportanonymousscripts: jspb.Message.getBooleanFieldWithDefault(msg, 3, false),
configfile: jspb.Message.getFieldWithDefault(msg, 4, ""),
coveragedir: jspb.Message.getFieldWithDefault(msg, 5, ""),
raw: jspb.Message.getBooleanFieldWithDefault(msg, 6, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.CoverageStart}
 */
proto.Request.CoverageStart.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.CoverageStart;
  return proto.Request.CoverageStart.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.CoverageStart} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.CoverageStart}
 */
proto.Request.CoverageStart.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setCoveragetype(value);
      break;
    case 2:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setResetonnavigation(value);
      break;
    case 3:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setReportanonymousscripts(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setConfigfile(value);
      break;
    case 5:
      var value = /** @type {string} */ (reader.readString());
      msg.setCoveragedir(value);
      break;
    case 6:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setRaw(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.CoverageStart.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.CoverageStart.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.CoverageStart} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.CoverageStart.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getCoveragetype();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getResetonnavigation();
  if (f) {
    writer.writeBool(
      2,
      f
    );
  }
  f = message.getReportanonymousscripts();
  if (f) {
    writer.writeBool(
      3,
      f
    );
  }
  f = message.getConfigfile();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
  f = message.getCoveragedir();
  if (f.length > 0) {
    writer.writeString(
      5,
      f
    );
  }
  f = message.getRaw();
  if (f) {
    writer.writeBool(
      6,
      f
    );
  }
};


/**
 * optional string coverageType = 1;
 * @return {string}
 */
proto.Request.CoverageStart.prototype.getCoveragetype = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.CoverageStart} returns this
 */
proto.Request.CoverageStart.prototype.setCoveragetype = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional bool resetOnNavigation = 2;
 * @return {boolean}
 */
proto.Request.CoverageStart.prototype.getResetonnavigation = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 2, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.CoverageStart} returns this
 */
proto.Request.CoverageStart.prototype.setResetonnavigation = function(value) {
  return jspb.Message.setProto3BooleanField(this, 2, value);
};


/**
 * optional bool reportAnonymousScripts = 3;
 * @return {boolean}
 */
proto.Request.CoverageStart.prototype.getReportanonymousscripts = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 3, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.CoverageStart} returns this
 */
proto.Request.CoverageStart.prototype.setReportanonymousscripts = function(value) {
  return jspb.Message.setProto3BooleanField(this, 3, value);
};


/**
 * optional string configFile = 4;
 * @return {string}
 */
proto.Request.CoverageStart.prototype.getConfigfile = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.CoverageStart} returns this
 */
proto.Request.CoverageStart.prototype.setConfigfile = function(value) {
  return jspb.Message.setProto3StringField(this, 4, value);
};


/**
 * optional string coverageDir = 5;
 * @return {string}
 */
proto.Request.CoverageStart.prototype.getCoveragedir = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 5, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.CoverageStart} returns this
 */
proto.Request.CoverageStart.prototype.setCoveragedir = function(value) {
  return jspb.Message.setProto3StringField(this, 5, value);
};


/**
 * optional bool raw = 6;
 * @return {boolean}
 */
proto.Request.CoverageStart.prototype.getRaw = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 6, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.CoverageStart} returns this
 */
proto.Request.CoverageStart.prototype.setRaw = function(value) {
  return jspb.Message.setProto3BooleanField(this, 6, value);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.Request.CoverageMerge.repeatedFields_ = [5];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.CoverageMerge.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.CoverageMerge.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.CoverageMerge} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.CoverageMerge.toObject = function(includeInstance, msg) {
  var f, obj = {
inputFolder: jspb.Message.getFieldWithDefault(msg, 1, ""),
outputFolder: jspb.Message.getFieldWithDefault(msg, 2, ""),
config: jspb.Message.getFieldWithDefault(msg, 3, ""),
name: jspb.Message.getFieldWithDefault(msg, 4, ""),
reportsList: (f = jspb.Message.getRepeatedField(msg, 5)) == null ? undefined : f
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.CoverageMerge}
 */
proto.Request.CoverageMerge.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.CoverageMerge;
  return proto.Request.CoverageMerge.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.CoverageMerge} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.CoverageMerge}
 */
proto.Request.CoverageMerge.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setInputFolder(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setOutputFolder(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setConfig(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setName(value);
      break;
    case 5:
      var value = /** @type {string} */ (reader.readString());
      msg.addReports(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.CoverageMerge.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.CoverageMerge.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.CoverageMerge} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.CoverageMerge.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getInputFolder();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getOutputFolder();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getConfig();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getName();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
  f = message.getReportsList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      5,
      f
    );
  }
};


/**
 * optional string input_folder = 1;
 * @return {string}
 */
proto.Request.CoverageMerge.prototype.getInputFolder = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.CoverageMerge} returns this
 */
proto.Request.CoverageMerge.prototype.setInputFolder = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string output_folder = 2;
 * @return {string}
 */
proto.Request.CoverageMerge.prototype.getOutputFolder = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.CoverageMerge} returns this
 */
proto.Request.CoverageMerge.prototype.setOutputFolder = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string config = 3;
 * @return {string}
 */
proto.Request.CoverageMerge.prototype.getConfig = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.CoverageMerge} returns this
 */
proto.Request.CoverageMerge.prototype.setConfig = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional string name = 4;
 * @return {string}
 */
proto.Request.CoverageMerge.prototype.getName = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.CoverageMerge} returns this
 */
proto.Request.CoverageMerge.prototype.setName = function(value) {
  return jspb.Message.setProto3StringField(this, 4, value);
};


/**
 * repeated string reports = 5;
 * @return {!Array<string>}
 */
proto.Request.CoverageMerge.prototype.getReportsList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 5));
};


/**
 * @param {!Array<string>} value
 * @return {!proto.Request.CoverageMerge} returns this
 */
proto.Request.CoverageMerge.prototype.setReportsList = function(value) {
  return jspb.Message.setField(this, 5, value || []);
};


/**
 * @param {string} value
 * @param {number=} opt_index
 * @return {!proto.Request.CoverageMerge} returns this
 */
proto.Request.CoverageMerge.prototype.addReports = function(value, opt_index) {
  return jspb.Message.addToRepeatedField(this, 5, value, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.Request.CoverageMerge} returns this
 */
proto.Request.CoverageMerge.prototype.clearReportsList = function() {
  return this.setReportsList([]);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.TraceGroup.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.TraceGroup.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.TraceGroup} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.TraceGroup.toObject = function(includeInstance, msg) {
  var f, obj = {
name: jspb.Message.getFieldWithDefault(msg, 1, ""),
file: jspb.Message.getFieldWithDefault(msg, 2, ""),
line: jspb.Message.getFieldWithDefault(msg, 3, 0),
column: jspb.Message.getFieldWithDefault(msg, 4, 0),
contextid: jspb.Message.getFieldWithDefault(msg, 5, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.TraceGroup}
 */
proto.Request.TraceGroup.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.TraceGroup;
  return proto.Request.TraceGroup.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.TraceGroup} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.TraceGroup}
 */
proto.Request.TraceGroup.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setName(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setFile(value);
      break;
    case 3:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setLine(value);
      break;
    case 4:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setColumn(value);
      break;
    case 5:
      var value = /** @type {string} */ (reader.readString());
      msg.setContextid(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.TraceGroup.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.TraceGroup.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.TraceGroup} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.TraceGroup.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getName();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getFile();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getLine();
  if (f !== 0) {
    writer.writeInt32(
      3,
      f
    );
  }
  f = message.getColumn();
  if (f !== 0) {
    writer.writeInt32(
      4,
      f
    );
  }
  f = message.getContextid();
  if (f.length > 0) {
    writer.writeString(
      5,
      f
    );
  }
};


/**
 * optional string name = 1;
 * @return {string}
 */
proto.Request.TraceGroup.prototype.getName = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.TraceGroup} returns this
 */
proto.Request.TraceGroup.prototype.setName = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string file = 2;
 * @return {string}
 */
proto.Request.TraceGroup.prototype.getFile = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.TraceGroup} returns this
 */
proto.Request.TraceGroup.prototype.setFile = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional int32 line = 3;
 * @return {number}
 */
proto.Request.TraceGroup.prototype.getLine = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 3, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.TraceGroup} returns this
 */
proto.Request.TraceGroup.prototype.setLine = function(value) {
  return jspb.Message.setProto3IntField(this, 3, value);
};


/**
 * optional int32 column = 4;
 * @return {number}
 */
proto.Request.TraceGroup.prototype.getColumn = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 4, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.TraceGroup} returns this
 */
proto.Request.TraceGroup.prototype.setColumn = function(value) {
  return jspb.Message.setProto3IntField(this, 4, value);
};


/**
 * optional string contextId = 5;
 * @return {string}
 */
proto.Request.TraceGroup.prototype.getContextid = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 5, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.TraceGroup} returns this
 */
proto.Request.TraceGroup.prototype.setContextid = function(value) {
  return jspb.Message.setProto3StringField(this, 5, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Label.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Label.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Label} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Label.toObject = function(includeInstance, msg) {
  var f, obj = {
label: jspb.Message.getFieldWithDefault(msg, 1, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Label}
 */
proto.Request.Label.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Label;
  return proto.Request.Label.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Label} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Label}
 */
proto.Request.Label.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setLabel(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Label.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Label.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Label} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Label.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getLabel();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
};


/**
 * optional string label = 1;
 * @return {string}
 */
proto.Request.Label.prototype.getLabel = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Label} returns this
 */
proto.Request.Label.prototype.setLabel = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.GetByOptions.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.GetByOptions.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.GetByOptions} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.GetByOptions.toObject = function(includeInstance, msg) {
  var f, obj = {
strategy: jspb.Message.getFieldWithDefault(msg, 1, ""),
text: jspb.Message.getFieldWithDefault(msg, 2, ""),
options: jspb.Message.getFieldWithDefault(msg, 3, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 4, false),
all: jspb.Message.getBooleanFieldWithDefault(msg, 5, false),
frameselector: jspb.Message.getFieldWithDefault(msg, 6, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.GetByOptions}
 */
proto.Request.GetByOptions.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.GetByOptions;
  return proto.Request.GetByOptions.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.GetByOptions} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.GetByOptions}
 */
proto.Request.GetByOptions.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setStrategy(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setText(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setOptions(value);
      break;
    case 4:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    case 5:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setAll(value);
      break;
    case 6:
      var value = /** @type {string} */ (reader.readString());
      msg.setFrameselector(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.GetByOptions.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.GetByOptions.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.GetByOptions} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.GetByOptions.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getStrategy();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getText();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getOptions();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      4,
      f
    );
  }
  f = message.getAll();
  if (f) {
    writer.writeBool(
      5,
      f
    );
  }
  f = message.getFrameselector();
  if (f.length > 0) {
    writer.writeString(
      6,
      f
    );
  }
};


/**
 * optional string strategy = 1;
 * @return {string}
 */
proto.Request.GetByOptions.prototype.getStrategy = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.GetByOptions} returns this
 */
proto.Request.GetByOptions.prototype.setStrategy = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string text = 2;
 * @return {string}
 */
proto.Request.GetByOptions.prototype.getText = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.GetByOptions} returns this
 */
proto.Request.GetByOptions.prototype.setText = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string options = 3;
 * @return {string}
 */
proto.Request.GetByOptions.prototype.getOptions = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.GetByOptions} returns this
 */
proto.Request.GetByOptions.prototype.setOptions = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional bool strict = 4;
 * @return {boolean}
 */
proto.Request.GetByOptions.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 4, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.GetByOptions} returns this
 */
proto.Request.GetByOptions.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 4, value);
};


/**
 * optional bool all = 5;
 * @return {boolean}
 */
proto.Request.GetByOptions.prototype.getAll = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 5, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.GetByOptions} returns this
 */
proto.Request.GetByOptions.prototype.setAll = function(value) {
  return jspb.Message.setProto3BooleanField(this, 5, value);
};


/**
 * optional string frameSelector = 6;
 * @return {string}
 */
proto.Request.GetByOptions.prototype.getFrameselector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 6, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.GetByOptions} returns this
 */
proto.Request.GetByOptions.prototype.setFrameselector = function(value) {
  return jspb.Message.setProto3StringField(this, 6, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Pdf.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Pdf.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Pdf} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Pdf.toObject = function(includeInstance, msg) {
  var f, obj = {
displayheaderfooter: jspb.Message.getBooleanFieldWithDefault(msg, 1, false),
footertemplate: jspb.Message.getFieldWithDefault(msg, 2, ""),
format: jspb.Message.getFieldWithDefault(msg, 3, ""),
headertemplate: jspb.Message.getFieldWithDefault(msg, 4, ""),
height: jspb.Message.getFieldWithDefault(msg, 5, ""),
landscape: jspb.Message.getBooleanFieldWithDefault(msg, 6, false),
margin: jspb.Message.getFieldWithDefault(msg, 7, ""),
outline: jspb.Message.getBooleanFieldWithDefault(msg, 8, false),
pageranges: jspb.Message.getFieldWithDefault(msg, 9, ""),
path: jspb.Message.getFieldWithDefault(msg, 10, ""),
prefercsspagesize: jspb.Message.getBooleanFieldWithDefault(msg, 11, false),
printbackground: jspb.Message.getBooleanFieldWithDefault(msg, 12, false),
scale: jspb.Message.getFloatingPointFieldWithDefault(msg, 13, 0.0),
tagged: jspb.Message.getBooleanFieldWithDefault(msg, 14, false),
width: jspb.Message.getFieldWithDefault(msg, 15, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Pdf}
 */
proto.Request.Pdf.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Pdf;
  return proto.Request.Pdf.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Pdf} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Pdf}
 */
proto.Request.Pdf.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setDisplayheaderfooter(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setFootertemplate(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setFormat(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setHeadertemplate(value);
      break;
    case 5:
      var value = /** @type {string} */ (reader.readString());
      msg.setHeight(value);
      break;
    case 6:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setLandscape(value);
      break;
    case 7:
      var value = /** @type {string} */ (reader.readString());
      msg.setMargin(value);
      break;
    case 8:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setOutline(value);
      break;
    case 9:
      var value = /** @type {string} */ (reader.readString());
      msg.setPageranges(value);
      break;
    case 10:
      var value = /** @type {string} */ (reader.readString());
      msg.setPath(value);
      break;
    case 11:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setPrefercsspagesize(value);
      break;
    case 12:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setPrintbackground(value);
      break;
    case 13:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setScale(value);
      break;
    case 14:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setTagged(value);
      break;
    case 15:
      var value = /** @type {string} */ (reader.readString());
      msg.setWidth(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Pdf.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Pdf.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Pdf} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Pdf.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getDisplayheaderfooter();
  if (f) {
    writer.writeBool(
      1,
      f
    );
  }
  f = message.getFootertemplate();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getFormat();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getHeadertemplate();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
  f = message.getHeight();
  if (f.length > 0) {
    writer.writeString(
      5,
      f
    );
  }
  f = message.getLandscape();
  if (f) {
    writer.writeBool(
      6,
      f
    );
  }
  f = message.getMargin();
  if (f.length > 0) {
    writer.writeString(
      7,
      f
    );
  }
  f = message.getOutline();
  if (f) {
    writer.writeBool(
      8,
      f
    );
  }
  f = message.getPageranges();
  if (f.length > 0) {
    writer.writeString(
      9,
      f
    );
  }
  f = message.getPath();
  if (f.length > 0) {
    writer.writeString(
      10,
      f
    );
  }
  f = message.getPrefercsspagesize();
  if (f) {
    writer.writeBool(
      11,
      f
    );
  }
  f = message.getPrintbackground();
  if (f) {
    writer.writeBool(
      12,
      f
    );
  }
  f = message.getScale();
  if (f !== 0.0) {
    writer.writeFloat(
      13,
      f
    );
  }
  f = message.getTagged();
  if (f) {
    writer.writeBool(
      14,
      f
    );
  }
  f = message.getWidth();
  if (f.length > 0) {
    writer.writeString(
      15,
      f
    );
  }
};


/**
 * optional bool displayHeaderFooter = 1;
 * @return {boolean}
 */
proto.Request.Pdf.prototype.getDisplayheaderfooter = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 1, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setDisplayheaderfooter = function(value) {
  return jspb.Message.setProto3BooleanField(this, 1, value);
};


/**
 * optional string footerTemplate = 2;
 * @return {string}
 */
proto.Request.Pdf.prototype.getFootertemplate = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setFootertemplate = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string format = 3;
 * @return {string}
 */
proto.Request.Pdf.prototype.getFormat = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setFormat = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional string headerTemplate = 4;
 * @return {string}
 */
proto.Request.Pdf.prototype.getHeadertemplate = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setHeadertemplate = function(value) {
  return jspb.Message.setProto3StringField(this, 4, value);
};


/**
 * optional string height = 5;
 * @return {string}
 */
proto.Request.Pdf.prototype.getHeight = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 5, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setHeight = function(value) {
  return jspb.Message.setProto3StringField(this, 5, value);
};


/**
 * optional bool landscape = 6;
 * @return {boolean}
 */
proto.Request.Pdf.prototype.getLandscape = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 6, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setLandscape = function(value) {
  return jspb.Message.setProto3BooleanField(this, 6, value);
};


/**
 * optional string margin = 7;
 * @return {string}
 */
proto.Request.Pdf.prototype.getMargin = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 7, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setMargin = function(value) {
  return jspb.Message.setProto3StringField(this, 7, value);
};


/**
 * optional bool outline = 8;
 * @return {boolean}
 */
proto.Request.Pdf.prototype.getOutline = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 8, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setOutline = function(value) {
  return jspb.Message.setProto3BooleanField(this, 8, value);
};


/**
 * optional string pageRanges = 9;
 * @return {string}
 */
proto.Request.Pdf.prototype.getPageranges = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 9, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setPageranges = function(value) {
  return jspb.Message.setProto3StringField(this, 9, value);
};


/**
 * optional string path = 10;
 * @return {string}
 */
proto.Request.Pdf.prototype.getPath = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 10, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setPath = function(value) {
  return jspb.Message.setProto3StringField(this, 10, value);
};


/**
 * optional bool preferCSSPageSize = 11;
 * @return {boolean}
 */
proto.Request.Pdf.prototype.getPrefercsspagesize = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 11, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setPrefercsspagesize = function(value) {
  return jspb.Message.setProto3BooleanField(this, 11, value);
};


/**
 * optional bool printBackground = 12;
 * @return {boolean}
 */
proto.Request.Pdf.prototype.getPrintbackground = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 12, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setPrintbackground = function(value) {
  return jspb.Message.setProto3BooleanField(this, 12, value);
};


/**
 * optional float scale = 13;
 * @return {number}
 */
proto.Request.Pdf.prototype.getScale = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 13, 0.0));
};


/**
 * @param {number} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setScale = function(value) {
  return jspb.Message.setProto3FloatField(this, 13, value);
};


/**
 * optional bool tagged = 14;
 * @return {boolean}
 */
proto.Request.Pdf.prototype.getTagged = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 14, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setTagged = function(value) {
  return jspb.Message.setProto3BooleanField(this, 14, value);
};


/**
 * optional string width = 15;
 * @return {string}
 */
proto.Request.Pdf.prototype.getWidth = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 15, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Pdf} returns this
 */
proto.Request.Pdf.prototype.setWidth = function(value) {
  return jspb.Message.setProto3StringField(this, 15, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.EmulateMedia.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.EmulateMedia.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.EmulateMedia} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.EmulateMedia.toObject = function(includeInstance, msg) {
  var f, obj = {
colorscheme: jspb.Message.getFieldWithDefault(msg, 1, ""),
forcedcolors: jspb.Message.getFieldWithDefault(msg, 2, ""),
media: jspb.Message.getFieldWithDefault(msg, 3, ""),
reducedmotion: jspb.Message.getFieldWithDefault(msg, 4, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.EmulateMedia}
 */
proto.Request.EmulateMedia.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.EmulateMedia;
  return proto.Request.EmulateMedia.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.EmulateMedia} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.EmulateMedia}
 */
proto.Request.EmulateMedia.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setColorscheme(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setForcedcolors(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setMedia(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setReducedmotion(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.EmulateMedia.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.EmulateMedia.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.EmulateMedia} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.EmulateMedia.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getColorscheme();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getForcedcolors();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getMedia();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getReducedmotion();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
};


/**
 * optional string colorScheme = 1;
 * @return {string}
 */
proto.Request.EmulateMedia.prototype.getColorscheme = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.EmulateMedia} returns this
 */
proto.Request.EmulateMedia.prototype.setColorscheme = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string forcedColors = 2;
 * @return {string}
 */
proto.Request.EmulateMedia.prototype.getForcedcolors = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.EmulateMedia} returns this
 */
proto.Request.EmulateMedia.prototype.setForcedcolors = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string media = 3;
 * @return {string}
 */
proto.Request.EmulateMedia.prototype.getMedia = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.EmulateMedia} returns this
 */
proto.Request.EmulateMedia.prototype.setMedia = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional string reducedMotion = 4;
 * @return {string}
 */
proto.Request.EmulateMedia.prototype.getReducedmotion = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.EmulateMedia} returns this
 */
proto.Request.EmulateMedia.prototype.setReducedmotion = function(value) {
  return jspb.Message.setProto3StringField(this, 4, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.ScreenshotOptions.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.ScreenshotOptions.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.ScreenshotOptions} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ScreenshotOptions.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
mask: jspb.Message.getFieldWithDefault(msg, 2, ""),
options: jspb.Message.getFieldWithDefault(msg, 3, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 4, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.ScreenshotOptions}
 */
proto.Request.ScreenshotOptions.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.ScreenshotOptions;
  return proto.Request.ScreenshotOptions.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.ScreenshotOptions} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.ScreenshotOptions}
 */
proto.Request.ScreenshotOptions.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setMask(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setOptions(value);
      break;
    case 4:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.ScreenshotOptions.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.ScreenshotOptions.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.ScreenshotOptions} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ScreenshotOptions.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getMask();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getOptions();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      4,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.ScreenshotOptions.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ScreenshotOptions} returns this
 */
proto.Request.ScreenshotOptions.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string mask = 2;
 * @return {string}
 */
proto.Request.ScreenshotOptions.prototype.getMask = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ScreenshotOptions} returns this
 */
proto.Request.ScreenshotOptions.prototype.setMask = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string options = 3;
 * @return {string}
 */
proto.Request.ScreenshotOptions.prototype.getOptions = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ScreenshotOptions} returns this
 */
proto.Request.ScreenshotOptions.prototype.setOptions = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional bool strict = 4;
 * @return {boolean}
 */
proto.Request.ScreenshotOptions.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 4, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.ScreenshotOptions} returns this
 */
proto.Request.ScreenshotOptions.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 4, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.KeywordCall.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.KeywordCall.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.KeywordCall} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.KeywordCall.toObject = function(includeInstance, msg) {
  var f, obj = {
name: jspb.Message.getFieldWithDefault(msg, 1, ""),
arguments: jspb.Message.getFieldWithDefault(msg, 2, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.KeywordCall}
 */
proto.Request.KeywordCall.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.KeywordCall;
  return proto.Request.KeywordCall.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.KeywordCall} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.KeywordCall}
 */
proto.Request.KeywordCall.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setName(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setArguments(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.KeywordCall.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.KeywordCall.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.KeywordCall} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.KeywordCall.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getName();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getArguments();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
};


/**
 * optional string name = 1;
 * @return {string}
 */
proto.Request.KeywordCall.prototype.getName = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.KeywordCall} returns this
 */
proto.Request.KeywordCall.prototype.setName = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string arguments = 2;
 * @return {string}
 */
proto.Request.KeywordCall.prototype.getArguments = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.KeywordCall} returns this
 */
proto.Request.KeywordCall.prototype.setArguments = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.FilePath.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.FilePath.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.FilePath} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.FilePath.toObject = function(includeInstance, msg) {
  var f, obj = {
path: jspb.Message.getFieldWithDefault(msg, 1, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.FilePath}
 */
proto.Request.FilePath.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.FilePath;
  return proto.Request.FilePath.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.FilePath} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.FilePath}
 */
proto.Request.FilePath.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setPath(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.FilePath.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.FilePath.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.FilePath} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.FilePath.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getPath();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
};


/**
 * optional string path = 1;
 * @return {string}
 */
proto.Request.FilePath.prototype.getPath = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.FilePath} returns this
 */
proto.Request.FilePath.prototype.setPath = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.Request.FileBySelector.repeatedFields_ = [1];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.FileBySelector.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.FileBySelector.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.FileBySelector} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.FileBySelector.toObject = function(includeInstance, msg) {
  var f, obj = {
pathList: (f = jspb.Message.getRepeatedField(msg, 1)) == null ? undefined : f,
selector: jspb.Message.getFieldWithDefault(msg, 2, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 3, false),
name: jspb.Message.getFieldWithDefault(msg, 4, ""),
mimetype: jspb.Message.getFieldWithDefault(msg, 5, ""),
buffer: jspb.Message.getFieldWithDefault(msg, 6, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.FileBySelector}
 */
proto.Request.FileBySelector.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.FileBySelector;
  return proto.Request.FileBySelector.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.FileBySelector} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.FileBySelector}
 */
proto.Request.FileBySelector.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.addPath(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 3:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setName(value);
      break;
    case 5:
      var value = /** @type {string} */ (reader.readString());
      msg.setMimetype(value);
      break;
    case 6:
      var value = /** @type {string} */ (reader.readString());
      msg.setBuffer(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.FileBySelector.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.FileBySelector.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.FileBySelector} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.FileBySelector.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getPathList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      1,
      f
    );
  }
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      3,
      f
    );
  }
  f = message.getName();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
  f = message.getMimetype();
  if (f.length > 0) {
    writer.writeString(
      5,
      f
    );
  }
  f = message.getBuffer();
  if (f.length > 0) {
    writer.writeString(
      6,
      f
    );
  }
};


/**
 * repeated string path = 1;
 * @return {!Array<string>}
 */
proto.Request.FileBySelector.prototype.getPathList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 1));
};


/**
 * @param {!Array<string>} value
 * @return {!proto.Request.FileBySelector} returns this
 */
proto.Request.FileBySelector.prototype.setPathList = function(value) {
  return jspb.Message.setField(this, 1, value || []);
};


/**
 * @param {string} value
 * @param {number=} opt_index
 * @return {!proto.Request.FileBySelector} returns this
 */
proto.Request.FileBySelector.prototype.addPath = function(value, opt_index) {
  return jspb.Message.addToRepeatedField(this, 1, value, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.Request.FileBySelector} returns this
 */
proto.Request.FileBySelector.prototype.clearPathList = function() {
  return this.setPathList([]);
};


/**
 * optional string selector = 2;
 * @return {string}
 */
proto.Request.FileBySelector.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.FileBySelector} returns this
 */
proto.Request.FileBySelector.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional bool strict = 3;
 * @return {boolean}
 */
proto.Request.FileBySelector.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 3, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.FileBySelector} returns this
 */
proto.Request.FileBySelector.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 3, value);
};


/**
 * optional string name = 4;
 * @return {string}
 */
proto.Request.FileBySelector.prototype.getName = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.FileBySelector} returns this
 */
proto.Request.FileBySelector.prototype.setName = function(value) {
  return jspb.Message.setProto3StringField(this, 4, value);
};


/**
 * optional string mimeType = 5;
 * @return {string}
 */
proto.Request.FileBySelector.prototype.getMimetype = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 5, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.FileBySelector} returns this
 */
proto.Request.FileBySelector.prototype.setMimetype = function(value) {
  return jspb.Message.setProto3StringField(this, 5, value);
};


/**
 * optional string buffer = 6;
 * @return {string}
 */
proto.Request.FileBySelector.prototype.getBuffer = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 6, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.FileBySelector} returns this
 */
proto.Request.FileBySelector.prototype.setBuffer = function(value) {
  return jspb.Message.setProto3StringField(this, 6, value);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.Request.LocatorHandlerAddCustom.repeatedFields_ = [4];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.LocatorHandlerAddCustom.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.LocatorHandlerAddCustom.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.LocatorHandlerAddCustom} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.LocatorHandlerAddCustom.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
nowaitafter: jspb.Message.getBooleanFieldWithDefault(msg, 2, false),
times: jspb.Message.getFieldWithDefault(msg, 3, ""),
handlerspecsList: jspb.Message.toObjectList(msg.getHandlerspecsList(),
    proto.Request.LocatorHandlerAddCustomAction.toObject, includeInstance)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.LocatorHandlerAddCustom}
 */
proto.Request.LocatorHandlerAddCustom.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.LocatorHandlerAddCustom;
  return proto.Request.LocatorHandlerAddCustom.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.LocatorHandlerAddCustom} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.LocatorHandlerAddCustom}
 */
proto.Request.LocatorHandlerAddCustom.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setNowaitafter(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setTimes(value);
      break;
    case 4:
      var value = new proto.Request.LocatorHandlerAddCustomAction;
      reader.readMessage(value,proto.Request.LocatorHandlerAddCustomAction.deserializeBinaryFromReader);
      msg.addHandlerspecs(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.LocatorHandlerAddCustom.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.LocatorHandlerAddCustom.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.LocatorHandlerAddCustom} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.LocatorHandlerAddCustom.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getNowaitafter();
  if (f) {
    writer.writeBool(
      2,
      f
    );
  }
  f = message.getTimes();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getHandlerspecsList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      4,
      f,
      proto.Request.LocatorHandlerAddCustomAction.serializeBinaryToWriter
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.LocatorHandlerAddCustom.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.LocatorHandlerAddCustom} returns this
 */
proto.Request.LocatorHandlerAddCustom.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional bool noWaitAfter = 2;
 * @return {boolean}
 */
proto.Request.LocatorHandlerAddCustom.prototype.getNowaitafter = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 2, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.LocatorHandlerAddCustom} returns this
 */
proto.Request.LocatorHandlerAddCustom.prototype.setNowaitafter = function(value) {
  return jspb.Message.setProto3BooleanField(this, 2, value);
};


/**
 * optional string times = 3;
 * @return {string}
 */
proto.Request.LocatorHandlerAddCustom.prototype.getTimes = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.LocatorHandlerAddCustom} returns this
 */
proto.Request.LocatorHandlerAddCustom.prototype.setTimes = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * repeated LocatorHandlerAddCustomAction handlerSpecs = 4;
 * @return {!Array<!proto.Request.LocatorHandlerAddCustomAction>}
 */
proto.Request.LocatorHandlerAddCustom.prototype.getHandlerspecsList = function() {
  return /** @type{!Array<!proto.Request.LocatorHandlerAddCustomAction>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.Request.LocatorHandlerAddCustomAction, 4));
};


/**
 * @param {!Array<!proto.Request.LocatorHandlerAddCustomAction>} value
 * @return {!proto.Request.LocatorHandlerAddCustom} returns this
*/
proto.Request.LocatorHandlerAddCustom.prototype.setHandlerspecsList = function(value) {
  return jspb.Message.setRepeatedWrapperField(this, 4, value);
};


/**
 * @param {!proto.Request.LocatorHandlerAddCustomAction=} opt_value
 * @param {number=} opt_index
 * @return {!proto.Request.LocatorHandlerAddCustomAction}
 */
proto.Request.LocatorHandlerAddCustom.prototype.addHandlerspecs = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 4, opt_value, proto.Request.LocatorHandlerAddCustomAction, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.Request.LocatorHandlerAddCustom} returns this
 */
proto.Request.LocatorHandlerAddCustom.prototype.clearHandlerspecsList = function() {
  return this.setHandlerspecsList([]);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.LocatorHandlerAddCustomAction.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.LocatorHandlerAddCustomAction.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.LocatorHandlerAddCustomAction} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.LocatorHandlerAddCustomAction.toObject = function(includeInstance, msg) {
  var f, obj = {
action: jspb.Message.getFieldWithDefault(msg, 1, ""),
selector: jspb.Message.getFieldWithDefault(msg, 2, ""),
value: jspb.Message.getFieldWithDefault(msg, 3, ""),
optionsasjson: jspb.Message.getFieldWithDefault(msg, 4, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.LocatorHandlerAddCustomAction}
 */
proto.Request.LocatorHandlerAddCustomAction.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.LocatorHandlerAddCustomAction;
  return proto.Request.LocatorHandlerAddCustomAction.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.LocatorHandlerAddCustomAction} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.LocatorHandlerAddCustomAction}
 */
proto.Request.LocatorHandlerAddCustomAction.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setAction(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setValue(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setOptionsasjson(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.LocatorHandlerAddCustomAction.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.LocatorHandlerAddCustomAction.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.LocatorHandlerAddCustomAction} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.LocatorHandlerAddCustomAction.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getAction();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getValue();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getOptionsasjson();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
};


/**
 * optional string action = 1;
 * @return {string}
 */
proto.Request.LocatorHandlerAddCustomAction.prototype.getAction = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.LocatorHandlerAddCustomAction} returns this
 */
proto.Request.LocatorHandlerAddCustomAction.prototype.setAction = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string selector = 2;
 * @return {string}
 */
proto.Request.LocatorHandlerAddCustomAction.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.LocatorHandlerAddCustomAction} returns this
 */
proto.Request.LocatorHandlerAddCustomAction.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string value = 3;
 * @return {string}
 */
proto.Request.LocatorHandlerAddCustomAction.prototype.getValue = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.LocatorHandlerAddCustomAction} returns this
 */
proto.Request.LocatorHandlerAddCustomAction.prototype.setValue = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional string optionsAsJson = 4;
 * @return {string}
 */
proto.Request.LocatorHandlerAddCustomAction.prototype.getOptionsasjson = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.LocatorHandlerAddCustomAction} returns this
 */
proto.Request.LocatorHandlerAddCustomAction.prototype.setOptionsasjson = function(value) {
  return jspb.Message.setProto3StringField(this, 4, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.LocatorHandlerRemove.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.LocatorHandlerRemove.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.LocatorHandlerRemove} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.LocatorHandlerRemove.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.LocatorHandlerRemove}
 */
proto.Request.LocatorHandlerRemove.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.LocatorHandlerRemove;
  return proto.Request.LocatorHandlerRemove.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.LocatorHandlerRemove} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.LocatorHandlerRemove}
 */
proto.Request.LocatorHandlerRemove.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.LocatorHandlerRemove.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.LocatorHandlerRemove.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.LocatorHandlerRemove} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.LocatorHandlerRemove.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.LocatorHandlerRemove.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.LocatorHandlerRemove} returns this
 */
proto.Request.LocatorHandlerRemove.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Json.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Json.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Json} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Json.toObject = function(includeInstance, msg) {
  var f, obj = {
body: jspb.Message.getFieldWithDefault(msg, 1, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Json}
 */
proto.Request.Json.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Json;
  return proto.Request.Json.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Json} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Json}
 */
proto.Request.Json.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setBody(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Json.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Json.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Json} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Json.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getBody();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
};


/**
 * optional string body = 1;
 * @return {string}
 */
proto.Request.Json.prototype.getBody = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Json} returns this
 */
proto.Request.Json.prototype.setBody = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.MouseButtonOptions.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.MouseButtonOptions.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.MouseButtonOptions} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.MouseButtonOptions.toObject = function(includeInstance, msg) {
  var f, obj = {
action: jspb.Message.getFieldWithDefault(msg, 1, ""),
json: jspb.Message.getFieldWithDefault(msg, 2, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.MouseButtonOptions}
 */
proto.Request.MouseButtonOptions.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.MouseButtonOptions;
  return proto.Request.MouseButtonOptions.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.MouseButtonOptions} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.MouseButtonOptions}
 */
proto.Request.MouseButtonOptions.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setAction(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setJson(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.MouseButtonOptions.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.MouseButtonOptions.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.MouseButtonOptions} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.MouseButtonOptions.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getAction();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getJson();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
};


/**
 * optional string action = 1;
 * @return {string}
 */
proto.Request.MouseButtonOptions.prototype.getAction = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.MouseButtonOptions} returns this
 */
proto.Request.MouseButtonOptions.prototype.setAction = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string json = 2;
 * @return {string}
 */
proto.Request.MouseButtonOptions.prototype.getJson = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.MouseButtonOptions} returns this
 */
proto.Request.MouseButtonOptions.prototype.setJson = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.MouseWheel.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.MouseWheel.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.MouseWheel} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.MouseWheel.toObject = function(includeInstance, msg) {
  var f, obj = {
deltax: jspb.Message.getFieldWithDefault(msg, 1, 0),
deltay: jspb.Message.getFieldWithDefault(msg, 2, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.MouseWheel}
 */
proto.Request.MouseWheel.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.MouseWheel;
  return proto.Request.MouseWheel.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.MouseWheel} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.MouseWheel}
 */
proto.Request.MouseWheel.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setDeltax(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setDeltay(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.MouseWheel.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.MouseWheel.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.MouseWheel} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.MouseWheel.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getDeltax();
  if (f !== 0) {
    writer.writeInt32(
      1,
      f
    );
  }
  f = message.getDeltay();
  if (f !== 0) {
    writer.writeInt32(
      2,
      f
    );
  }
};


/**
 * optional int32 deltaX = 1;
 * @return {number}
 */
proto.Request.MouseWheel.prototype.getDeltax = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 1, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.MouseWheel} returns this
 */
proto.Request.MouseWheel.prototype.setDeltax = function(value) {
  return jspb.Message.setProto3IntField(this, 1, value);
};


/**
 * optional int32 deltaY = 2;
 * @return {number}
 */
proto.Request.MouseWheel.prototype.getDeltay = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.MouseWheel} returns this
 */
proto.Request.MouseWheel.prototype.setDeltay = function(value) {
  return jspb.Message.setProto3IntField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.KeyboardKeypress.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.KeyboardKeypress.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.KeyboardKeypress} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.KeyboardKeypress.toObject = function(includeInstance, msg) {
  var f, obj = {
action: jspb.Message.getFieldWithDefault(msg, 1, ""),
key: jspb.Message.getFieldWithDefault(msg, 2, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.KeyboardKeypress}
 */
proto.Request.KeyboardKeypress.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.KeyboardKeypress;
  return proto.Request.KeyboardKeypress.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.KeyboardKeypress} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.KeyboardKeypress}
 */
proto.Request.KeyboardKeypress.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setAction(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setKey(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.KeyboardKeypress.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.KeyboardKeypress.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.KeyboardKeypress} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.KeyboardKeypress.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getAction();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getKey();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
};


/**
 * optional string action = 1;
 * @return {string}
 */
proto.Request.KeyboardKeypress.prototype.getAction = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.KeyboardKeypress} returns this
 */
proto.Request.KeyboardKeypress.prototype.setAction = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string key = 2;
 * @return {string}
 */
proto.Request.KeyboardKeypress.prototype.getKey = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.KeyboardKeypress} returns this
 */
proto.Request.KeyboardKeypress.prototype.setKey = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.KeyboardInputOptions.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.KeyboardInputOptions.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.KeyboardInputOptions} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.KeyboardInputOptions.toObject = function(includeInstance, msg) {
  var f, obj = {
action: jspb.Message.getFieldWithDefault(msg, 1, ""),
input: jspb.Message.getFieldWithDefault(msg, 2, ""),
delay: jspb.Message.getFieldWithDefault(msg, 3, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.KeyboardInputOptions}
 */
proto.Request.KeyboardInputOptions.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.KeyboardInputOptions;
  return proto.Request.KeyboardInputOptions.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.KeyboardInputOptions} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.KeyboardInputOptions}
 */
proto.Request.KeyboardInputOptions.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setAction(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setInput(value);
      break;
    case 3:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setDelay(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.KeyboardInputOptions.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.KeyboardInputOptions.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.KeyboardInputOptions} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.KeyboardInputOptions.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getAction();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getInput();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getDelay();
  if (f !== 0) {
    writer.writeInt32(
      3,
      f
    );
  }
};


/**
 * optional string action = 1;
 * @return {string}
 */
proto.Request.KeyboardInputOptions.prototype.getAction = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.KeyboardInputOptions} returns this
 */
proto.Request.KeyboardInputOptions.prototype.setAction = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string input = 2;
 * @return {string}
 */
proto.Request.KeyboardInputOptions.prototype.getInput = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.KeyboardInputOptions} returns this
 */
proto.Request.KeyboardInputOptions.prototype.setInput = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional int32 delay = 3;
 * @return {number}
 */
proto.Request.KeyboardInputOptions.prototype.getDelay = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 3, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.KeyboardInputOptions} returns this
 */
proto.Request.KeyboardInputOptions.prototype.setDelay = function(value) {
  return jspb.Message.setProto3IntField(this, 3, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Browser.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Browser.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Browser} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Browser.toObject = function(includeInstance, msg) {
  var f, obj = {
browser: jspb.Message.getFieldWithDefault(msg, 1, ""),
rawoptions: jspb.Message.getFieldWithDefault(msg, 2, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Browser}
 */
proto.Request.Browser.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Browser;
  return proto.Request.Browser.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Browser} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Browser}
 */
proto.Request.Browser.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setBrowser(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setRawoptions(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Browser.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Browser.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Browser} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Browser.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getBrowser();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getRawoptions();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
};


/**
 * optional string browser = 1;
 * @return {string}
 */
proto.Request.Browser.prototype.getBrowser = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Browser} returns this
 */
proto.Request.Browser.prototype.setBrowser = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string rawOptions = 2;
 * @return {string}
 */
proto.Request.Browser.prototype.getRawoptions = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Browser} returns this
 */
proto.Request.Browser.prototype.setRawoptions = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Context.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Context.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Context} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Context.toObject = function(includeInstance, msg) {
  var f, obj = {
rawoptions: jspb.Message.getFieldWithDefault(msg, 1, ""),
defaulttimeout: jspb.Message.getFieldWithDefault(msg, 2, 0),
tracefile: jspb.Message.getFieldWithDefault(msg, 3, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Context}
 */
proto.Request.Context.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Context;
  return proto.Request.Context.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Context} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Context}
 */
proto.Request.Context.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setRawoptions(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setDefaulttimeout(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setTracefile(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Context.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Context.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Context} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Context.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getRawoptions();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getDefaulttimeout();
  if (f !== 0) {
    writer.writeInt32(
      2,
      f
    );
  }
  f = message.getTracefile();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
};


/**
 * optional string rawOptions = 1;
 * @return {string}
 */
proto.Request.Context.prototype.getRawoptions = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Context} returns this
 */
proto.Request.Context.prototype.setRawoptions = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional int32 defaultTimeout = 2;
 * @return {number}
 */
proto.Request.Context.prototype.getDefaulttimeout = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.Context} returns this
 */
proto.Request.Context.prototype.setDefaulttimeout = function(value) {
  return jspb.Message.setProto3IntField(this, 2, value);
};


/**
 * optional string traceFile = 3;
 * @return {string}
 */
proto.Request.Context.prototype.getTracefile = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Context} returns this
 */
proto.Request.Context.prototype.setTracefile = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.PersistentContext.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.PersistentContext.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.PersistentContext} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.PersistentContext.toObject = function(includeInstance, msg) {
  var f, obj = {
browser: jspb.Message.getFieldWithDefault(msg, 1, ""),
rawoptions: jspb.Message.getFieldWithDefault(msg, 2, ""),
defaulttimeout: jspb.Message.getFieldWithDefault(msg, 3, 0),
tracefile: jspb.Message.getFieldWithDefault(msg, 4, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.PersistentContext}
 */
proto.Request.PersistentContext.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.PersistentContext;
  return proto.Request.PersistentContext.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.PersistentContext} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.PersistentContext}
 */
proto.Request.PersistentContext.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setBrowser(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setRawoptions(value);
      break;
    case 3:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setDefaulttimeout(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setTracefile(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.PersistentContext.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.PersistentContext.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.PersistentContext} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.PersistentContext.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getBrowser();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getRawoptions();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getDefaulttimeout();
  if (f !== 0) {
    writer.writeInt32(
      3,
      f
    );
  }
  f = message.getTracefile();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
};


/**
 * optional string browser = 1;
 * @return {string}
 */
proto.Request.PersistentContext.prototype.getBrowser = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.PersistentContext} returns this
 */
proto.Request.PersistentContext.prototype.setBrowser = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string rawOptions = 2;
 * @return {string}
 */
proto.Request.PersistentContext.prototype.getRawoptions = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.PersistentContext} returns this
 */
proto.Request.PersistentContext.prototype.setRawoptions = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional int32 defaultTimeout = 3;
 * @return {number}
 */
proto.Request.PersistentContext.prototype.getDefaulttimeout = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 3, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.PersistentContext} returns this
 */
proto.Request.PersistentContext.prototype.setDefaulttimeout = function(value) {
  return jspb.Message.setProto3IntField(this, 3, value);
};


/**
 * optional string traceFile = 4;
 * @return {string}
 */
proto.Request.PersistentContext.prototype.getTracefile = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.PersistentContext} returns this
 */
proto.Request.PersistentContext.prototype.setTracefile = function(value) {
  return jspb.Message.setProto3StringField(this, 4, value);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.Request.ElectronLaunch.repeatedFields_ = [2];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.ElectronLaunch.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.ElectronLaunch.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.ElectronLaunch} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ElectronLaunch.toObject = function(includeInstance, msg) {
  var f, obj = {
executablePath: jspb.Message.getFieldWithDefault(msg, 1, ""),
argsList: (f = jspb.Message.getRepeatedField(msg, 2)) == null ? undefined : f,
envMap: (f = msg.getEnvMap()) ? f.toObject(includeInstance, undefined) : [],
timeout: jspb.Message.getFieldWithDefault(msg, 4, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.ElectronLaunch}
 */
proto.Request.ElectronLaunch.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.ElectronLaunch;
  return proto.Request.ElectronLaunch.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.ElectronLaunch} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.ElectronLaunch}
 */
proto.Request.ElectronLaunch.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setExecutablePath(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.addArgs(value);
      break;
    case 3:
      var value = msg.getEnvMap();
      reader.readMessage(value, function(message, reader) {
        jspb.Map.deserializeBinary(message, reader, jspb.BinaryReader.prototype.readString, jspb.BinaryReader.prototype.readString, null, "", "");
         });
      break;
    case 4:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setTimeout(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.ElectronLaunch.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.ElectronLaunch.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.ElectronLaunch} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ElectronLaunch.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getExecutablePath();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getArgsList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      2,
      f
    );
  }
  f = message.getEnvMap(true);
  if (f && f.getLength() > 0) {
    f.serializeBinary(3, writer, jspb.BinaryWriter.prototype.writeString, jspb.BinaryWriter.prototype.writeString);
  }
  f = message.getTimeout();
  if (f !== 0) {
    writer.writeInt32(
      4,
      f
    );
  }
};


/**
 * optional string executable_path = 1;
 * @return {string}
 */
proto.Request.ElectronLaunch.prototype.getExecutablePath = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElectronLaunch} returns this
 */
proto.Request.ElectronLaunch.prototype.setExecutablePath = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * repeated string args = 2;
 * @return {!Array<string>}
 */
proto.Request.ElectronLaunch.prototype.getArgsList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 2));
};


/**
 * @param {!Array<string>} value
 * @return {!proto.Request.ElectronLaunch} returns this
 */
proto.Request.ElectronLaunch.prototype.setArgsList = function(value) {
  return jspb.Message.setField(this, 2, value || []);
};


/**
 * @param {string} value
 * @param {number=} opt_index
 * @return {!proto.Request.ElectronLaunch} returns this
 */
proto.Request.ElectronLaunch.prototype.addArgs = function(value, opt_index) {
  return jspb.Message.addToRepeatedField(this, 2, value, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.Request.ElectronLaunch} returns this
 */
proto.Request.ElectronLaunch.prototype.clearArgsList = function() {
  return this.setArgsList([]);
};


/**
 * map<string, string> env = 3;
 * @param {boolean=} opt_noLazyCreate Do not create the map if
 * empty, instead returning `undefined`
 * @return {!jspb.Map<string,string>}
 */
proto.Request.ElectronLaunch.prototype.getEnvMap = function(opt_noLazyCreate) {
  return /** @type {!jspb.Map<string,string>} */ (
      jspb.Message.getMapField(this, 3, opt_noLazyCreate,
      null));
};


/**
 * Clears values from the map. The map will be non-null.
 * @return {!proto.Request.ElectronLaunch} returns this
 */
proto.Request.ElectronLaunch.prototype.clearEnvMap = function() {
  this.getEnvMap().clear();
  return this;
};


/**
 * optional int32 timeout = 4;
 * @return {number}
 */
proto.Request.ElectronLaunch.prototype.getTimeout = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 4, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.ElectronLaunch} returns this
 */
proto.Request.ElectronLaunch.prototype.setTimeout = function(value) {
  return jspb.Message.setProto3IntField(this, 4, value);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.Request.Permissions.repeatedFields_ = [1];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Permissions.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Permissions.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Permissions} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Permissions.toObject = function(includeInstance, msg) {
  var f, obj = {
permissionsList: (f = jspb.Message.getRepeatedField(msg, 1)) == null ? undefined : f,
origin: jspb.Message.getFieldWithDefault(msg, 2, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Permissions}
 */
proto.Request.Permissions.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Permissions;
  return proto.Request.Permissions.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Permissions} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Permissions}
 */
proto.Request.Permissions.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.addPermissions(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setOrigin(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Permissions.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Permissions.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Permissions} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Permissions.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getPermissionsList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      1,
      f
    );
  }
  f = message.getOrigin();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
};


/**
 * repeated string permissions = 1;
 * @return {!Array<string>}
 */
proto.Request.Permissions.prototype.getPermissionsList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 1));
};


/**
 * @param {!Array<string>} value
 * @return {!proto.Request.Permissions} returns this
 */
proto.Request.Permissions.prototype.setPermissionsList = function(value) {
  return jspb.Message.setField(this, 1, value || []);
};


/**
 * @param {string} value
 * @param {number=} opt_index
 * @return {!proto.Request.Permissions} returns this
 */
proto.Request.Permissions.prototype.addPermissions = function(value, opt_index) {
  return jspb.Message.addToRepeatedField(this, 1, value, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.Request.Permissions} returns this
 */
proto.Request.Permissions.prototype.clearPermissionsList = function() {
  return this.setPermissionsList([]);
};


/**
 * optional string origin = 2;
 * @return {string}
 */
proto.Request.Permissions.prototype.getOrigin = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Permissions} returns this
 */
proto.Request.Permissions.prototype.setOrigin = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Url.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Url.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Url} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Url.toObject = function(includeInstance, msg) {
  var f, obj = {
url: jspb.Message.getFieldWithDefault(msg, 1, ""),
defaulttimeout: jspb.Message.getFieldWithDefault(msg, 2, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Url}
 */
proto.Request.Url.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Url;
  return proto.Request.Url.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Url} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Url}
 */
proto.Request.Url.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setUrl(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setDefaulttimeout(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Url.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Url.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Url} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Url.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getUrl();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getDefaulttimeout();
  if (f !== 0) {
    writer.writeInt32(
      2,
      f
    );
  }
};


/**
 * optional string url = 1;
 * @return {string}
 */
proto.Request.Url.prototype.getUrl = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Url} returns this
 */
proto.Request.Url.prototype.setUrl = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional int32 defaultTimeout = 2;
 * @return {number}
 */
proto.Request.Url.prototype.getDefaulttimeout = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.Url} returns this
 */
proto.Request.Url.prototype.setDefaulttimeout = function(value) {
  return jspb.Message.setProto3IntField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.DownloadOptions.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.DownloadOptions.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.DownloadOptions} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.DownloadOptions.toObject = function(includeInstance, msg) {
  var f, obj = {
url: jspb.Message.getFieldWithDefault(msg, 1, ""),
path: jspb.Message.getFieldWithDefault(msg, 2, ""),
waitforfinish: jspb.Message.getBooleanFieldWithDefault(msg, 3, false),
downloadtimeout: jspb.Message.getFieldWithDefault(msg, 4, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.DownloadOptions}
 */
proto.Request.DownloadOptions.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.DownloadOptions;
  return proto.Request.DownloadOptions.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.DownloadOptions} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.DownloadOptions}
 */
proto.Request.DownloadOptions.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setUrl(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setPath(value);
      break;
    case 3:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setWaitforfinish(value);
      break;
    case 4:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setDownloadtimeout(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.DownloadOptions.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.DownloadOptions.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.DownloadOptions} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.DownloadOptions.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getUrl();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getPath();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getWaitforfinish();
  if (f) {
    writer.writeBool(
      3,
      f
    );
  }
  f = message.getDownloadtimeout();
  if (f !== 0) {
    writer.writeInt32(
      4,
      f
    );
  }
};


/**
 * optional string url = 1;
 * @return {string}
 */
proto.Request.DownloadOptions.prototype.getUrl = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.DownloadOptions} returns this
 */
proto.Request.DownloadOptions.prototype.setUrl = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string path = 2;
 * @return {string}
 */
proto.Request.DownloadOptions.prototype.getPath = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.DownloadOptions} returns this
 */
proto.Request.DownloadOptions.prototype.setPath = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional bool waitForFinish = 3;
 * @return {boolean}
 */
proto.Request.DownloadOptions.prototype.getWaitforfinish = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 3, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.DownloadOptions} returns this
 */
proto.Request.DownloadOptions.prototype.setWaitforfinish = function(value) {
  return jspb.Message.setProto3BooleanField(this, 3, value);
};


/**
 * optional int32 downloadTimeout = 4;
 * @return {number}
 */
proto.Request.DownloadOptions.prototype.getDownloadtimeout = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 4, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.DownloadOptions} returns this
 */
proto.Request.DownloadOptions.prototype.setDownloadtimeout = function(value) {
  return jspb.Message.setProto3IntField(this, 4, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.DownloadID.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.DownloadID.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.DownloadID} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.DownloadID.toObject = function(includeInstance, msg) {
  var f, obj = {
id: jspb.Message.getFieldWithDefault(msg, 1, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.DownloadID}
 */
proto.Request.DownloadID.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.DownloadID;
  return proto.Request.DownloadID.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.DownloadID} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.DownloadID}
 */
proto.Request.DownloadID.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setId(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.DownloadID.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.DownloadID.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.DownloadID} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.DownloadID.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getId();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
};


/**
 * optional string id = 1;
 * @return {string}
 */
proto.Request.DownloadID.prototype.getId = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.DownloadID} returns this
 */
proto.Request.DownloadID.prototype.setId = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.UrlOptions.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.UrlOptions.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.UrlOptions} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.UrlOptions.toObject = function(includeInstance, msg) {
  var f, obj = {
url: (f = msg.getUrl()) && proto.Request.Url.toObject(includeInstance, f),
waituntil: jspb.Message.getFieldWithDefault(msg, 2, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.UrlOptions}
 */
proto.Request.UrlOptions.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.UrlOptions;
  return proto.Request.UrlOptions.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.UrlOptions} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.UrlOptions}
 */
proto.Request.UrlOptions.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new proto.Request.Url;
      reader.readMessage(value,proto.Request.Url.deserializeBinaryFromReader);
      msg.setUrl(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setWaituntil(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.UrlOptions.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.UrlOptions.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.UrlOptions} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.UrlOptions.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getUrl();
  if (f != null) {
    writer.writeMessage(
      1,
      f,
      proto.Request.Url.serializeBinaryToWriter
    );
  }
  f = message.getWaituntil();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
};


/**
 * optional Url url = 1;
 * @return {?proto.Request.Url}
 */
proto.Request.UrlOptions.prototype.getUrl = function() {
  return /** @type{?proto.Request.Url} */ (
    jspb.Message.getWrapperField(this, proto.Request.Url, 1));
};


/**
 * @param {?proto.Request.Url|undefined} value
 * @return {!proto.Request.UrlOptions} returns this
*/
proto.Request.UrlOptions.prototype.setUrl = function(value) {
  return jspb.Message.setWrapperField(this, 1, value);
};


/**
 * Clears the message field making it undefined.
 * @return {!proto.Request.UrlOptions} returns this
 */
proto.Request.UrlOptions.prototype.clearUrl = function() {
  return this.setUrl(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.Request.UrlOptions.prototype.hasUrl = function() {
  return jspb.Message.getField(this, 1) != null;
};


/**
 * optional string waitUntil = 2;
 * @return {string}
 */
proto.Request.UrlOptions.prototype.getWaituntil = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.UrlOptions} returns this
 */
proto.Request.UrlOptions.prototype.setWaituntil = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.PageLoadState.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.PageLoadState.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.PageLoadState} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.PageLoadState.toObject = function(includeInstance, msg) {
  var f, obj = {
state: jspb.Message.getFieldWithDefault(msg, 1, ""),
timeout: jspb.Message.getFieldWithDefault(msg, 2, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.PageLoadState}
 */
proto.Request.PageLoadState.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.PageLoadState;
  return proto.Request.PageLoadState.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.PageLoadState} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.PageLoadState}
 */
proto.Request.PageLoadState.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setState(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setTimeout(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.PageLoadState.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.PageLoadState.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.PageLoadState} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.PageLoadState.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getState();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getTimeout();
  if (f !== 0) {
    writer.writeInt32(
      2,
      f
    );
  }
};


/**
 * optional string state = 1;
 * @return {string}
 */
proto.Request.PageLoadState.prototype.getState = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.PageLoadState} returns this
 */
proto.Request.PageLoadState.prototype.setState = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional int32 timeout = 2;
 * @return {number}
 */
proto.Request.PageLoadState.prototype.getTimeout = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.PageLoadState} returns this
 */
proto.Request.PageLoadState.prototype.setTimeout = function(value) {
  return jspb.Message.setProto3IntField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.ConnectBrowser.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.ConnectBrowser.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.ConnectBrowser} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ConnectBrowser.toObject = function(includeInstance, msg) {
  var f, obj = {
browser: jspb.Message.getFieldWithDefault(msg, 1, ""),
url: jspb.Message.getFieldWithDefault(msg, 2, ""),
connectcdp: jspb.Message.getBooleanFieldWithDefault(msg, 3, false),
timeout: jspb.Message.getFieldWithDefault(msg, 4, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.ConnectBrowser}
 */
proto.Request.ConnectBrowser.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.ConnectBrowser;
  return proto.Request.ConnectBrowser.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.ConnectBrowser} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.ConnectBrowser}
 */
proto.Request.ConnectBrowser.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setBrowser(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setUrl(value);
      break;
    case 3:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setConnectcdp(value);
      break;
    case 4:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setTimeout(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.ConnectBrowser.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.ConnectBrowser.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.ConnectBrowser} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ConnectBrowser.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getBrowser();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getUrl();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getConnectcdp();
  if (f) {
    writer.writeBool(
      3,
      f
    );
  }
  f = message.getTimeout();
  if (f !== 0) {
    writer.writeInt32(
      4,
      f
    );
  }
};


/**
 * optional string browser = 1;
 * @return {string}
 */
proto.Request.ConnectBrowser.prototype.getBrowser = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ConnectBrowser} returns this
 */
proto.Request.ConnectBrowser.prototype.setBrowser = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string url = 2;
 * @return {string}
 */
proto.Request.ConnectBrowser.prototype.getUrl = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ConnectBrowser} returns this
 */
proto.Request.ConnectBrowser.prototype.setUrl = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional bool connectCDP = 3;
 * @return {boolean}
 */
proto.Request.ConnectBrowser.prototype.getConnectcdp = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 3, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.ConnectBrowser} returns this
 */
proto.Request.ConnectBrowser.prototype.setConnectcdp = function(value) {
  return jspb.Message.setProto3BooleanField(this, 3, value);
};


/**
 * optional int32 timeout = 4;
 * @return {number}
 */
proto.Request.ConnectBrowser.prototype.getTimeout = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 4, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.ConnectBrowser} returns this
 */
proto.Request.ConnectBrowser.prototype.setTimeout = function(value) {
  return jspb.Message.setProto3IntField(this, 4, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.TextInput.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.TextInput.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.TextInput} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.TextInput.toObject = function(includeInstance, msg) {
  var f, obj = {
input: jspb.Message.getFieldWithDefault(msg, 1, ""),
selector: jspb.Message.getFieldWithDefault(msg, 2, ""),
type: jspb.Message.getBooleanFieldWithDefault(msg, 3, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.TextInput}
 */
proto.Request.TextInput.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.TextInput;
  return proto.Request.TextInput.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.TextInput} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.TextInput}
 */
proto.Request.TextInput.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setInput(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 3:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setType(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.TextInput.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.TextInput.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.TextInput} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.TextInput.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getInput();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getType();
  if (f) {
    writer.writeBool(
      3,
      f
    );
  }
};


/**
 * optional string input = 1;
 * @return {string}
 */
proto.Request.TextInput.prototype.getInput = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.TextInput} returns this
 */
proto.Request.TextInput.prototype.setInput = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string selector = 2;
 * @return {string}
 */
proto.Request.TextInput.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.TextInput} returns this
 */
proto.Request.TextInput.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional bool type = 3;
 * @return {boolean}
 */
proto.Request.TextInput.prototype.getType = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 3, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.TextInput} returns this
 */
proto.Request.TextInput.prototype.setType = function(value) {
  return jspb.Message.setProto3BooleanField(this, 3, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.ElementProperty.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.ElementProperty.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.ElementProperty} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ElementProperty.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
property: jspb.Message.getFieldWithDefault(msg, 2, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 3, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.ElementProperty}
 */
proto.Request.ElementProperty.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.ElementProperty;
  return proto.Request.ElementProperty.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.ElementProperty} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.ElementProperty}
 */
proto.Request.ElementProperty.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setProperty(value);
      break;
    case 3:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.ElementProperty.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.ElementProperty.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.ElementProperty} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ElementProperty.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getProperty();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      3,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.ElementProperty.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementProperty} returns this
 */
proto.Request.ElementProperty.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string property = 2;
 * @return {string}
 */
proto.Request.ElementProperty.prototype.getProperty = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementProperty} returns this
 */
proto.Request.ElementProperty.prototype.setProperty = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional bool strict = 3;
 * @return {boolean}
 */
proto.Request.ElementProperty.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 3, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.ElementProperty} returns this
 */
proto.Request.ElementProperty.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 3, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.TypeText.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.TypeText.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.TypeText} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.TypeText.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
text: jspb.Message.getFieldWithDefault(msg, 2, ""),
delay: jspb.Message.getFieldWithDefault(msg, 3, 0),
clear: jspb.Message.getBooleanFieldWithDefault(msg, 4, false),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 5, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.TypeText}
 */
proto.Request.TypeText.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.TypeText;
  return proto.Request.TypeText.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.TypeText} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.TypeText}
 */
proto.Request.TypeText.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setText(value);
      break;
    case 3:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setDelay(value);
      break;
    case 4:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setClear(value);
      break;
    case 5:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.TypeText.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.TypeText.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.TypeText} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.TypeText.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getText();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getDelay();
  if (f !== 0) {
    writer.writeInt32(
      3,
      f
    );
  }
  f = message.getClear();
  if (f) {
    writer.writeBool(
      4,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      5,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.TypeText.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.TypeText} returns this
 */
proto.Request.TypeText.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string text = 2;
 * @return {string}
 */
proto.Request.TypeText.prototype.getText = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.TypeText} returns this
 */
proto.Request.TypeText.prototype.setText = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional int32 delay = 3;
 * @return {number}
 */
proto.Request.TypeText.prototype.getDelay = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 3, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.TypeText} returns this
 */
proto.Request.TypeText.prototype.setDelay = function(value) {
  return jspb.Message.setProto3IntField(this, 3, value);
};


/**
 * optional bool clear = 4;
 * @return {boolean}
 */
proto.Request.TypeText.prototype.getClear = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 4, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.TypeText} returns this
 */
proto.Request.TypeText.prototype.setClear = function(value) {
  return jspb.Message.setProto3BooleanField(this, 4, value);
};


/**
 * optional bool strict = 5;
 * @return {boolean}
 */
proto.Request.TypeText.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 5, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.TypeText} returns this
 */
proto.Request.TypeText.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 5, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.FillText.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.FillText.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.FillText} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.FillText.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
text: jspb.Message.getFieldWithDefault(msg, 2, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 3, false),
force: jspb.Message.getBooleanFieldWithDefault(msg, 4, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.FillText}
 */
proto.Request.FillText.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.FillText;
  return proto.Request.FillText.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.FillText} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.FillText}
 */
proto.Request.FillText.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setText(value);
      break;
    case 3:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    case 4:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setForce(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.FillText.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.FillText.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.FillText} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.FillText.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getText();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      3,
      f
    );
  }
  f = message.getForce();
  if (f) {
    writer.writeBool(
      4,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.FillText.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.FillText} returns this
 */
proto.Request.FillText.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string text = 2;
 * @return {string}
 */
proto.Request.FillText.prototype.getText = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.FillText} returns this
 */
proto.Request.FillText.prototype.setText = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional bool strict = 3;
 * @return {boolean}
 */
proto.Request.FillText.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 3, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.FillText} returns this
 */
proto.Request.FillText.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 3, value);
};


/**
 * optional bool force = 4;
 * @return {boolean}
 */
proto.Request.FillText.prototype.getForce = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 4, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.FillText} returns this
 */
proto.Request.FillText.prototype.setForce = function(value) {
  return jspb.Message.setProto3BooleanField(this, 4, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.ClearText.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.ClearText.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.ClearText} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ClearText.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 2, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.ClearText}
 */
proto.Request.ClearText.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.ClearText;
  return proto.Request.ClearText.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.ClearText} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.ClearText}
 */
proto.Request.ClearText.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.ClearText.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.ClearText.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.ClearText} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ClearText.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      2,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.ClearText.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ClearText} returns this
 */
proto.Request.ClearText.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional bool strict = 2;
 * @return {boolean}
 */
proto.Request.ClearText.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 2, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.ClearText} returns this
 */
proto.Request.ClearText.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 2, value);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.Request.PressKeys.repeatedFields_ = [3];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.PressKeys.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.PressKeys.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.PressKeys} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.PressKeys.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 2, false),
keyList: (f = jspb.Message.getRepeatedField(msg, 3)) == null ? undefined : f,
pressdelay: jspb.Message.getFieldWithDefault(msg, 4, 0),
keydelay: jspb.Message.getFieldWithDefault(msg, 5, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.PressKeys}
 */
proto.Request.PressKeys.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.PressKeys;
  return proto.Request.PressKeys.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.PressKeys} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.PressKeys}
 */
proto.Request.PressKeys.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.addKey(value);
      break;
    case 4:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setPressdelay(value);
      break;
    case 5:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setKeydelay(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.PressKeys.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.PressKeys.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.PressKeys} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.PressKeys.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      2,
      f
    );
  }
  f = message.getKeyList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      3,
      f
    );
  }
  f = message.getPressdelay();
  if (f !== 0) {
    writer.writeInt32(
      4,
      f
    );
  }
  f = message.getKeydelay();
  if (f !== 0) {
    writer.writeInt32(
      5,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.PressKeys.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.PressKeys} returns this
 */
proto.Request.PressKeys.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional bool strict = 2;
 * @return {boolean}
 */
proto.Request.PressKeys.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 2, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.PressKeys} returns this
 */
proto.Request.PressKeys.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 2, value);
};


/**
 * repeated string key = 3;
 * @return {!Array<string>}
 */
proto.Request.PressKeys.prototype.getKeyList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 3));
};


/**
 * @param {!Array<string>} value
 * @return {!proto.Request.PressKeys} returns this
 */
proto.Request.PressKeys.prototype.setKeyList = function(value) {
  return jspb.Message.setField(this, 3, value || []);
};


/**
 * @param {string} value
 * @param {number=} opt_index
 * @return {!proto.Request.PressKeys} returns this
 */
proto.Request.PressKeys.prototype.addKey = function(value, opt_index) {
  return jspb.Message.addToRepeatedField(this, 3, value, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.Request.PressKeys} returns this
 */
proto.Request.PressKeys.prototype.clearKeyList = function() {
  return this.setKeyList([]);
};


/**
 * optional int32 pressDelay = 4;
 * @return {number}
 */
proto.Request.PressKeys.prototype.getPressdelay = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 4, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.PressKeys} returns this
 */
proto.Request.PressKeys.prototype.setPressdelay = function(value) {
  return jspb.Message.setProto3IntField(this, 4, value);
};


/**
 * optional int32 keyDelay = 5;
 * @return {number}
 */
proto.Request.PressKeys.prototype.getKeydelay = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 5, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.PressKeys} returns this
 */
proto.Request.PressKeys.prototype.setKeydelay = function(value) {
  return jspb.Message.setProto3IntField(this, 5, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.ElementSelector.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.ElementSelector.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.ElementSelector} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ElementSelector.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 2, false),
force: jspb.Message.getBooleanFieldWithDefault(msg, 3, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.ElementSelector}
 */
proto.Request.ElementSelector.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.ElementSelector;
  return proto.Request.ElementSelector.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.ElementSelector} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.ElementSelector}
 */
proto.Request.ElementSelector.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    case 3:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setForce(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.ElementSelector.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.ElementSelector.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.ElementSelector} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ElementSelector.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      2,
      f
    );
  }
  f = message.getForce();
  if (f) {
    writer.writeBool(
      3,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.ElementSelector.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementSelector} returns this
 */
proto.Request.ElementSelector.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional bool strict = 2;
 * @return {boolean}
 */
proto.Request.ElementSelector.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 2, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.ElementSelector} returns this
 */
proto.Request.ElementSelector.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 2, value);
};


/**
 * optional bool force = 3;
 * @return {boolean}
 */
proto.Request.ElementSelector.prototype.getForce = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 3, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.ElementSelector} returns this
 */
proto.Request.ElementSelector.prototype.setForce = function(value) {
  return jspb.Message.setProto3BooleanField(this, 3, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Timeout.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Timeout.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Timeout} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Timeout.toObject = function(includeInstance, msg) {
  var f, obj = {
timeout: jspb.Message.getFloatingPointFieldWithDefault(msg, 1, 0.0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Timeout}
 */
proto.Request.Timeout.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Timeout;
  return proto.Request.Timeout.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Timeout} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Timeout}
 */
proto.Request.Timeout.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setTimeout(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Timeout.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Timeout.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Timeout} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Timeout.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getTimeout();
  if (f !== 0.0) {
    writer.writeFloat(
      1,
      f
    );
  }
};


/**
 * optional float timeout = 1;
 * @return {number}
 */
proto.Request.Timeout.prototype.getTimeout = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 1, 0.0));
};


/**
 * @param {number} value
 * @return {!proto.Request.Timeout} returns this
 */
proto.Request.Timeout.prototype.setTimeout = function(value) {
  return jspb.Message.setProto3FloatField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Index.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Index.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Index} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Index.toObject = function(includeInstance, msg) {
  var f, obj = {
index: jspb.Message.getFieldWithDefault(msg, 1, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Index}
 */
proto.Request.Index.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Index;
  return proto.Request.Index.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Index} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Index}
 */
proto.Request.Index.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setIndex(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Index.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Index.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Index} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Index.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getIndex();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
};


/**
 * optional string index = 1;
 * @return {string}
 */
proto.Request.Index.prototype.getIndex = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Index} returns this
 */
proto.Request.Index.prototype.setIndex = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.IdWithTimeout.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.IdWithTimeout.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.IdWithTimeout} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.IdWithTimeout.toObject = function(includeInstance, msg) {
  var f, obj = {
id: jspb.Message.getFieldWithDefault(msg, 1, ""),
timeout: jspb.Message.getFloatingPointFieldWithDefault(msg, 2, 0.0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.IdWithTimeout}
 */
proto.Request.IdWithTimeout.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.IdWithTimeout;
  return proto.Request.IdWithTimeout.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.IdWithTimeout} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.IdWithTimeout}
 */
proto.Request.IdWithTimeout.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setId(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setTimeout(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.IdWithTimeout.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.IdWithTimeout.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.IdWithTimeout} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.IdWithTimeout.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getId();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getTimeout();
  if (f !== 0.0) {
    writer.writeFloat(
      2,
      f
    );
  }
};


/**
 * optional string id = 1;
 * @return {string}
 */
proto.Request.IdWithTimeout.prototype.getId = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.IdWithTimeout} returns this
 */
proto.Request.IdWithTimeout.prototype.setId = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional float timeout = 2;
 * @return {number}
 */
proto.Request.IdWithTimeout.prototype.getTimeout = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 2, 0.0));
};


/**
 * @param {number} value
 * @return {!proto.Request.IdWithTimeout} returns this
 */
proto.Request.IdWithTimeout.prototype.setTimeout = function(value) {
  return jspb.Message.setProto3FloatField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.StyleTag.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.StyleTag.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.StyleTag} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.StyleTag.toObject = function(includeInstance, msg) {
  var f, obj = {
content: jspb.Message.getFieldWithDefault(msg, 1, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.StyleTag}
 */
proto.Request.StyleTag.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.StyleTag;
  return proto.Request.StyleTag.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.StyleTag} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.StyleTag}
 */
proto.Request.StyleTag.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setContent(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.StyleTag.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.StyleTag.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.StyleTag} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.StyleTag.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getContent();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
};


/**
 * optional string content = 1;
 * @return {string}
 */
proto.Request.StyleTag.prototype.getContent = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.StyleTag} returns this
 */
proto.Request.StyleTag.prototype.setContent = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.ElementSelectorWithOptions.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.ElementSelectorWithOptions.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.ElementSelectorWithOptions} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ElementSelectorWithOptions.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
options: jspb.Message.getFieldWithDefault(msg, 2, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 3, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.ElementSelectorWithOptions}
 */
proto.Request.ElementSelectorWithOptions.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.ElementSelectorWithOptions;
  return proto.Request.ElementSelectorWithOptions.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.ElementSelectorWithOptions} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.ElementSelectorWithOptions}
 */
proto.Request.ElementSelectorWithOptions.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setOptions(value);
      break;
    case 3:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.ElementSelectorWithOptions.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.ElementSelectorWithOptions.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.ElementSelectorWithOptions} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ElementSelectorWithOptions.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getOptions();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      3,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.ElementSelectorWithOptions.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementSelectorWithOptions} returns this
 */
proto.Request.ElementSelectorWithOptions.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string options = 2;
 * @return {string}
 */
proto.Request.ElementSelectorWithOptions.prototype.getOptions = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementSelectorWithOptions} returns this
 */
proto.Request.ElementSelectorWithOptions.prototype.setOptions = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional bool strict = 3;
 * @return {boolean}
 */
proto.Request.ElementSelectorWithOptions.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 3, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.ElementSelectorWithOptions} returns this
 */
proto.Request.ElementSelectorWithOptions.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 3, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.ElementSelectorWithDuration.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.ElementSelectorWithDuration.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.ElementSelectorWithDuration} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ElementSelectorWithDuration.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
duration: jspb.Message.getFieldWithDefault(msg, 2, 0),
width: jspb.Message.getFieldWithDefault(msg, 3, ""),
style: jspb.Message.getFieldWithDefault(msg, 4, ""),
color: jspb.Message.getFieldWithDefault(msg, 5, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 6, false),
mode: jspb.Message.getFieldWithDefault(msg, 7, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.ElementSelectorWithDuration}
 */
proto.Request.ElementSelectorWithDuration.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.ElementSelectorWithDuration;
  return proto.Request.ElementSelectorWithDuration.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.ElementSelectorWithDuration} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.ElementSelectorWithDuration}
 */
proto.Request.ElementSelectorWithDuration.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setDuration(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setWidth(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setStyle(value);
      break;
    case 5:
      var value = /** @type {string} */ (reader.readString());
      msg.setColor(value);
      break;
    case 6:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    case 7:
      var value = /** @type {string} */ (reader.readString());
      msg.setMode(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.ElementSelectorWithDuration.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.ElementSelectorWithDuration.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.ElementSelectorWithDuration} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ElementSelectorWithDuration.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getDuration();
  if (f !== 0) {
    writer.writeInt32(
      2,
      f
    );
  }
  f = message.getWidth();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getStyle();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
  f = message.getColor();
  if (f.length > 0) {
    writer.writeString(
      5,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      6,
      f
    );
  }
  f = message.getMode();
  if (f.length > 0) {
    writer.writeString(
      7,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.ElementSelectorWithDuration.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementSelectorWithDuration} returns this
 */
proto.Request.ElementSelectorWithDuration.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional int32 duration = 2;
 * @return {number}
 */
proto.Request.ElementSelectorWithDuration.prototype.getDuration = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.ElementSelectorWithDuration} returns this
 */
proto.Request.ElementSelectorWithDuration.prototype.setDuration = function(value) {
  return jspb.Message.setProto3IntField(this, 2, value);
};


/**
 * optional string width = 3;
 * @return {string}
 */
proto.Request.ElementSelectorWithDuration.prototype.getWidth = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementSelectorWithDuration} returns this
 */
proto.Request.ElementSelectorWithDuration.prototype.setWidth = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional string style = 4;
 * @return {string}
 */
proto.Request.ElementSelectorWithDuration.prototype.getStyle = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementSelectorWithDuration} returns this
 */
proto.Request.ElementSelectorWithDuration.prototype.setStyle = function(value) {
  return jspb.Message.setProto3StringField(this, 4, value);
};


/**
 * optional string color = 5;
 * @return {string}
 */
proto.Request.ElementSelectorWithDuration.prototype.getColor = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 5, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementSelectorWithDuration} returns this
 */
proto.Request.ElementSelectorWithDuration.prototype.setColor = function(value) {
  return jspb.Message.setProto3StringField(this, 5, value);
};


/**
 * optional bool strict = 6;
 * @return {boolean}
 */
proto.Request.ElementSelectorWithDuration.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 6, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.ElementSelectorWithDuration} returns this
 */
proto.Request.ElementSelectorWithDuration.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 6, value);
};


/**
 * optional string mode = 7;
 * @return {string}
 */
proto.Request.ElementSelectorWithDuration.prototype.getMode = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 7, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementSelectorWithDuration} returns this
 */
proto.Request.ElementSelectorWithDuration.prototype.setMode = function(value) {
  return jspb.Message.setProto3StringField(this, 7, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.SelectElementSelector.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.SelectElementSelector.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.SelectElementSelector} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.SelectElementSelector.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
matcherjson: jspb.Message.getFieldWithDefault(msg, 2, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 3, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.SelectElementSelector}
 */
proto.Request.SelectElementSelector.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.SelectElementSelector;
  return proto.Request.SelectElementSelector.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.SelectElementSelector} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.SelectElementSelector}
 */
proto.Request.SelectElementSelector.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setMatcherjson(value);
      break;
    case 3:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.SelectElementSelector.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.SelectElementSelector.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.SelectElementSelector} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.SelectElementSelector.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getMatcherjson();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      3,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.SelectElementSelector.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.SelectElementSelector} returns this
 */
proto.Request.SelectElementSelector.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string matcherJson = 2;
 * @return {string}
 */
proto.Request.SelectElementSelector.prototype.getMatcherjson = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.SelectElementSelector} returns this
 */
proto.Request.SelectElementSelector.prototype.setMatcherjson = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional bool strict = 3;
 * @return {boolean}
 */
proto.Request.SelectElementSelector.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 3, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.SelectElementSelector} returns this
 */
proto.Request.SelectElementSelector.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 3, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.WaitForFunctionOptions.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.WaitForFunctionOptions.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.WaitForFunctionOptions} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.WaitForFunctionOptions.toObject = function(includeInstance, msg) {
  var f, obj = {
script: jspb.Message.getFieldWithDefault(msg, 1, ""),
selector: jspb.Message.getFieldWithDefault(msg, 2, ""),
options: jspb.Message.getFieldWithDefault(msg, 3, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 4, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.WaitForFunctionOptions}
 */
proto.Request.WaitForFunctionOptions.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.WaitForFunctionOptions;
  return proto.Request.WaitForFunctionOptions.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.WaitForFunctionOptions} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.WaitForFunctionOptions}
 */
proto.Request.WaitForFunctionOptions.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setScript(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setOptions(value);
      break;
    case 4:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.WaitForFunctionOptions.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.WaitForFunctionOptions.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.WaitForFunctionOptions} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.WaitForFunctionOptions.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getScript();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getOptions();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      4,
      f
    );
  }
};


/**
 * optional string script = 1;
 * @return {string}
 */
proto.Request.WaitForFunctionOptions.prototype.getScript = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.WaitForFunctionOptions} returns this
 */
proto.Request.WaitForFunctionOptions.prototype.setScript = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string selector = 2;
 * @return {string}
 */
proto.Request.WaitForFunctionOptions.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.WaitForFunctionOptions} returns this
 */
proto.Request.WaitForFunctionOptions.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string options = 3;
 * @return {string}
 */
proto.Request.WaitForFunctionOptions.prototype.getOptions = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.WaitForFunctionOptions} returns this
 */
proto.Request.WaitForFunctionOptions.prototype.setOptions = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional bool strict = 4;
 * @return {boolean}
 */
proto.Request.WaitForFunctionOptions.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 4, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.WaitForFunctionOptions} returns this
 */
proto.Request.WaitForFunctionOptions.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 4, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.PlaywrightObject.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.PlaywrightObject.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.PlaywrightObject} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.PlaywrightObject.toObject = function(includeInstance, msg) {
  var f, obj = {
info: jspb.Message.getFieldWithDefault(msg, 1, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.PlaywrightObject}
 */
proto.Request.PlaywrightObject.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.PlaywrightObject;
  return proto.Request.PlaywrightObject.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.PlaywrightObject} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.PlaywrightObject}
 */
proto.Request.PlaywrightObject.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setInfo(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.PlaywrightObject.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.PlaywrightObject.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.PlaywrightObject} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.PlaywrightObject.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getInfo();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
};


/**
 * optional string info = 1;
 * @return {string}
 */
proto.Request.PlaywrightObject.prototype.getInfo = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.PlaywrightObject} returns this
 */
proto.Request.PlaywrightObject.prototype.setInfo = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Viewport.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Viewport.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Viewport} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Viewport.toObject = function(includeInstance, msg) {
  var f, obj = {
width: jspb.Message.getFieldWithDefault(msg, 1, 0),
height: jspb.Message.getFieldWithDefault(msg, 2, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Viewport}
 */
proto.Request.Viewport.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Viewport;
  return proto.Request.Viewport.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Viewport} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Viewport}
 */
proto.Request.Viewport.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setWidth(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setHeight(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Viewport.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Viewport.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Viewport} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Viewport.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getWidth();
  if (f !== 0) {
    writer.writeInt32(
      1,
      f
    );
  }
  f = message.getHeight();
  if (f !== 0) {
    writer.writeInt32(
      2,
      f
    );
  }
};


/**
 * optional int32 width = 1;
 * @return {number}
 */
proto.Request.Viewport.prototype.getWidth = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 1, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.Viewport} returns this
 */
proto.Request.Viewport.prototype.setWidth = function(value) {
  return jspb.Message.setProto3IntField(this, 1, value);
};


/**
 * optional int32 height = 2;
 * @return {number}
 */
proto.Request.Viewport.prototype.getHeight = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/**
 * @param {number} value
 * @return {!proto.Request.Viewport} returns this
 */
proto.Request.Viewport.prototype.setHeight = function(value) {
  return jspb.Message.setProto3IntField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.HttpRequest.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.HttpRequest.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.HttpRequest} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.HttpRequest.toObject = function(includeInstance, msg) {
  var f, obj = {
url: jspb.Message.getFieldWithDefault(msg, 1, ""),
method: jspb.Message.getFieldWithDefault(msg, 2, ""),
body: jspb.Message.getFieldWithDefault(msg, 3, ""),
headers: jspb.Message.getFieldWithDefault(msg, 4, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.HttpRequest}
 */
proto.Request.HttpRequest.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.HttpRequest;
  return proto.Request.HttpRequest.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.HttpRequest} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.HttpRequest}
 */
proto.Request.HttpRequest.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setUrl(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setMethod(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setBody(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setHeaders(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.HttpRequest.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.HttpRequest.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.HttpRequest} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.HttpRequest.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getUrl();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getMethod();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getBody();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getHeaders();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
};


/**
 * optional string url = 1;
 * @return {string}
 */
proto.Request.HttpRequest.prototype.getUrl = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.HttpRequest} returns this
 */
proto.Request.HttpRequest.prototype.setUrl = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string method = 2;
 * @return {string}
 */
proto.Request.HttpRequest.prototype.getMethod = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.HttpRequest} returns this
 */
proto.Request.HttpRequest.prototype.setMethod = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string body = 3;
 * @return {string}
 */
proto.Request.HttpRequest.prototype.getBody = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.HttpRequest} returns this
 */
proto.Request.HttpRequest.prototype.setBody = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional string headers = 4;
 * @return {string}
 */
proto.Request.HttpRequest.prototype.getHeaders = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.HttpRequest} returns this
 */
proto.Request.HttpRequest.prototype.setHeaders = function(value) {
  return jspb.Message.setProto3StringField(this, 4, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.HttpCapture.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.HttpCapture.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.HttpCapture} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.HttpCapture.toObject = function(includeInstance, msg) {
  var f, obj = {
urlorpredicate: jspb.Message.getFieldWithDefault(msg, 1, ""),
timeout: jspb.Message.getFloatingPointFieldWithDefault(msg, 2, 0.0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.HttpCapture}
 */
proto.Request.HttpCapture.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.HttpCapture;
  return proto.Request.HttpCapture.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.HttpCapture} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.HttpCapture}
 */
proto.Request.HttpCapture.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setUrlorpredicate(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setTimeout(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.HttpCapture.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.HttpCapture.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.HttpCapture} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.HttpCapture.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getUrlorpredicate();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getTimeout();
  if (f !== 0.0) {
    writer.writeFloat(
      2,
      f
    );
  }
};


/**
 * optional string urlOrPredicate = 1;
 * @return {string}
 */
proto.Request.HttpCapture.prototype.getUrlorpredicate = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.HttpCapture} returns this
 */
proto.Request.HttpCapture.prototype.setUrlorpredicate = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional float timeout = 2;
 * @return {number}
 */
proto.Request.HttpCapture.prototype.getTimeout = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 2, 0.0));
};


/**
 * @param {number} value
 * @return {!proto.Request.HttpCapture} returns this
 */
proto.Request.HttpCapture.prototype.setTimeout = function(value) {
  return jspb.Message.setProto3FloatField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Device.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Device.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Device} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Device.toObject = function(includeInstance, msg) {
  var f, obj = {
name: jspb.Message.getFieldWithDefault(msg, 1, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Device}
 */
proto.Request.Device.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Device;
  return proto.Request.Device.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Device} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Device}
 */
proto.Request.Device.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setName(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Device.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Device.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Device} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Device.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getName();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
};


/**
 * optional string name = 1;
 * @return {string}
 */
proto.Request.Device.prototype.getName = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.Device} returns this
 */
proto.Request.Device.prototype.setName = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.AlertAction.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.AlertAction.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.AlertAction} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.AlertAction.toObject = function(includeInstance, msg) {
  var f, obj = {
alertaction: jspb.Message.getFieldWithDefault(msg, 1, ""),
promptinput: jspb.Message.getFieldWithDefault(msg, 2, ""),
timeout: jspb.Message.getFloatingPointFieldWithDefault(msg, 3, 0.0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.AlertAction}
 */
proto.Request.AlertAction.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.AlertAction;
  return proto.Request.AlertAction.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.AlertAction} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.AlertAction}
 */
proto.Request.AlertAction.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setAlertaction(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setPromptinput(value);
      break;
    case 3:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setTimeout(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.AlertAction.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.AlertAction.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.AlertAction} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.AlertAction.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getAlertaction();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getPromptinput();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getTimeout();
  if (f !== 0.0) {
    writer.writeFloat(
      3,
      f
    );
  }
};


/**
 * optional string alertAction = 1;
 * @return {string}
 */
proto.Request.AlertAction.prototype.getAlertaction = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.AlertAction} returns this
 */
proto.Request.AlertAction.prototype.setAlertaction = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string promptInput = 2;
 * @return {string}
 */
proto.Request.AlertAction.prototype.getPromptinput = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.AlertAction} returns this
 */
proto.Request.AlertAction.prototype.setPromptinput = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional float timeout = 3;
 * @return {number}
 */
proto.Request.AlertAction.prototype.getTimeout = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 3, 0.0));
};


/**
 * @param {number} value
 * @return {!proto.Request.AlertAction} returns this
 */
proto.Request.AlertAction.prototype.setTimeout = function(value) {
  return jspb.Message.setProto3FloatField(this, 3, value);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.Request.AlertActions.repeatedFields_ = [1];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.AlertActions.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.AlertActions.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.AlertActions} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.AlertActions.toObject = function(includeInstance, msg) {
  var f, obj = {
itemsList: jspb.Message.toObjectList(msg.getItemsList(),
    proto.Request.AlertAction.toObject, includeInstance)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.AlertActions}
 */
proto.Request.AlertActions.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.AlertActions;
  return proto.Request.AlertActions.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.AlertActions} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.AlertActions}
 */
proto.Request.AlertActions.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new proto.Request.AlertAction;
      reader.readMessage(value,proto.Request.AlertAction.deserializeBinaryFromReader);
      msg.addItems(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.AlertActions.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.AlertActions.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.AlertActions} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.AlertActions.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getItemsList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      1,
      f,
      proto.Request.AlertAction.serializeBinaryToWriter
    );
  }
};


/**
 * repeated AlertAction items = 1;
 * @return {!Array<!proto.Request.AlertAction>}
 */
proto.Request.AlertActions.prototype.getItemsList = function() {
  return /** @type{!Array<!proto.Request.AlertAction>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.Request.AlertAction, 1));
};


/**
 * @param {!Array<!proto.Request.AlertAction>} value
 * @return {!proto.Request.AlertActions} returns this
*/
proto.Request.AlertActions.prototype.setItemsList = function(value) {
  return jspb.Message.setRepeatedWrapperField(this, 1, value);
};


/**
 * @param {!proto.Request.AlertAction=} opt_value
 * @param {number=} opt_index
 * @return {!proto.Request.AlertAction}
 */
proto.Request.AlertActions.prototype.addItems = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 1, opt_value, proto.Request.AlertAction, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.Request.AlertActions} returns this
 */
proto.Request.AlertActions.prototype.clearItemsList = function() {
  return this.setItemsList([]);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.Bool.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.Bool.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.Bool} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Bool.toObject = function(includeInstance, msg) {
  var f, obj = {
value: jspb.Message.getBooleanFieldWithDefault(msg, 1, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.Bool}
 */
proto.Request.Bool.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.Bool;
  return proto.Request.Bool.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.Bool} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.Bool}
 */
proto.Request.Bool.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setValue(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.Bool.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.Bool.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.Bool} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.Bool.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getValue();
  if (f) {
    writer.writeBool(
      1,
      f
    );
  }
};


/**
 * optional bool value = 1;
 * @return {boolean}
 */
proto.Request.Bool.prototype.getValue = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 1, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.Bool} returns this
 */
proto.Request.Bool.prototype.setValue = function(value) {
  return jspb.Message.setProto3BooleanField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.EvaluateAll.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.EvaluateAll.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.EvaluateAll} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.EvaluateAll.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
script: jspb.Message.getFieldWithDefault(msg, 2, ""),
arg: jspb.Message.getFieldWithDefault(msg, 3, ""),
allelements: jspb.Message.getBooleanFieldWithDefault(msg, 4, false),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 5, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.EvaluateAll}
 */
proto.Request.EvaluateAll.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.EvaluateAll;
  return proto.Request.EvaluateAll.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.EvaluateAll} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.EvaluateAll}
 */
proto.Request.EvaluateAll.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setScript(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setArg(value);
      break;
    case 4:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setAllelements(value);
      break;
    case 5:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.EvaluateAll.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.EvaluateAll.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.EvaluateAll} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.EvaluateAll.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getScript();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getArg();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getAllelements();
  if (f) {
    writer.writeBool(
      4,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      5,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.EvaluateAll.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.EvaluateAll} returns this
 */
proto.Request.EvaluateAll.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string script = 2;
 * @return {string}
 */
proto.Request.EvaluateAll.prototype.getScript = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.EvaluateAll} returns this
 */
proto.Request.EvaluateAll.prototype.setScript = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string arg = 3;
 * @return {string}
 */
proto.Request.EvaluateAll.prototype.getArg = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.EvaluateAll} returns this
 */
proto.Request.EvaluateAll.prototype.setArg = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional bool allElements = 4;
 * @return {boolean}
 */
proto.Request.EvaluateAll.prototype.getAllelements = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 4, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.EvaluateAll} returns this
 */
proto.Request.EvaluateAll.prototype.setAllelements = function(value) {
  return jspb.Message.setProto3BooleanField(this, 4, value);
};


/**
 * optional bool strict = 5;
 * @return {boolean}
 */
proto.Request.EvaluateAll.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 5, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.EvaluateAll} returns this
 */
proto.Request.EvaluateAll.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 5, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Request.ElementStyle.prototype.toObject = function(opt_includeInstance) {
  return proto.Request.ElementStyle.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Request.ElementStyle} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ElementStyle.toObject = function(includeInstance, msg) {
  var f, obj = {
selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
pseudo: jspb.Message.getFieldWithDefault(msg, 2, ""),
stylekey: jspb.Message.getFieldWithDefault(msg, 3, ""),
strict: jspb.Message.getBooleanFieldWithDefault(msg, 4, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Request.ElementStyle}
 */
proto.Request.ElementStyle.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Request.ElementStyle;
  return proto.Request.ElementStyle.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Request.ElementStyle} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Request.ElementStyle}
 */
proto.Request.ElementStyle.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setSelector(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setPseudo(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setStylekey(value);
      break;
    case 4:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setStrict(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Request.ElementStyle.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Request.ElementStyle.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Request.ElementStyle} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Request.ElementStyle.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSelector();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getPseudo();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getStylekey();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getStrict();
  if (f) {
    writer.writeBool(
      4,
      f
    );
  }
};


/**
 * optional string selector = 1;
 * @return {string}
 */
proto.Request.ElementStyle.prototype.getSelector = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementStyle} returns this
 */
proto.Request.ElementStyle.prototype.setSelector = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string pseudo = 2;
 * @return {string}
 */
proto.Request.ElementStyle.prototype.getPseudo = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementStyle} returns this
 */
proto.Request.ElementStyle.prototype.setPseudo = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string styleKey = 3;
 * @return {string}
 */
proto.Request.ElementStyle.prototype.getStylekey = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Request.ElementStyle} returns this
 */
proto.Request.ElementStyle.prototype.setStylekey = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional bool strict = 4;
 * @return {boolean}
 */
proto.Request.ElementStyle.prototype.getStrict = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 4, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Request.ElementStyle} returns this
 */
proto.Request.ElementStyle.prototype.setStrict = function(value) {
  return jspb.Message.setProto3BooleanField(this, 4, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Types.prototype.toObject = function(opt_includeInstance) {
  return proto.Types.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Types} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Types.toObject = function(includeInstance, msg) {
  var f, obj = {

  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Types}
 */
proto.Types.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Types;
  return proto.Types.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Types} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Types}
 */
proto.Types.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Types.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Types.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Types} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Types.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Types.SelectEntry.prototype.toObject = function(opt_includeInstance) {
  return proto.Types.SelectEntry.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Types.SelectEntry} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Types.SelectEntry.toObject = function(includeInstance, msg) {
  var f, obj = {
value: jspb.Message.getFieldWithDefault(msg, 2, ""),
label: jspb.Message.getFieldWithDefault(msg, 3, ""),
index: jspb.Message.getFieldWithDefault(msg, 4, 0),
selected: jspb.Message.getBooleanFieldWithDefault(msg, 5, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Types.SelectEntry}
 */
proto.Types.SelectEntry.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Types.SelectEntry;
  return proto.Types.SelectEntry.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Types.SelectEntry} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Types.SelectEntry}
 */
proto.Types.SelectEntry.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setValue(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setLabel(value);
      break;
    case 4:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setIndex(value);
      break;
    case 5:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setSelected(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Types.SelectEntry.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Types.SelectEntry.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Types.SelectEntry} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Types.SelectEntry.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getValue();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getLabel();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getIndex();
  if (f !== 0) {
    writer.writeInt32(
      4,
      f
    );
  }
  f = message.getSelected();
  if (f) {
    writer.writeBool(
      5,
      f
    );
  }
};


/**
 * optional string value = 2;
 * @return {string}
 */
proto.Types.SelectEntry.prototype.getValue = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Types.SelectEntry} returns this
 */
proto.Types.SelectEntry.prototype.setValue = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string label = 3;
 * @return {string}
 */
proto.Types.SelectEntry.prototype.getLabel = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Types.SelectEntry} returns this
 */
proto.Types.SelectEntry.prototype.setLabel = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional int32 index = 4;
 * @return {number}
 */
proto.Types.SelectEntry.prototype.getIndex = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 4, 0));
};


/**
 * @param {number} value
 * @return {!proto.Types.SelectEntry} returns this
 */
proto.Types.SelectEntry.prototype.setIndex = function(value) {
  return jspb.Message.setProto3IntField(this, 4, value);
};


/**
 * optional bool selected = 5;
 * @return {boolean}
 */
proto.Types.SelectEntry.prototype.getSelected = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 5, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Types.SelectEntry} returns this
 */
proto.Types.SelectEntry.prototype.setSelected = function(value) {
  return jspb.Message.setProto3BooleanField(this, 5, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.toObject = function(includeInstance, msg) {
  var f, obj = {

  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response}
 */
proto.Response.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response;
  return proto.Response.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response}
 */
proto.Response.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.Empty.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.Empty.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.Empty} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.Empty.toObject = function(includeInstance, msg) {
  var f, obj = {
log: jspb.Message.getFieldWithDefault(msg, 1, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.Empty}
 */
proto.Response.Empty.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.Empty;
  return proto.Response.Empty.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.Empty} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.Empty}
 */
proto.Response.Empty.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setLog(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.Empty.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.Empty.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.Empty} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.Empty.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getLog();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
};


/**
 * optional string log = 1;
 * @return {string}
 */
proto.Response.Empty.prototype.getLog = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.Empty} returns this
 */
proto.Response.Empty.prototype.setLog = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.String.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.String.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.String} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.String.toObject = function(includeInstance, msg) {
  var f, obj = {
log: jspb.Message.getFieldWithDefault(msg, 1, ""),
body: jspb.Message.getFieldWithDefault(msg, 2, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.String}
 */
proto.Response.String.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.String;
  return proto.Response.String.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.String} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.String}
 */
proto.Response.String.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setLog(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setBody(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.String.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.String.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.String} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.String.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getLog();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getBody();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
};


/**
 * optional string log = 1;
 * @return {string}
 */
proto.Response.String.prototype.getLog = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.String} returns this
 */
proto.Response.String.prototype.setLog = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string body = 2;
 * @return {string}
 */
proto.Response.String.prototype.getBody = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.String} returns this
 */
proto.Response.String.prototype.setBody = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.Response.ListString.repeatedFields_ = [1];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.ListString.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.ListString.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.ListString} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.ListString.toObject = function(includeInstance, msg) {
  var f, obj = {
itemsList: (f = jspb.Message.getRepeatedField(msg, 1)) == null ? undefined : f
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.ListString}
 */
proto.Response.ListString.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.ListString;
  return proto.Response.ListString.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.ListString} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.ListString}
 */
proto.Response.ListString.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.addItems(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.ListString.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.ListString.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.ListString} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.ListString.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getItemsList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      1,
      f
    );
  }
};


/**
 * repeated string items = 1;
 * @return {!Array<string>}
 */
proto.Response.ListString.prototype.getItemsList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 1));
};


/**
 * @param {!Array<string>} value
 * @return {!proto.Response.ListString} returns this
 */
proto.Response.ListString.prototype.setItemsList = function(value) {
  return jspb.Message.setField(this, 1, value || []);
};


/**
 * @param {string} value
 * @param {number=} opt_index
 * @return {!proto.Response.ListString} returns this
 */
proto.Response.ListString.prototype.addItems = function(value, opt_index) {
  return jspb.Message.addToRepeatedField(this, 1, value, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.Response.ListString} returns this
 */
proto.Response.ListString.prototype.clearItemsList = function() {
  return this.setItemsList([]);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.Response.Keywords.repeatedFields_ = [2,3,4];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.Keywords.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.Keywords.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.Keywords} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.Keywords.toObject = function(includeInstance, msg) {
  var f, obj = {
log: jspb.Message.getFieldWithDefault(msg, 1, ""),
keywordsList: (f = jspb.Message.getRepeatedField(msg, 2)) == null ? undefined : f,
keyworddocumentationsList: (f = jspb.Message.getRepeatedField(msg, 3)) == null ? undefined : f,
keywordargumentsList: (f = jspb.Message.getRepeatedField(msg, 4)) == null ? undefined : f
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.Keywords}
 */
proto.Response.Keywords.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.Keywords;
  return proto.Response.Keywords.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.Keywords} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.Keywords}
 */
proto.Response.Keywords.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setLog(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.addKeywords(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.addKeyworddocumentations(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.addKeywordarguments(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.Keywords.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.Keywords.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.Keywords} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.Keywords.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getLog();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getKeywordsList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      2,
      f
    );
  }
  f = message.getKeyworddocumentationsList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      3,
      f
    );
  }
  f = message.getKeywordargumentsList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      4,
      f
    );
  }
};


/**
 * optional string log = 1;
 * @return {string}
 */
proto.Response.Keywords.prototype.getLog = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.Keywords} returns this
 */
proto.Response.Keywords.prototype.setLog = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * repeated string keywords = 2;
 * @return {!Array<string>}
 */
proto.Response.Keywords.prototype.getKeywordsList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 2));
};


/**
 * @param {!Array<string>} value
 * @return {!proto.Response.Keywords} returns this
 */
proto.Response.Keywords.prototype.setKeywordsList = function(value) {
  return jspb.Message.setField(this, 2, value || []);
};


/**
 * @param {string} value
 * @param {number=} opt_index
 * @return {!proto.Response.Keywords} returns this
 */
proto.Response.Keywords.prototype.addKeywords = function(value, opt_index) {
  return jspb.Message.addToRepeatedField(this, 2, value, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.Response.Keywords} returns this
 */
proto.Response.Keywords.prototype.clearKeywordsList = function() {
  return this.setKeywordsList([]);
};


/**
 * repeated string keywordDocumentations = 3;
 * @return {!Array<string>}
 */
proto.Response.Keywords.prototype.getKeyworddocumentationsList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 3));
};


/**
 * @param {!Array<string>} value
 * @return {!proto.Response.Keywords} returns this
 */
proto.Response.Keywords.prototype.setKeyworddocumentationsList = function(value) {
  return jspb.Message.setField(this, 3, value || []);
};


/**
 * @param {string} value
 * @param {number=} opt_index
 * @return {!proto.Response.Keywords} returns this
 */
proto.Response.Keywords.prototype.addKeyworddocumentations = function(value, opt_index) {
  return jspb.Message.addToRepeatedField(this, 3, value, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.Response.Keywords} returns this
 */
proto.Response.Keywords.prototype.clearKeyworddocumentationsList = function() {
  return this.setKeyworddocumentationsList([]);
};


/**
 * repeated string keywordArguments = 4;
 * @return {!Array<string>}
 */
proto.Response.Keywords.prototype.getKeywordargumentsList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 4));
};


/**
 * @param {!Array<string>} value
 * @return {!proto.Response.Keywords} returns this
 */
proto.Response.Keywords.prototype.setKeywordargumentsList = function(value) {
  return jspb.Message.setField(this, 4, value || []);
};


/**
 * @param {string} value
 * @param {number=} opt_index
 * @return {!proto.Response.Keywords} returns this
 */
proto.Response.Keywords.prototype.addKeywordarguments = function(value, opt_index) {
  return jspb.Message.addToRepeatedField(this, 4, value, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.Response.Keywords} returns this
 */
proto.Response.Keywords.prototype.clearKeywordargumentsList = function() {
  return this.setKeywordargumentsList([]);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.Bool.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.Bool.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.Bool} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.Bool.toObject = function(includeInstance, msg) {
  var f, obj = {
log: jspb.Message.getFieldWithDefault(msg, 1, ""),
body: jspb.Message.getBooleanFieldWithDefault(msg, 2, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.Bool}
 */
proto.Response.Bool.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.Bool;
  return proto.Response.Bool.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.Bool} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.Bool}
 */
proto.Response.Bool.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setLog(value);
      break;
    case 2:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setBody(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.Bool.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.Bool.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.Bool} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.Bool.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getLog();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getBody();
  if (f) {
    writer.writeBool(
      2,
      f
    );
  }
};


/**
 * optional string log = 1;
 * @return {string}
 */
proto.Response.Bool.prototype.getLog = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.Bool} returns this
 */
proto.Response.Bool.prototype.setLog = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional bool body = 2;
 * @return {boolean}
 */
proto.Response.Bool.prototype.getBody = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 2, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Response.Bool} returns this
 */
proto.Response.Bool.prototype.setBody = function(value) {
  return jspb.Message.setProto3BooleanField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.Int.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.Int.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.Int} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.Int.toObject = function(includeInstance, msg) {
  var f, obj = {
log: jspb.Message.getFieldWithDefault(msg, 1, ""),
body: jspb.Message.getFieldWithDefault(msg, 2, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.Int}
 */
proto.Response.Int.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.Int;
  return proto.Response.Int.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.Int} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.Int}
 */
proto.Response.Int.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setLog(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setBody(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.Int.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.Int.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.Int} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.Int.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getLog();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getBody();
  if (f !== 0) {
    writer.writeInt32(
      2,
      f
    );
  }
};


/**
 * optional string log = 1;
 * @return {string}
 */
proto.Response.Int.prototype.getLog = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.Int} returns this
 */
proto.Response.Int.prototype.setLog = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional int32 body = 2;
 * @return {number}
 */
proto.Response.Int.prototype.getBody = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/**
 * @param {number} value
 * @return {!proto.Response.Int} returns this
 */
proto.Response.Int.prototype.setBody = function(value) {
  return jspb.Message.setProto3IntField(this, 2, value);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.Response.Select.repeatedFields_ = [1];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.Select.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.Select.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.Select} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.Select.toObject = function(includeInstance, msg) {
  var f, obj = {
entryList: jspb.Message.toObjectList(msg.getEntryList(),
    proto.Types.SelectEntry.toObject, includeInstance)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.Select}
 */
proto.Response.Select.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.Select;
  return proto.Response.Select.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.Select} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.Select}
 */
proto.Response.Select.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new proto.Types.SelectEntry;
      reader.readMessage(value,proto.Types.SelectEntry.deserializeBinaryFromReader);
      msg.addEntry(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.Select.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.Select.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.Select} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.Select.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getEntryList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      1,
      f,
      proto.Types.SelectEntry.serializeBinaryToWriter
    );
  }
};


/**
 * repeated Types.SelectEntry entry = 1;
 * @return {!Array<!proto.Types.SelectEntry>}
 */
proto.Response.Select.prototype.getEntryList = function() {
  return /** @type{!Array<!proto.Types.SelectEntry>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.Types.SelectEntry, 1));
};


/**
 * @param {!Array<!proto.Types.SelectEntry>} value
 * @return {!proto.Response.Select} returns this
*/
proto.Response.Select.prototype.setEntryList = function(value) {
  return jspb.Message.setRepeatedWrapperField(this, 1, value);
};


/**
 * @param {!proto.Types.SelectEntry=} opt_value
 * @param {number=} opt_index
 * @return {!proto.Types.SelectEntry}
 */
proto.Response.Select.prototype.addEntry = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 1, opt_value, proto.Types.SelectEntry, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.Response.Select} returns this
 */
proto.Response.Select.prototype.clearEntryList = function() {
  return this.setEntryList([]);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.Json.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.Json.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.Json} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.Json.toObject = function(includeInstance, msg) {
  var f, obj = {
log: jspb.Message.getFieldWithDefault(msg, 1, ""),
json: jspb.Message.getFieldWithDefault(msg, 2, ""),
bodypart: jspb.Message.getFieldWithDefault(msg, 3, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.Json}
 */
proto.Response.Json.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.Json;
  return proto.Response.Json.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.Json} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.Json}
 */
proto.Response.Json.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setLog(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setJson(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setBodypart(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.Json.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.Json.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.Json} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.Json.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getLog();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getJson();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getBodypart();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
};


/**
 * optional string log = 1;
 * @return {string}
 */
proto.Response.Json.prototype.getLog = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.Json} returns this
 */
proto.Response.Json.prototype.setLog = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string json = 2;
 * @return {string}
 */
proto.Response.Json.prototype.getJson = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.Json} returns this
 */
proto.Response.Json.prototype.setJson = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string bodyPart = 3;
 * @return {string}
 */
proto.Response.Json.prototype.getBodypart = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.Json} returns this
 */
proto.Response.Json.prototype.setBodypart = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.JavascriptExecutionResult.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.JavascriptExecutionResult.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.JavascriptExecutionResult} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.JavascriptExecutionResult.toObject = function(includeInstance, msg) {
  var f, obj = {
log: jspb.Message.getFieldWithDefault(msg, 1, ""),
result: jspb.Message.getFieldWithDefault(msg, 2, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.JavascriptExecutionResult}
 */
proto.Response.JavascriptExecutionResult.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.JavascriptExecutionResult;
  return proto.Response.JavascriptExecutionResult.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.JavascriptExecutionResult} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.JavascriptExecutionResult}
 */
proto.Response.JavascriptExecutionResult.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setLog(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setResult(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.JavascriptExecutionResult.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.JavascriptExecutionResult.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.JavascriptExecutionResult} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.JavascriptExecutionResult.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getLog();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getResult();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
};


/**
 * optional string log = 1;
 * @return {string}
 */
proto.Response.JavascriptExecutionResult.prototype.getLog = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.JavascriptExecutionResult} returns this
 */
proto.Response.JavascriptExecutionResult.prototype.setLog = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string result = 2;
 * @return {string}
 */
proto.Response.JavascriptExecutionResult.prototype.getResult = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.JavascriptExecutionResult} returns this
 */
proto.Response.JavascriptExecutionResult.prototype.setResult = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.NewContextResponse.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.NewContextResponse.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.NewContextResponse} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.NewContextResponse.toObject = function(includeInstance, msg) {
  var f, obj = {
id: jspb.Message.getFieldWithDefault(msg, 1, ""),
log: jspb.Message.getFieldWithDefault(msg, 2, ""),
contextoptions: jspb.Message.getFieldWithDefault(msg, 3, ""),
newbrowser: jspb.Message.getBooleanFieldWithDefault(msg, 4, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.NewContextResponse}
 */
proto.Response.NewContextResponse.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.NewContextResponse;
  return proto.Response.NewContextResponse.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.NewContextResponse} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.NewContextResponse}
 */
proto.Response.NewContextResponse.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setId(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setLog(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setContextoptions(value);
      break;
    case 4:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setNewbrowser(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.NewContextResponse.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.NewContextResponse.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.NewContextResponse} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.NewContextResponse.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getId();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getLog();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getContextoptions();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getNewbrowser();
  if (f) {
    writer.writeBool(
      4,
      f
    );
  }
};


/**
 * optional string id = 1;
 * @return {string}
 */
proto.Response.NewContextResponse.prototype.getId = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.NewContextResponse} returns this
 */
proto.Response.NewContextResponse.prototype.setId = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string log = 2;
 * @return {string}
 */
proto.Response.NewContextResponse.prototype.getLog = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.NewContextResponse} returns this
 */
proto.Response.NewContextResponse.prototype.setLog = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string contextOptions = 3;
 * @return {string}
 */
proto.Response.NewContextResponse.prototype.getContextoptions = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.NewContextResponse} returns this
 */
proto.Response.NewContextResponse.prototype.setContextoptions = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional bool newBrowser = 4;
 * @return {boolean}
 */
proto.Response.NewContextResponse.prototype.getNewbrowser = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 4, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Response.NewContextResponse} returns this
 */
proto.Response.NewContextResponse.prototype.setNewbrowser = function(value) {
  return jspb.Message.setProto3BooleanField(this, 4, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.NewPersistentContextResponse.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.NewPersistentContextResponse.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.NewPersistentContextResponse} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.NewPersistentContextResponse.toObject = function(includeInstance, msg) {
  var f, obj = {
id: jspb.Message.getFieldWithDefault(msg, 1, ""),
log: jspb.Message.getFieldWithDefault(msg, 2, ""),
contextoptions: jspb.Message.getFieldWithDefault(msg, 3, ""),
newbrowser: jspb.Message.getBooleanFieldWithDefault(msg, 4, false),
video: jspb.Message.getFieldWithDefault(msg, 5, ""),
pageid: jspb.Message.getFieldWithDefault(msg, 6, ""),
browserid: jspb.Message.getFieldWithDefault(msg, 7, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.NewPersistentContextResponse}
 */
proto.Response.NewPersistentContextResponse.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.NewPersistentContextResponse;
  return proto.Response.NewPersistentContextResponse.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.NewPersistentContextResponse} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.NewPersistentContextResponse}
 */
proto.Response.NewPersistentContextResponse.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setId(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setLog(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setContextoptions(value);
      break;
    case 4:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setNewbrowser(value);
      break;
    case 5:
      var value = /** @type {string} */ (reader.readString());
      msg.setVideo(value);
      break;
    case 6:
      var value = /** @type {string} */ (reader.readString());
      msg.setPageid(value);
      break;
    case 7:
      var value = /** @type {string} */ (reader.readString());
      msg.setBrowserid(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.NewPersistentContextResponse.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.NewPersistentContextResponse.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.NewPersistentContextResponse} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.NewPersistentContextResponse.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getId();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getLog();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getContextoptions();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getNewbrowser();
  if (f) {
    writer.writeBool(
      4,
      f
    );
  }
  f = message.getVideo();
  if (f.length > 0) {
    writer.writeString(
      5,
      f
    );
  }
  f = message.getPageid();
  if (f.length > 0) {
    writer.writeString(
      6,
      f
    );
  }
  f = message.getBrowserid();
  if (f.length > 0) {
    writer.writeString(
      7,
      f
    );
  }
};


/**
 * optional string id = 1;
 * @return {string}
 */
proto.Response.NewPersistentContextResponse.prototype.getId = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.NewPersistentContextResponse} returns this
 */
proto.Response.NewPersistentContextResponse.prototype.setId = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string log = 2;
 * @return {string}
 */
proto.Response.NewPersistentContextResponse.prototype.getLog = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.NewPersistentContextResponse} returns this
 */
proto.Response.NewPersistentContextResponse.prototype.setLog = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string contextOptions = 3;
 * @return {string}
 */
proto.Response.NewPersistentContextResponse.prototype.getContextoptions = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.NewPersistentContextResponse} returns this
 */
proto.Response.NewPersistentContextResponse.prototype.setContextoptions = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional bool newBrowser = 4;
 * @return {boolean}
 */
proto.Response.NewPersistentContextResponse.prototype.getNewbrowser = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 4, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Response.NewPersistentContextResponse} returns this
 */
proto.Response.NewPersistentContextResponse.prototype.setNewbrowser = function(value) {
  return jspb.Message.setProto3BooleanField(this, 4, value);
};


/**
 * optional string video = 5;
 * @return {string}
 */
proto.Response.NewPersistentContextResponse.prototype.getVideo = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 5, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.NewPersistentContextResponse} returns this
 */
proto.Response.NewPersistentContextResponse.prototype.setVideo = function(value) {
  return jspb.Message.setProto3StringField(this, 5, value);
};


/**
 * optional string pageId = 6;
 * @return {string}
 */
proto.Response.NewPersistentContextResponse.prototype.getPageid = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 6, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.NewPersistentContextResponse} returns this
 */
proto.Response.NewPersistentContextResponse.prototype.setPageid = function(value) {
  return jspb.Message.setProto3StringField(this, 6, value);
};


/**
 * optional string browserId = 7;
 * @return {string}
 */
proto.Response.NewPersistentContextResponse.prototype.getBrowserid = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 7, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.NewPersistentContextResponse} returns this
 */
proto.Response.NewPersistentContextResponse.prototype.setBrowserid = function(value) {
  return jspb.Message.setProto3StringField(this, 7, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.NewPageResponse.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.NewPageResponse.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.NewPageResponse} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.NewPageResponse.toObject = function(includeInstance, msg) {
  var f, obj = {
log: jspb.Message.getFieldWithDefault(msg, 1, ""),
body: jspb.Message.getFieldWithDefault(msg, 2, ""),
video: jspb.Message.getFieldWithDefault(msg, 3, ""),
newbrowser: jspb.Message.getBooleanFieldWithDefault(msg, 4, false),
newcontext: jspb.Message.getBooleanFieldWithDefault(msg, 5, false)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.NewPageResponse}
 */
proto.Response.NewPageResponse.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.NewPageResponse;
  return proto.Response.NewPageResponse.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.NewPageResponse} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.NewPageResponse}
 */
proto.Response.NewPageResponse.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setLog(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setBody(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setVideo(value);
      break;
    case 4:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setNewbrowser(value);
      break;
    case 5:
      var value = /** @type {boolean} */ (reader.readBool());
      msg.setNewcontext(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.NewPageResponse.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.NewPageResponse.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.NewPageResponse} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.NewPageResponse.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getLog();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getBody();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getVideo();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getNewbrowser();
  if (f) {
    writer.writeBool(
      4,
      f
    );
  }
  f = message.getNewcontext();
  if (f) {
    writer.writeBool(
      5,
      f
    );
  }
};


/**
 * optional string log = 1;
 * @return {string}
 */
proto.Response.NewPageResponse.prototype.getLog = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.NewPageResponse} returns this
 */
proto.Response.NewPageResponse.prototype.setLog = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string body = 2;
 * @return {string}
 */
proto.Response.NewPageResponse.prototype.getBody = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.NewPageResponse} returns this
 */
proto.Response.NewPageResponse.prototype.setBody = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string video = 3;
 * @return {string}
 */
proto.Response.NewPageResponse.prototype.getVideo = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.NewPageResponse} returns this
 */
proto.Response.NewPageResponse.prototype.setVideo = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional bool newBrowser = 4;
 * @return {boolean}
 */
proto.Response.NewPageResponse.prototype.getNewbrowser = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 4, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Response.NewPageResponse} returns this
 */
proto.Response.NewPageResponse.prototype.setNewbrowser = function(value) {
  return jspb.Message.setProto3BooleanField(this, 4, value);
};


/**
 * optional bool newContext = 5;
 * @return {boolean}
 */
proto.Response.NewPageResponse.prototype.getNewcontext = function() {
  return /** @type {boolean} */ (jspb.Message.getBooleanFieldWithDefault(this, 5, false));
};


/**
 * @param {boolean} value
 * @return {!proto.Response.NewPageResponse} returns this
 */
proto.Response.NewPageResponse.prototype.setNewcontext = function(value) {
  return jspb.Message.setProto3BooleanField(this, 5, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.Response.PageReportResponse.prototype.toObject = function(opt_includeInstance) {
  return proto.Response.PageReportResponse.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.Response.PageReportResponse} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.PageReportResponse.toObject = function(includeInstance, msg) {
  var f, obj = {
log: jspb.Message.getFieldWithDefault(msg, 1, ""),
errors: jspb.Message.getFieldWithDefault(msg, 2, ""),
console: jspb.Message.getFieldWithDefault(msg, 3, ""),
pageid: jspb.Message.getFieldWithDefault(msg, 4, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.Response.PageReportResponse}
 */
proto.Response.PageReportResponse.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.Response.PageReportResponse;
  return proto.Response.PageReportResponse.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.Response.PageReportResponse} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.Response.PageReportResponse}
 */
proto.Response.PageReportResponse.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setLog(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setErrors(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setConsole(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setPageid(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.Response.PageReportResponse.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.Response.PageReportResponse.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.Response.PageReportResponse} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.Response.PageReportResponse.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getLog();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getErrors();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getConsole();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getPageid();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
};


/**
 * optional string log = 1;
 * @return {string}
 */
proto.Response.PageReportResponse.prototype.getLog = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.PageReportResponse} returns this
 */
proto.Response.PageReportResponse.prototype.setLog = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string errors = 2;
 * @return {string}
 */
proto.Response.PageReportResponse.prototype.getErrors = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.PageReportResponse} returns this
 */
proto.Response.PageReportResponse.prototype.setErrors = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional string console = 3;
 * @return {string}
 */
proto.Response.PageReportResponse.prototype.getConsole = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.PageReportResponse} returns this
 */
proto.Response.PageReportResponse.prototype.setConsole = function(value) {
  return jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional string pageId = 4;
 * @return {string}
 */
proto.Response.PageReportResponse.prototype.getPageid = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/**
 * @param {string} value
 * @return {!proto.Response.PageReportResponse} returns this
 */
proto.Response.PageReportResponse.prototype.setPageid = function(value) {
  return jspb.Message.setProto3StringField(this, 4, value);
};


goog.object.extend(exports, proto);
