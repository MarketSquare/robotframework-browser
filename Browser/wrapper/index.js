"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __commonJS = (cb, mod) => function __require() {
  return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __decorateClass = (decorators, target, key, kind) => {
  var result = kind > 1 ? void 0 : kind ? __getOwnPropDesc(target, key) : target;
  for (var i = decorators.length - 1, decorator; i >= 0; i--)
    if (decorator = decorators[i])
      result = (kind ? decorator(target, key, result) : decorator(result)) || result;
  if (kind && result) __defProp(target, key, result);
  return result;
};

// node/playwright-wrapper/generated/playwright_pb.js
var require_playwright_pb = __commonJS({
  "node/playwright-wrapper/generated/playwright_pb.js"(exports2) {
    "use strict";
    var jspb = require("google-protobuf");
    var goog = jspb;
    var global = typeof globalThis !== "undefined" && globalThis || typeof window !== "undefined" && window || typeof global !== "undefined" && global || typeof self !== "undefined" && self || (function() {
      return this;
    }).call(null) || Function("return this")();
    goog.exportSymbol("proto.Request", null, global);
    goog.exportSymbol("proto.Request.AlertAction", null, global);
    goog.exportSymbol("proto.Request.AlertActions", null, global);
    goog.exportSymbol("proto.Request.AriaSnapShot", null, global);
    goog.exportSymbol("proto.Request.Bool", null, global);
    goog.exportSymbol("proto.Request.Browser", null, global);
    goog.exportSymbol("proto.Request.ClearText", null, global);
    goog.exportSymbol("proto.Request.ClockAdvance", null, global);
    goog.exportSymbol("proto.Request.ClockSetTime", null, global);
    goog.exportSymbol("proto.Request.ClosePage", null, global);
    goog.exportSymbol("proto.Request.ConnectBrowser", null, global);
    goog.exportSymbol("proto.Request.Context", null, global);
    goog.exportSymbol("proto.Request.CoverageMerge", null, global);
    goog.exportSymbol("proto.Request.CoverageStart", null, global);
    goog.exportSymbol("proto.Request.Device", null, global);
    goog.exportSymbol("proto.Request.DownloadID", null, global);
    goog.exportSymbol("proto.Request.DownloadOptions", null, global);
    goog.exportSymbol("proto.Request.ElectronLaunch", null, global);
    goog.exportSymbol("proto.Request.ElementProperty", null, global);
    goog.exportSymbol("proto.Request.ElementSelector", null, global);
    goog.exportSymbol("proto.Request.ElementSelectorWithDuration", null, global);
    goog.exportSymbol("proto.Request.ElementSelectorWithOptions", null, global);
    goog.exportSymbol("proto.Request.ElementStyle", null, global);
    goog.exportSymbol("proto.Request.Empty", null, global);
    goog.exportSymbol("proto.Request.EmulateMedia", null, global);
    goog.exportSymbol("proto.Request.EvaluateAll", null, global);
    goog.exportSymbol("proto.Request.FileBySelector", null, global);
    goog.exportSymbol("proto.Request.FilePath", null, global);
    goog.exportSymbol("proto.Request.FillText", null, global);
    goog.exportSymbol("proto.Request.GetByOptions", null, global);
    goog.exportSymbol("proto.Request.HttpCapture", null, global);
    goog.exportSymbol("proto.Request.HttpRequest", null, global);
    goog.exportSymbol("proto.Request.IdWithTimeout", null, global);
    goog.exportSymbol("proto.Request.Index", null, global);
    goog.exportSymbol("proto.Request.Json", null, global);
    goog.exportSymbol("proto.Request.KeyboardInputOptions", null, global);
    goog.exportSymbol("proto.Request.KeyboardKeypress", null, global);
    goog.exportSymbol("proto.Request.KeywordCall", null, global);
    goog.exportSymbol("proto.Request.Label", null, global);
    goog.exportSymbol("proto.Request.LocatorHandlerAddCustom", null, global);
    goog.exportSymbol("proto.Request.LocatorHandlerAddCustomAction", null, global);
    goog.exportSymbol("proto.Request.LocatorHandlerRemove", null, global);
    goog.exportSymbol("proto.Request.MouseButtonOptions", null, global);
    goog.exportSymbol("proto.Request.MouseWheel", null, global);
    goog.exportSymbol("proto.Request.PageLoadState", null, global);
    goog.exportSymbol("proto.Request.Pdf", null, global);
    goog.exportSymbol("proto.Request.Permissions", null, global);
    goog.exportSymbol("proto.Request.PersistentContext", null, global);
    goog.exportSymbol("proto.Request.PlaywrightObject", null, global);
    goog.exportSymbol("proto.Request.PressKeys", null, global);
    goog.exportSymbol("proto.Request.ScreenshotOptions", null, global);
    goog.exportSymbol("proto.Request.SelectElementSelector", null, global);
    goog.exportSymbol("proto.Request.StyleTag", null, global);
    goog.exportSymbol("proto.Request.TextInput", null, global);
    goog.exportSymbol("proto.Request.Timeout", null, global);
    goog.exportSymbol("proto.Request.TraceGroup", null, global);
    goog.exportSymbol("proto.Request.TypeText", null, global);
    goog.exportSymbol("proto.Request.Url", null, global);
    goog.exportSymbol("proto.Request.UrlOptions", null, global);
    goog.exportSymbol("proto.Request.Viewport", null, global);
    goog.exportSymbol("proto.Request.WaitForFunctionOptions", null, global);
    goog.exportSymbol("proto.Response", null, global);
    goog.exportSymbol("proto.Response.Bool", null, global);
    goog.exportSymbol("proto.Response.Empty", null, global);
    goog.exportSymbol("proto.Response.Int", null, global);
    goog.exportSymbol("proto.Response.JavascriptExecutionResult", null, global);
    goog.exportSymbol("proto.Response.Json", null, global);
    goog.exportSymbol("proto.Response.Keywords", null, global);
    goog.exportSymbol("proto.Response.ListString", null, global);
    goog.exportSymbol("proto.Response.NewContextResponse", null, global);
    goog.exportSymbol("proto.Response.NewPageResponse", null, global);
    goog.exportSymbol("proto.Response.NewPersistentContextResponse", null, global);
    goog.exportSymbol("proto.Response.PageReportResponse", null, global);
    goog.exportSymbol("proto.Response.Select", null, global);
    goog.exportSymbol("proto.Response.String", null, global);
    goog.exportSymbol("proto.Types", null, global);
    goog.exportSymbol("proto.Types.SelectEntry", null, global);
    proto.Request = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.displayName = "proto.Request";
    }
    proto.Request.Empty = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.Empty, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Empty.displayName = "proto.Request.Empty";
    }
    proto.Request.AriaSnapShot = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.AriaSnapShot, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.AriaSnapShot.displayName = "proto.Request.AriaSnapShot";
    }
    proto.Request.ClosePage = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.ClosePage, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.ClosePage.displayName = "proto.Request.ClosePage";
    }
    proto.Request.ClockSetTime = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.ClockSetTime, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.ClockSetTime.displayName = "proto.Request.ClockSetTime";
    }
    proto.Request.ClockAdvance = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.ClockAdvance, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.ClockAdvance.displayName = "proto.Request.ClockAdvance";
    }
    proto.Request.CoverageStart = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.CoverageStart, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.CoverageStart.displayName = "proto.Request.CoverageStart";
    }
    proto.Request.CoverageMerge = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.CoverageMerge.repeatedFields_, null);
    };
    goog.inherits(proto.Request.CoverageMerge, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.CoverageMerge.displayName = "proto.Request.CoverageMerge";
    }
    proto.Request.TraceGroup = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.TraceGroup, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.TraceGroup.displayName = "proto.Request.TraceGroup";
    }
    proto.Request.Label = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.Label, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Label.displayName = "proto.Request.Label";
    }
    proto.Request.GetByOptions = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.GetByOptions, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.GetByOptions.displayName = "proto.Request.GetByOptions";
    }
    proto.Request.Pdf = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.Pdf, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Pdf.displayName = "proto.Request.Pdf";
    }
    proto.Request.EmulateMedia = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.EmulateMedia, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.EmulateMedia.displayName = "proto.Request.EmulateMedia";
    }
    proto.Request.ScreenshotOptions = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.ScreenshotOptions, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.ScreenshotOptions.displayName = "proto.Request.ScreenshotOptions";
    }
    proto.Request.KeywordCall = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.KeywordCall, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.KeywordCall.displayName = "proto.Request.KeywordCall";
    }
    proto.Request.FilePath = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.FilePath, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.FilePath.displayName = "proto.Request.FilePath";
    }
    proto.Request.FileBySelector = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.FileBySelector.repeatedFields_, null);
    };
    goog.inherits(proto.Request.FileBySelector, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.FileBySelector.displayName = "proto.Request.FileBySelector";
    }
    proto.Request.LocatorHandlerAddCustom = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.LocatorHandlerAddCustom.repeatedFields_, null);
    };
    goog.inherits(proto.Request.LocatorHandlerAddCustom, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.LocatorHandlerAddCustom.displayName = "proto.Request.LocatorHandlerAddCustom";
    }
    proto.Request.LocatorHandlerAddCustomAction = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.LocatorHandlerAddCustomAction, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.LocatorHandlerAddCustomAction.displayName = "proto.Request.LocatorHandlerAddCustomAction";
    }
    proto.Request.LocatorHandlerRemove = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.LocatorHandlerRemove, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.LocatorHandlerRemove.displayName = "proto.Request.LocatorHandlerRemove";
    }
    proto.Request.Json = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.Json, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Json.displayName = "proto.Request.Json";
    }
    proto.Request.MouseButtonOptions = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.MouseButtonOptions, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.MouseButtonOptions.displayName = "proto.Request.MouseButtonOptions";
    }
    proto.Request.MouseWheel = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.MouseWheel, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.MouseWheel.displayName = "proto.Request.MouseWheel";
    }
    proto.Request.KeyboardKeypress = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.KeyboardKeypress, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.KeyboardKeypress.displayName = "proto.Request.KeyboardKeypress";
    }
    proto.Request.KeyboardInputOptions = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.KeyboardInputOptions, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.KeyboardInputOptions.displayName = "proto.Request.KeyboardInputOptions";
    }
    proto.Request.Browser = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.Browser, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Browser.displayName = "proto.Request.Browser";
    }
    proto.Request.Context = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.Context, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Context.displayName = "proto.Request.Context";
    }
    proto.Request.PersistentContext = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.PersistentContext, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.PersistentContext.displayName = "proto.Request.PersistentContext";
    }
    proto.Request.ElectronLaunch = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.ElectronLaunch.repeatedFields_, null);
    };
    goog.inherits(proto.Request.ElectronLaunch, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.ElectronLaunch.displayName = "proto.Request.ElectronLaunch";
    }
    proto.Request.Permissions = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.Permissions.repeatedFields_, null);
    };
    goog.inherits(proto.Request.Permissions, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Permissions.displayName = "proto.Request.Permissions";
    }
    proto.Request.Url = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.Url, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Url.displayName = "proto.Request.Url";
    }
    proto.Request.DownloadOptions = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.DownloadOptions, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.DownloadOptions.displayName = "proto.Request.DownloadOptions";
    }
    proto.Request.DownloadID = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.DownloadID, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.DownloadID.displayName = "proto.Request.DownloadID";
    }
    proto.Request.UrlOptions = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.UrlOptions, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.UrlOptions.displayName = "proto.Request.UrlOptions";
    }
    proto.Request.PageLoadState = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.PageLoadState, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.PageLoadState.displayName = "proto.Request.PageLoadState";
    }
    proto.Request.ConnectBrowser = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.ConnectBrowser, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.ConnectBrowser.displayName = "proto.Request.ConnectBrowser";
    }
    proto.Request.TextInput = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.TextInput, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.TextInput.displayName = "proto.Request.TextInput";
    }
    proto.Request.ElementProperty = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.ElementProperty, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.ElementProperty.displayName = "proto.Request.ElementProperty";
    }
    proto.Request.TypeText = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.TypeText, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.TypeText.displayName = "proto.Request.TypeText";
    }
    proto.Request.FillText = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.FillText, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.FillText.displayName = "proto.Request.FillText";
    }
    proto.Request.ClearText = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.ClearText, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.ClearText.displayName = "proto.Request.ClearText";
    }
    proto.Request.PressKeys = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.PressKeys.repeatedFields_, null);
    };
    goog.inherits(proto.Request.PressKeys, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.PressKeys.displayName = "proto.Request.PressKeys";
    }
    proto.Request.ElementSelector = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.ElementSelector, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.ElementSelector.displayName = "proto.Request.ElementSelector";
    }
    proto.Request.Timeout = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.Timeout, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Timeout.displayName = "proto.Request.Timeout";
    }
    proto.Request.Index = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.Index, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Index.displayName = "proto.Request.Index";
    }
    proto.Request.IdWithTimeout = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.IdWithTimeout, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.IdWithTimeout.displayName = "proto.Request.IdWithTimeout";
    }
    proto.Request.StyleTag = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.StyleTag, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.StyleTag.displayName = "proto.Request.StyleTag";
    }
    proto.Request.ElementSelectorWithOptions = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.ElementSelectorWithOptions, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.ElementSelectorWithOptions.displayName = "proto.Request.ElementSelectorWithOptions";
    }
    proto.Request.ElementSelectorWithDuration = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.ElementSelectorWithDuration, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.ElementSelectorWithDuration.displayName = "proto.Request.ElementSelectorWithDuration";
    }
    proto.Request.SelectElementSelector = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.SelectElementSelector, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.SelectElementSelector.displayName = "proto.Request.SelectElementSelector";
    }
    proto.Request.WaitForFunctionOptions = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.WaitForFunctionOptions, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.WaitForFunctionOptions.displayName = "proto.Request.WaitForFunctionOptions";
    }
    proto.Request.PlaywrightObject = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.PlaywrightObject, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.PlaywrightObject.displayName = "proto.Request.PlaywrightObject";
    }
    proto.Request.Viewport = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.Viewport, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Viewport.displayName = "proto.Request.Viewport";
    }
    proto.Request.HttpRequest = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.HttpRequest, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.HttpRequest.displayName = "proto.Request.HttpRequest";
    }
    proto.Request.HttpCapture = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.HttpCapture, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.HttpCapture.displayName = "proto.Request.HttpCapture";
    }
    proto.Request.Device = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.Device, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Device.displayName = "proto.Request.Device";
    }
    proto.Request.AlertAction = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.AlertAction, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.AlertAction.displayName = "proto.Request.AlertAction";
    }
    proto.Request.AlertActions = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, proto.Request.AlertActions.repeatedFields_, null);
    };
    goog.inherits(proto.Request.AlertActions, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.AlertActions.displayName = "proto.Request.AlertActions";
    }
    proto.Request.Bool = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.Bool, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.Bool.displayName = "proto.Request.Bool";
    }
    proto.Request.EvaluateAll = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.EvaluateAll, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.EvaluateAll.displayName = "proto.Request.EvaluateAll";
    }
    proto.Request.ElementStyle = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Request.ElementStyle, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Request.ElementStyle.displayName = "proto.Request.ElementStyle";
    }
    proto.Types = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Types, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Types.displayName = "proto.Types";
    }
    proto.Types.SelectEntry = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Types.SelectEntry, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Types.SelectEntry.displayName = "proto.Types.SelectEntry";
    }
    proto.Response = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Response, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.displayName = "proto.Response";
    }
    proto.Response.Empty = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Response.Empty, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.Empty.displayName = "proto.Response.Empty";
    }
    proto.Response.String = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Response.String, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.String.displayName = "proto.Response.String";
    }
    proto.Response.ListString = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, proto.Response.ListString.repeatedFields_, null);
    };
    goog.inherits(proto.Response.ListString, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.ListString.displayName = "proto.Response.ListString";
    }
    proto.Response.Keywords = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, proto.Response.Keywords.repeatedFields_, null);
    };
    goog.inherits(proto.Response.Keywords, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.Keywords.displayName = "proto.Response.Keywords";
    }
    proto.Response.Bool = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Response.Bool, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.Bool.displayName = "proto.Response.Bool";
    }
    proto.Response.Int = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Response.Int, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.Int.displayName = "proto.Response.Int";
    }
    proto.Response.Select = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, proto.Response.Select.repeatedFields_, null);
    };
    goog.inherits(proto.Response.Select, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.Select.displayName = "proto.Response.Select";
    }
    proto.Response.Json = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Response.Json, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.Json.displayName = "proto.Response.Json";
    }
    proto.Response.JavascriptExecutionResult = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Response.JavascriptExecutionResult, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.JavascriptExecutionResult.displayName = "proto.Response.JavascriptExecutionResult";
    }
    proto.Response.NewContextResponse = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Response.NewContextResponse, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.NewContextResponse.displayName = "proto.Response.NewContextResponse";
    }
    proto.Response.NewPersistentContextResponse = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Response.NewPersistentContextResponse, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.NewPersistentContextResponse.displayName = "proto.Response.NewPersistentContextResponse";
    }
    proto.Response.NewPageResponse = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Response.NewPageResponse, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.NewPageResponse.displayName = "proto.Response.NewPageResponse";
    }
    proto.Response.PageReportResponse = function(opt_data) {
      jspb.Message.initialize(this, opt_data, 0, -1, null, null);
    };
    goog.inherits(proto.Response.PageReportResponse, jspb.Message);
    if (goog.DEBUG && !COMPILED) {
      proto.Response.PageReportResponse.displayName = "proto.Response.PageReportResponse";
    }
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.toObject(opt_includeInstance, this);
      };
      proto.Request.toObject = function(includeInstance, msg) {
        var f, obj = {};
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request();
      return proto.Request.deserializeBinaryFromReader(msg, reader);
    };
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
    proto.Request.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Empty.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Empty.toObject(opt_includeInstance, this);
      };
      proto.Request.Empty.toObject = function(includeInstance, msg) {
        var f, obj = {};
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.Empty.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Empty();
      return proto.Request.Empty.deserializeBinaryFromReader(msg, reader);
    };
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
    proto.Request.Empty.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Empty.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Empty.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.AriaSnapShot.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.AriaSnapShot.toObject(opt_includeInstance, this);
      };
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
    proto.Request.AriaSnapShot.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.AriaSnapShot();
      return proto.Request.AriaSnapShot.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.AriaSnapShot.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLocator(value);
            break;
          case 2:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.AriaSnapShot.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.AriaSnapShot.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.AriaSnapShot.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.AriaSnapShot.prototype.getLocator = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.AriaSnapShot.prototype.setLocator = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.AriaSnapShot.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 2, false)
      );
    };
    proto.Request.AriaSnapShot.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.ClosePage.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.ClosePage.toObject(opt_includeInstance, this);
      };
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
    proto.Request.ClosePage.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.ClosePage();
      return proto.Request.ClosePage.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.ClosePage.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setRunbeforeunload(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.ClosePage.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.ClosePage.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.ClosePage.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getRunbeforeunload();
      if (f) {
        writer.writeBool(
          1,
          f
        );
      }
    };
    proto.Request.ClosePage.prototype.getRunbeforeunload = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 1, false)
      );
    };
    proto.Request.ClosePage.prototype.setRunbeforeunload = function(value) {
      return jspb.Message.setProto3BooleanField(this, 1, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.ClockSetTime.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.ClockSetTime.toObject(opt_includeInstance, this);
      };
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
    proto.Request.ClockSetTime.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.ClockSetTime();
      return proto.Request.ClockSetTime.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.ClockSetTime.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setTime(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSettype(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.ClockSetTime.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.ClockSetTime.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.ClockSetTime.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.ClockSetTime.prototype.getTime = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 1, 0)
      );
    };
    proto.Request.ClockSetTime.prototype.setTime = function(value) {
      return jspb.Message.setProto3IntField(this, 1, value);
    };
    proto.Request.ClockSetTime.prototype.getSettype = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.ClockSetTime.prototype.setSettype = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.ClockAdvance.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.ClockAdvance.toObject(opt_includeInstance, this);
      };
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
    proto.Request.ClockAdvance.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.ClockAdvance();
      return proto.Request.ClockAdvance.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.ClockAdvance.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setTime(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setAdvancetype(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.ClockAdvance.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.ClockAdvance.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.ClockAdvance.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.ClockAdvance.prototype.getTime = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 1, 0)
      );
    };
    proto.Request.ClockAdvance.prototype.setTime = function(value) {
      return jspb.Message.setProto3IntField(this, 1, value);
    };
    proto.Request.ClockAdvance.prototype.getAdvancetype = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.ClockAdvance.prototype.setAdvancetype = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.CoverageStart.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.CoverageStart.toObject(opt_includeInstance, this);
      };
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
    proto.Request.CoverageStart.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.CoverageStart();
      return proto.Request.CoverageStart.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.CoverageStart.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setCoveragetype(value);
            break;
          case 2:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setResetonnavigation(value);
            break;
          case 3:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setReportanonymousscripts(value);
            break;
          case 4:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setConfigfile(value);
            break;
          case 5:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setCoveragedir(value);
            break;
          case 6:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setRaw(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.CoverageStart.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.CoverageStart.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.CoverageStart.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.CoverageStart.prototype.getCoveragetype = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.CoverageStart.prototype.setCoveragetype = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.CoverageStart.prototype.getResetonnavigation = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 2, false)
      );
    };
    proto.Request.CoverageStart.prototype.setResetonnavigation = function(value) {
      return jspb.Message.setProto3BooleanField(this, 2, value);
    };
    proto.Request.CoverageStart.prototype.getReportanonymousscripts = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 3, false)
      );
    };
    proto.Request.CoverageStart.prototype.setReportanonymousscripts = function(value) {
      return jspb.Message.setProto3BooleanField(this, 3, value);
    };
    proto.Request.CoverageStart.prototype.getConfigfile = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 4, "")
      );
    };
    proto.Request.CoverageStart.prototype.setConfigfile = function(value) {
      return jspb.Message.setProto3StringField(this, 4, value);
    };
    proto.Request.CoverageStart.prototype.getCoveragedir = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 5, "")
      );
    };
    proto.Request.CoverageStart.prototype.setCoveragedir = function(value) {
      return jspb.Message.setProto3StringField(this, 5, value);
    };
    proto.Request.CoverageStart.prototype.getRaw = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 6, false)
      );
    };
    proto.Request.CoverageStart.prototype.setRaw = function(value) {
      return jspb.Message.setProto3BooleanField(this, 6, value);
    };
    proto.Request.CoverageMerge.repeatedFields_ = [5];
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.CoverageMerge.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.CoverageMerge.toObject(opt_includeInstance, this);
      };
      proto.Request.CoverageMerge.toObject = function(includeInstance, msg) {
        var f, obj = {
          inputFolder: jspb.Message.getFieldWithDefault(msg, 1, ""),
          outputFolder: jspb.Message.getFieldWithDefault(msg, 2, ""),
          config: jspb.Message.getFieldWithDefault(msg, 3, ""),
          name: jspb.Message.getFieldWithDefault(msg, 4, ""),
          reportsList: (f = jspb.Message.getRepeatedField(msg, 5)) == null ? void 0 : f
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.CoverageMerge.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.CoverageMerge();
      return proto.Request.CoverageMerge.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.CoverageMerge.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setInputFolder(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setOutputFolder(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setConfig(value);
            break;
          case 4:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setName(value);
            break;
          case 5:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.addReports(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.CoverageMerge.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.CoverageMerge.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.CoverageMerge.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.CoverageMerge.prototype.getInputFolder = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.CoverageMerge.prototype.setInputFolder = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.CoverageMerge.prototype.getOutputFolder = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.CoverageMerge.prototype.setOutputFolder = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.CoverageMerge.prototype.getConfig = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.CoverageMerge.prototype.setConfig = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Request.CoverageMerge.prototype.getName = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 4, "")
      );
    };
    proto.Request.CoverageMerge.prototype.setName = function(value) {
      return jspb.Message.setProto3StringField(this, 4, value);
    };
    proto.Request.CoverageMerge.prototype.getReportsList = function() {
      return (
        /** @type {!Array<string>} */
        jspb.Message.getRepeatedField(this, 5)
      );
    };
    proto.Request.CoverageMerge.prototype.setReportsList = function(value) {
      return jspb.Message.setField(this, 5, value || []);
    };
    proto.Request.CoverageMerge.prototype.addReports = function(value, opt_index) {
      return jspb.Message.addToRepeatedField(this, 5, value, opt_index);
    };
    proto.Request.CoverageMerge.prototype.clearReportsList = function() {
      return this.setReportsList([]);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.TraceGroup.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.TraceGroup.toObject(opt_includeInstance, this);
      };
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
    proto.Request.TraceGroup.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.TraceGroup();
      return proto.Request.TraceGroup.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.TraceGroup.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setName(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setFile(value);
            break;
          case 3:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setLine(value);
            break;
          case 4:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setColumn(value);
            break;
          case 5:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setContextid(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.TraceGroup.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.TraceGroup.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.TraceGroup.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.TraceGroup.prototype.getName = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.TraceGroup.prototype.setName = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.TraceGroup.prototype.getFile = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.TraceGroup.prototype.setFile = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.TraceGroup.prototype.getLine = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 3, 0)
      );
    };
    proto.Request.TraceGroup.prototype.setLine = function(value) {
      return jspb.Message.setProto3IntField(this, 3, value);
    };
    proto.Request.TraceGroup.prototype.getColumn = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 4, 0)
      );
    };
    proto.Request.TraceGroup.prototype.setColumn = function(value) {
      return jspb.Message.setProto3IntField(this, 4, value);
    };
    proto.Request.TraceGroup.prototype.getContextid = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 5, "")
      );
    };
    proto.Request.TraceGroup.prototype.setContextid = function(value) {
      return jspb.Message.setProto3StringField(this, 5, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Label.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Label.toObject(opt_includeInstance, this);
      };
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
    proto.Request.Label.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Label();
      return proto.Request.Label.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.Label.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLabel(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.Label.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Label.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Label.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getLabel();
      if (f.length > 0) {
        writer.writeString(
          1,
          f
        );
      }
    };
    proto.Request.Label.prototype.getLabel = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.Label.prototype.setLabel = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.GetByOptions.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.GetByOptions.toObject(opt_includeInstance, this);
      };
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
    proto.Request.GetByOptions.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.GetByOptions();
      return proto.Request.GetByOptions.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.GetByOptions.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setStrategy(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setText(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setOptions(value);
            break;
          case 4:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          case 5:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setAll(value);
            break;
          case 6:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setFrameselector(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.GetByOptions.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.GetByOptions.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.GetByOptions.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.GetByOptions.prototype.getStrategy = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.GetByOptions.prototype.setStrategy = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.GetByOptions.prototype.getText = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.GetByOptions.prototype.setText = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.GetByOptions.prototype.getOptions = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.GetByOptions.prototype.setOptions = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Request.GetByOptions.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 4, false)
      );
    };
    proto.Request.GetByOptions.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 4, value);
    };
    proto.Request.GetByOptions.prototype.getAll = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 5, false)
      );
    };
    proto.Request.GetByOptions.prototype.setAll = function(value) {
      return jspb.Message.setProto3BooleanField(this, 5, value);
    };
    proto.Request.GetByOptions.prototype.getFrameselector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 6, "")
      );
    };
    proto.Request.GetByOptions.prototype.setFrameselector = function(value) {
      return jspb.Message.setProto3StringField(this, 6, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Pdf.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Pdf.toObject(opt_includeInstance, this);
      };
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
          scale: jspb.Message.getFloatingPointFieldWithDefault(msg, 13, 0),
          tagged: jspb.Message.getBooleanFieldWithDefault(msg, 14, false),
          width: jspb.Message.getFieldWithDefault(msg, 15, "")
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.Pdf.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Pdf();
      return proto.Request.Pdf.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.Pdf.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setDisplayheaderfooter(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setFootertemplate(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setFormat(value);
            break;
          case 4:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setHeadertemplate(value);
            break;
          case 5:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setHeight(value);
            break;
          case 6:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setLandscape(value);
            break;
          case 7:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setMargin(value);
            break;
          case 8:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setOutline(value);
            break;
          case 9:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setPageranges(value);
            break;
          case 10:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setPath(value);
            break;
          case 11:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setPrefercsspagesize(value);
            break;
          case 12:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setPrintbackground(value);
            break;
          case 13:
            var value = (
              /** @type {number} */
              reader.readFloat()
            );
            msg.setScale(value);
            break;
          case 14:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setTagged(value);
            break;
          case 15:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setWidth(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.Pdf.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Pdf.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Pdf.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
      if (f !== 0) {
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
    proto.Request.Pdf.prototype.getDisplayheaderfooter = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 1, false)
      );
    };
    proto.Request.Pdf.prototype.setDisplayheaderfooter = function(value) {
      return jspb.Message.setProto3BooleanField(this, 1, value);
    };
    proto.Request.Pdf.prototype.getFootertemplate = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.Pdf.prototype.setFootertemplate = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.Pdf.prototype.getFormat = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.Pdf.prototype.setFormat = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Request.Pdf.prototype.getHeadertemplate = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 4, "")
      );
    };
    proto.Request.Pdf.prototype.setHeadertemplate = function(value) {
      return jspb.Message.setProto3StringField(this, 4, value);
    };
    proto.Request.Pdf.prototype.getHeight = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 5, "")
      );
    };
    proto.Request.Pdf.prototype.setHeight = function(value) {
      return jspb.Message.setProto3StringField(this, 5, value);
    };
    proto.Request.Pdf.prototype.getLandscape = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 6, false)
      );
    };
    proto.Request.Pdf.prototype.setLandscape = function(value) {
      return jspb.Message.setProto3BooleanField(this, 6, value);
    };
    proto.Request.Pdf.prototype.getMargin = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 7, "")
      );
    };
    proto.Request.Pdf.prototype.setMargin = function(value) {
      return jspb.Message.setProto3StringField(this, 7, value);
    };
    proto.Request.Pdf.prototype.getOutline = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 8, false)
      );
    };
    proto.Request.Pdf.prototype.setOutline = function(value) {
      return jspb.Message.setProto3BooleanField(this, 8, value);
    };
    proto.Request.Pdf.prototype.getPageranges = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 9, "")
      );
    };
    proto.Request.Pdf.prototype.setPageranges = function(value) {
      return jspb.Message.setProto3StringField(this, 9, value);
    };
    proto.Request.Pdf.prototype.getPath = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 10, "")
      );
    };
    proto.Request.Pdf.prototype.setPath = function(value) {
      return jspb.Message.setProto3StringField(this, 10, value);
    };
    proto.Request.Pdf.prototype.getPrefercsspagesize = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 11, false)
      );
    };
    proto.Request.Pdf.prototype.setPrefercsspagesize = function(value) {
      return jspb.Message.setProto3BooleanField(this, 11, value);
    };
    proto.Request.Pdf.prototype.getPrintbackground = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 12, false)
      );
    };
    proto.Request.Pdf.prototype.setPrintbackground = function(value) {
      return jspb.Message.setProto3BooleanField(this, 12, value);
    };
    proto.Request.Pdf.prototype.getScale = function() {
      return (
        /** @type {number} */
        jspb.Message.getFloatingPointFieldWithDefault(this, 13, 0)
      );
    };
    proto.Request.Pdf.prototype.setScale = function(value) {
      return jspb.Message.setProto3FloatField(this, 13, value);
    };
    proto.Request.Pdf.prototype.getTagged = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 14, false)
      );
    };
    proto.Request.Pdf.prototype.setTagged = function(value) {
      return jspb.Message.setProto3BooleanField(this, 14, value);
    };
    proto.Request.Pdf.prototype.getWidth = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 15, "")
      );
    };
    proto.Request.Pdf.prototype.setWidth = function(value) {
      return jspb.Message.setProto3StringField(this, 15, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.EmulateMedia.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.EmulateMedia.toObject(opt_includeInstance, this);
      };
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
    proto.Request.EmulateMedia.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.EmulateMedia();
      return proto.Request.EmulateMedia.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.EmulateMedia.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setColorscheme(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setForcedcolors(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setMedia(value);
            break;
          case 4:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setReducedmotion(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.EmulateMedia.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.EmulateMedia.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.EmulateMedia.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.EmulateMedia.prototype.getColorscheme = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.EmulateMedia.prototype.setColorscheme = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.EmulateMedia.prototype.getForcedcolors = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.EmulateMedia.prototype.setForcedcolors = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.EmulateMedia.prototype.getMedia = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.EmulateMedia.prototype.setMedia = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Request.EmulateMedia.prototype.getReducedmotion = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 4, "")
      );
    };
    proto.Request.EmulateMedia.prototype.setReducedmotion = function(value) {
      return jspb.Message.setProto3StringField(this, 4, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.ScreenshotOptions.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.ScreenshotOptions.toObject(opt_includeInstance, this);
      };
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
    proto.Request.ScreenshotOptions.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.ScreenshotOptions();
      return proto.Request.ScreenshotOptions.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.ScreenshotOptions.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setMask(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setOptions(value);
            break;
          case 4:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.ScreenshotOptions.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.ScreenshotOptions.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.ScreenshotOptions.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.ScreenshotOptions.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.ScreenshotOptions.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.ScreenshotOptions.prototype.getMask = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.ScreenshotOptions.prototype.setMask = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.ScreenshotOptions.prototype.getOptions = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.ScreenshotOptions.prototype.setOptions = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Request.ScreenshotOptions.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 4, false)
      );
    };
    proto.Request.ScreenshotOptions.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 4, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.KeywordCall.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.KeywordCall.toObject(opt_includeInstance, this);
      };
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
    proto.Request.KeywordCall.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.KeywordCall();
      return proto.Request.KeywordCall.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.KeywordCall.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setName(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setArguments(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.KeywordCall.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.KeywordCall.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.KeywordCall.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.KeywordCall.prototype.getName = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.KeywordCall.prototype.setName = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.KeywordCall.prototype.getArguments = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.KeywordCall.prototype.setArguments = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.FilePath.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.FilePath.toObject(opt_includeInstance, this);
      };
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
    proto.Request.FilePath.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.FilePath();
      return proto.Request.FilePath.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.FilePath.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setPath(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.FilePath.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.FilePath.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.FilePath.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getPath();
      if (f.length > 0) {
        writer.writeString(
          1,
          f
        );
      }
    };
    proto.Request.FilePath.prototype.getPath = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.FilePath.prototype.setPath = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.FileBySelector.repeatedFields_ = [1];
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.FileBySelector.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.FileBySelector.toObject(opt_includeInstance, this);
      };
      proto.Request.FileBySelector.toObject = function(includeInstance, msg) {
        var f, obj = {
          pathList: (f = jspb.Message.getRepeatedField(msg, 1)) == null ? void 0 : f,
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
    proto.Request.FileBySelector.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.FileBySelector();
      return proto.Request.FileBySelector.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.FileBySelector.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.addPath(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 3:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          case 4:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setName(value);
            break;
          case 5:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setMimetype(value);
            break;
          case 6:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setBuffer(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.FileBySelector.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.FileBySelector.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.FileBySelector.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.FileBySelector.prototype.getPathList = function() {
      return (
        /** @type {!Array<string>} */
        jspb.Message.getRepeatedField(this, 1)
      );
    };
    proto.Request.FileBySelector.prototype.setPathList = function(value) {
      return jspb.Message.setField(this, 1, value || []);
    };
    proto.Request.FileBySelector.prototype.addPath = function(value, opt_index) {
      return jspb.Message.addToRepeatedField(this, 1, value, opt_index);
    };
    proto.Request.FileBySelector.prototype.clearPathList = function() {
      return this.setPathList([]);
    };
    proto.Request.FileBySelector.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.FileBySelector.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.FileBySelector.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 3, false)
      );
    };
    proto.Request.FileBySelector.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 3, value);
    };
    proto.Request.FileBySelector.prototype.getName = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 4, "")
      );
    };
    proto.Request.FileBySelector.prototype.setName = function(value) {
      return jspb.Message.setProto3StringField(this, 4, value);
    };
    proto.Request.FileBySelector.prototype.getMimetype = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 5, "")
      );
    };
    proto.Request.FileBySelector.prototype.setMimetype = function(value) {
      return jspb.Message.setProto3StringField(this, 5, value);
    };
    proto.Request.FileBySelector.prototype.getBuffer = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 6, "")
      );
    };
    proto.Request.FileBySelector.prototype.setBuffer = function(value) {
      return jspb.Message.setProto3StringField(this, 6, value);
    };
    proto.Request.LocatorHandlerAddCustom.repeatedFields_ = [4];
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.LocatorHandlerAddCustom.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.LocatorHandlerAddCustom.toObject(opt_includeInstance, this);
      };
      proto.Request.LocatorHandlerAddCustom.toObject = function(includeInstance, msg) {
        var f, obj = {
          selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
          nowaitafter: jspb.Message.getBooleanFieldWithDefault(msg, 2, false),
          times: jspb.Message.getFieldWithDefault(msg, 3, ""),
          handlerspecsList: jspb.Message.toObjectList(
            msg.getHandlerspecsList(),
            proto.Request.LocatorHandlerAddCustomAction.toObject,
            includeInstance
          )
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.LocatorHandlerAddCustom.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.LocatorHandlerAddCustom();
      return proto.Request.LocatorHandlerAddCustom.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.LocatorHandlerAddCustom.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setNowaitafter(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setTimes(value);
            break;
          case 4:
            var value = new proto.Request.LocatorHandlerAddCustomAction();
            reader.readMessage(value, proto.Request.LocatorHandlerAddCustomAction.deserializeBinaryFromReader);
            msg.addHandlerspecs(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.LocatorHandlerAddCustom.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.LocatorHandlerAddCustom.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.LocatorHandlerAddCustom.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.LocatorHandlerAddCustom.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.LocatorHandlerAddCustom.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.LocatorHandlerAddCustom.prototype.getNowaitafter = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 2, false)
      );
    };
    proto.Request.LocatorHandlerAddCustom.prototype.setNowaitafter = function(value) {
      return jspb.Message.setProto3BooleanField(this, 2, value);
    };
    proto.Request.LocatorHandlerAddCustom.prototype.getTimes = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.LocatorHandlerAddCustom.prototype.setTimes = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Request.LocatorHandlerAddCustom.prototype.getHandlerspecsList = function() {
      return (
        /** @type{!Array<!proto.Request.LocatorHandlerAddCustomAction>} */
        jspb.Message.getRepeatedWrapperField(this, proto.Request.LocatorHandlerAddCustomAction, 4)
      );
    };
    proto.Request.LocatorHandlerAddCustom.prototype.setHandlerspecsList = function(value) {
      return jspb.Message.setRepeatedWrapperField(this, 4, value);
    };
    proto.Request.LocatorHandlerAddCustom.prototype.addHandlerspecs = function(opt_value, opt_index) {
      return jspb.Message.addToRepeatedWrapperField(this, 4, opt_value, proto.Request.LocatorHandlerAddCustomAction, opt_index);
    };
    proto.Request.LocatorHandlerAddCustom.prototype.clearHandlerspecsList = function() {
      return this.setHandlerspecsList([]);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.LocatorHandlerAddCustomAction.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.LocatorHandlerAddCustomAction.toObject(opt_includeInstance, this);
      };
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
    proto.Request.LocatorHandlerAddCustomAction.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.LocatorHandlerAddCustomAction();
      return proto.Request.LocatorHandlerAddCustomAction.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.LocatorHandlerAddCustomAction.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setAction(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setValue(value);
            break;
          case 4:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setOptionsasjson(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.LocatorHandlerAddCustomAction.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.LocatorHandlerAddCustomAction.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.LocatorHandlerAddCustomAction.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.LocatorHandlerAddCustomAction.prototype.getAction = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.LocatorHandlerAddCustomAction.prototype.setAction = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.LocatorHandlerAddCustomAction.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.LocatorHandlerAddCustomAction.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.LocatorHandlerAddCustomAction.prototype.getValue = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.LocatorHandlerAddCustomAction.prototype.setValue = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Request.LocatorHandlerAddCustomAction.prototype.getOptionsasjson = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 4, "")
      );
    };
    proto.Request.LocatorHandlerAddCustomAction.prototype.setOptionsasjson = function(value) {
      return jspb.Message.setProto3StringField(this, 4, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.LocatorHandlerRemove.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.LocatorHandlerRemove.toObject(opt_includeInstance, this);
      };
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
    proto.Request.LocatorHandlerRemove.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.LocatorHandlerRemove();
      return proto.Request.LocatorHandlerRemove.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.LocatorHandlerRemove.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.LocatorHandlerRemove.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.LocatorHandlerRemove.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.LocatorHandlerRemove.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getSelector();
      if (f.length > 0) {
        writer.writeString(
          1,
          f
        );
      }
    };
    proto.Request.LocatorHandlerRemove.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.LocatorHandlerRemove.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Json.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Json.toObject(opt_includeInstance, this);
      };
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
    proto.Request.Json.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Json();
      return proto.Request.Json.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.Json.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setBody(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.Json.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Json.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Json.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getBody();
      if (f.length > 0) {
        writer.writeString(
          1,
          f
        );
      }
    };
    proto.Request.Json.prototype.getBody = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.Json.prototype.setBody = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.MouseButtonOptions.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.MouseButtonOptions.toObject(opt_includeInstance, this);
      };
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
    proto.Request.MouseButtonOptions.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.MouseButtonOptions();
      return proto.Request.MouseButtonOptions.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.MouseButtonOptions.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setAction(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setJson(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.MouseButtonOptions.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.MouseButtonOptions.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.MouseButtonOptions.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.MouseButtonOptions.prototype.getAction = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.MouseButtonOptions.prototype.setAction = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.MouseButtonOptions.prototype.getJson = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.MouseButtonOptions.prototype.setJson = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.MouseWheel.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.MouseWheel.toObject(opt_includeInstance, this);
      };
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
    proto.Request.MouseWheel.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.MouseWheel();
      return proto.Request.MouseWheel.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.MouseWheel.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setDeltax(value);
            break;
          case 2:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setDeltay(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.MouseWheel.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.MouseWheel.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.MouseWheel.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.MouseWheel.prototype.getDeltax = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 1, 0)
      );
    };
    proto.Request.MouseWheel.prototype.setDeltax = function(value) {
      return jspb.Message.setProto3IntField(this, 1, value);
    };
    proto.Request.MouseWheel.prototype.getDeltay = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 2, 0)
      );
    };
    proto.Request.MouseWheel.prototype.setDeltay = function(value) {
      return jspb.Message.setProto3IntField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.KeyboardKeypress.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.KeyboardKeypress.toObject(opt_includeInstance, this);
      };
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
    proto.Request.KeyboardKeypress.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.KeyboardKeypress();
      return proto.Request.KeyboardKeypress.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.KeyboardKeypress.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setAction(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setKey(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.KeyboardKeypress.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.KeyboardKeypress.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.KeyboardKeypress.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.KeyboardKeypress.prototype.getAction = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.KeyboardKeypress.prototype.setAction = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.KeyboardKeypress.prototype.getKey = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.KeyboardKeypress.prototype.setKey = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.KeyboardInputOptions.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.KeyboardInputOptions.toObject(opt_includeInstance, this);
      };
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
    proto.Request.KeyboardInputOptions.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.KeyboardInputOptions();
      return proto.Request.KeyboardInputOptions.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.KeyboardInputOptions.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setAction(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setInput(value);
            break;
          case 3:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setDelay(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.KeyboardInputOptions.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.KeyboardInputOptions.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.KeyboardInputOptions.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.KeyboardInputOptions.prototype.getAction = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.KeyboardInputOptions.prototype.setAction = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.KeyboardInputOptions.prototype.getInput = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.KeyboardInputOptions.prototype.setInput = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.KeyboardInputOptions.prototype.getDelay = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 3, 0)
      );
    };
    proto.Request.KeyboardInputOptions.prototype.setDelay = function(value) {
      return jspb.Message.setProto3IntField(this, 3, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Browser.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Browser.toObject(opt_includeInstance, this);
      };
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
    proto.Request.Browser.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Browser();
      return proto.Request.Browser.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.Browser.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setBrowser(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setRawoptions(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.Browser.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Browser.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Browser.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.Browser.prototype.getBrowser = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.Browser.prototype.setBrowser = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.Browser.prototype.getRawoptions = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.Browser.prototype.setRawoptions = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Context.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Context.toObject(opt_includeInstance, this);
      };
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
    proto.Request.Context.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Context();
      return proto.Request.Context.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.Context.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setRawoptions(value);
            break;
          case 2:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setDefaulttimeout(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setTracefile(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.Context.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Context.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Context.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.Context.prototype.getRawoptions = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.Context.prototype.setRawoptions = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.Context.prototype.getDefaulttimeout = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 2, 0)
      );
    };
    proto.Request.Context.prototype.setDefaulttimeout = function(value) {
      return jspb.Message.setProto3IntField(this, 2, value);
    };
    proto.Request.Context.prototype.getTracefile = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.Context.prototype.setTracefile = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.PersistentContext.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.PersistentContext.toObject(opt_includeInstance, this);
      };
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
    proto.Request.PersistentContext.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.PersistentContext();
      return proto.Request.PersistentContext.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.PersistentContext.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setBrowser(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setRawoptions(value);
            break;
          case 3:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setDefaulttimeout(value);
            break;
          case 4:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setTracefile(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.PersistentContext.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.PersistentContext.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.PersistentContext.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.PersistentContext.prototype.getBrowser = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.PersistentContext.prototype.setBrowser = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.PersistentContext.prototype.getRawoptions = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.PersistentContext.prototype.setRawoptions = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.PersistentContext.prototype.getDefaulttimeout = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 3, 0)
      );
    };
    proto.Request.PersistentContext.prototype.setDefaulttimeout = function(value) {
      return jspb.Message.setProto3IntField(this, 3, value);
    };
    proto.Request.PersistentContext.prototype.getTracefile = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 4, "")
      );
    };
    proto.Request.PersistentContext.prototype.setTracefile = function(value) {
      return jspb.Message.setProto3StringField(this, 4, value);
    };
    proto.Request.ElectronLaunch.repeatedFields_ = [2];
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.ElectronLaunch.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.ElectronLaunch.toObject(opt_includeInstance, this);
      };
      proto.Request.ElectronLaunch.toObject = function(includeInstance, msg) {
        var f, obj = {
          executablePath: jspb.Message.getFieldWithDefault(msg, 1, ""),
          argsList: (f = jspb.Message.getRepeatedField(msg, 2)) == null ? void 0 : f,
          envMap: (f = msg.getEnvMap()) ? f.toObject(includeInstance, void 0) : [],
          timeout: jspb.Message.getFieldWithDefault(msg, 4, 0)
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.ElectronLaunch.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.ElectronLaunch();
      return proto.Request.ElectronLaunch.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.ElectronLaunch.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setExecutablePath(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.addArgs(value);
            break;
          case 3:
            var value = msg.getEnvMap();
            reader.readMessage(value, function(message, reader2) {
              jspb.Map.deserializeBinary(message, reader2, jspb.BinaryReader.prototype.readString, jspb.BinaryReader.prototype.readString, null, "", "");
            });
            break;
          case 4:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setTimeout(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.ElectronLaunch.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.ElectronLaunch.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.ElectronLaunch.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.ElectronLaunch.prototype.getExecutablePath = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.ElectronLaunch.prototype.setExecutablePath = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.ElectronLaunch.prototype.getArgsList = function() {
      return (
        /** @type {!Array<string>} */
        jspb.Message.getRepeatedField(this, 2)
      );
    };
    proto.Request.ElectronLaunch.prototype.setArgsList = function(value) {
      return jspb.Message.setField(this, 2, value || []);
    };
    proto.Request.ElectronLaunch.prototype.addArgs = function(value, opt_index) {
      return jspb.Message.addToRepeatedField(this, 2, value, opt_index);
    };
    proto.Request.ElectronLaunch.prototype.clearArgsList = function() {
      return this.setArgsList([]);
    };
    proto.Request.ElectronLaunch.prototype.getEnvMap = function(opt_noLazyCreate) {
      return (
        /** @type {!jspb.Map<string,string>} */
        jspb.Message.getMapField(
          this,
          3,
          opt_noLazyCreate,
          null
        )
      );
    };
    proto.Request.ElectronLaunch.prototype.clearEnvMap = function() {
      this.getEnvMap().clear();
      return this;
    };
    proto.Request.ElectronLaunch.prototype.getTimeout = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 4, 0)
      );
    };
    proto.Request.ElectronLaunch.prototype.setTimeout = function(value) {
      return jspb.Message.setProto3IntField(this, 4, value);
    };
    proto.Request.Permissions.repeatedFields_ = [1];
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Permissions.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Permissions.toObject(opt_includeInstance, this);
      };
      proto.Request.Permissions.toObject = function(includeInstance, msg) {
        var f, obj = {
          permissionsList: (f = jspb.Message.getRepeatedField(msg, 1)) == null ? void 0 : f,
          origin: jspb.Message.getFieldWithDefault(msg, 2, "")
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.Permissions.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Permissions();
      return proto.Request.Permissions.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.Permissions.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.addPermissions(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setOrigin(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.Permissions.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Permissions.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Permissions.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.Permissions.prototype.getPermissionsList = function() {
      return (
        /** @type {!Array<string>} */
        jspb.Message.getRepeatedField(this, 1)
      );
    };
    proto.Request.Permissions.prototype.setPermissionsList = function(value) {
      return jspb.Message.setField(this, 1, value || []);
    };
    proto.Request.Permissions.prototype.addPermissions = function(value, opt_index) {
      return jspb.Message.addToRepeatedField(this, 1, value, opt_index);
    };
    proto.Request.Permissions.prototype.clearPermissionsList = function() {
      return this.setPermissionsList([]);
    };
    proto.Request.Permissions.prototype.getOrigin = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.Permissions.prototype.setOrigin = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Url.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Url.toObject(opt_includeInstance, this);
      };
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
    proto.Request.Url.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Url();
      return proto.Request.Url.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.Url.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setUrl(value);
            break;
          case 2:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setDefaulttimeout(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.Url.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Url.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Url.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.Url.prototype.getUrl = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.Url.prototype.setUrl = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.Url.prototype.getDefaulttimeout = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 2, 0)
      );
    };
    proto.Request.Url.prototype.setDefaulttimeout = function(value) {
      return jspb.Message.setProto3IntField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.DownloadOptions.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.DownloadOptions.toObject(opt_includeInstance, this);
      };
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
    proto.Request.DownloadOptions.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.DownloadOptions();
      return proto.Request.DownloadOptions.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.DownloadOptions.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setUrl(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setPath(value);
            break;
          case 3:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setWaitforfinish(value);
            break;
          case 4:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setDownloadtimeout(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.DownloadOptions.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.DownloadOptions.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.DownloadOptions.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.DownloadOptions.prototype.getUrl = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.DownloadOptions.prototype.setUrl = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.DownloadOptions.prototype.getPath = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.DownloadOptions.prototype.setPath = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.DownloadOptions.prototype.getWaitforfinish = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 3, false)
      );
    };
    proto.Request.DownloadOptions.prototype.setWaitforfinish = function(value) {
      return jspb.Message.setProto3BooleanField(this, 3, value);
    };
    proto.Request.DownloadOptions.prototype.getDownloadtimeout = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 4, 0)
      );
    };
    proto.Request.DownloadOptions.prototype.setDownloadtimeout = function(value) {
      return jspb.Message.setProto3IntField(this, 4, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.DownloadID.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.DownloadID.toObject(opt_includeInstance, this);
      };
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
    proto.Request.DownloadID.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.DownloadID();
      return proto.Request.DownloadID.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.DownloadID.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setId(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.DownloadID.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.DownloadID.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.DownloadID.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getId();
      if (f.length > 0) {
        writer.writeString(
          1,
          f
        );
      }
    };
    proto.Request.DownloadID.prototype.getId = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.DownloadID.prototype.setId = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.UrlOptions.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.UrlOptions.toObject(opt_includeInstance, this);
      };
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
    proto.Request.UrlOptions.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.UrlOptions();
      return proto.Request.UrlOptions.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.UrlOptions.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = new proto.Request.Url();
            reader.readMessage(value, proto.Request.Url.deserializeBinaryFromReader);
            msg.setUrl(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setWaituntil(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.UrlOptions.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.UrlOptions.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.UrlOptions.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.UrlOptions.prototype.getUrl = function() {
      return (
        /** @type{?proto.Request.Url} */
        jspb.Message.getWrapperField(this, proto.Request.Url, 1)
      );
    };
    proto.Request.UrlOptions.prototype.setUrl = function(value) {
      return jspb.Message.setWrapperField(this, 1, value);
    };
    proto.Request.UrlOptions.prototype.clearUrl = function() {
      return this.setUrl(void 0);
    };
    proto.Request.UrlOptions.prototype.hasUrl = function() {
      return jspb.Message.getField(this, 1) != null;
    };
    proto.Request.UrlOptions.prototype.getWaituntil = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.UrlOptions.prototype.setWaituntil = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.PageLoadState.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.PageLoadState.toObject(opt_includeInstance, this);
      };
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
    proto.Request.PageLoadState.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.PageLoadState();
      return proto.Request.PageLoadState.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.PageLoadState.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setState(value);
            break;
          case 2:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setTimeout(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.PageLoadState.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.PageLoadState.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.PageLoadState.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.PageLoadState.prototype.getState = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.PageLoadState.prototype.setState = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.PageLoadState.prototype.getTimeout = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 2, 0)
      );
    };
    proto.Request.PageLoadState.prototype.setTimeout = function(value) {
      return jspb.Message.setProto3IntField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.ConnectBrowser.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.ConnectBrowser.toObject(opt_includeInstance, this);
      };
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
    proto.Request.ConnectBrowser.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.ConnectBrowser();
      return proto.Request.ConnectBrowser.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.ConnectBrowser.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setBrowser(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setUrl(value);
            break;
          case 3:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setConnectcdp(value);
            break;
          case 4:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setTimeout(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.ConnectBrowser.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.ConnectBrowser.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.ConnectBrowser.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.ConnectBrowser.prototype.getBrowser = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.ConnectBrowser.prototype.setBrowser = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.ConnectBrowser.prototype.getUrl = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.ConnectBrowser.prototype.setUrl = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.ConnectBrowser.prototype.getConnectcdp = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 3, false)
      );
    };
    proto.Request.ConnectBrowser.prototype.setConnectcdp = function(value) {
      return jspb.Message.setProto3BooleanField(this, 3, value);
    };
    proto.Request.ConnectBrowser.prototype.getTimeout = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 4, 0)
      );
    };
    proto.Request.ConnectBrowser.prototype.setTimeout = function(value) {
      return jspb.Message.setProto3IntField(this, 4, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.TextInput.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.TextInput.toObject(opt_includeInstance, this);
      };
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
    proto.Request.TextInput.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.TextInput();
      return proto.Request.TextInput.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.TextInput.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setInput(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 3:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setType(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.TextInput.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.TextInput.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.TextInput.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.TextInput.prototype.getInput = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.TextInput.prototype.setInput = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.TextInput.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.TextInput.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.TextInput.prototype.getType = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 3, false)
      );
    };
    proto.Request.TextInput.prototype.setType = function(value) {
      return jspb.Message.setProto3BooleanField(this, 3, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.ElementProperty.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.ElementProperty.toObject(opt_includeInstance, this);
      };
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
    proto.Request.ElementProperty.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.ElementProperty();
      return proto.Request.ElementProperty.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.ElementProperty.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setProperty(value);
            break;
          case 3:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.ElementProperty.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.ElementProperty.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.ElementProperty.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.ElementProperty.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.ElementProperty.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.ElementProperty.prototype.getProperty = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.ElementProperty.prototype.setProperty = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.ElementProperty.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 3, false)
      );
    };
    proto.Request.ElementProperty.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 3, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.TypeText.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.TypeText.toObject(opt_includeInstance, this);
      };
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
    proto.Request.TypeText.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.TypeText();
      return proto.Request.TypeText.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.TypeText.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setText(value);
            break;
          case 3:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setDelay(value);
            break;
          case 4:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setClear(value);
            break;
          case 5:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.TypeText.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.TypeText.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.TypeText.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.TypeText.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.TypeText.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.TypeText.prototype.getText = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.TypeText.prototype.setText = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.TypeText.prototype.getDelay = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 3, 0)
      );
    };
    proto.Request.TypeText.prototype.setDelay = function(value) {
      return jspb.Message.setProto3IntField(this, 3, value);
    };
    proto.Request.TypeText.prototype.getClear = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 4, false)
      );
    };
    proto.Request.TypeText.prototype.setClear = function(value) {
      return jspb.Message.setProto3BooleanField(this, 4, value);
    };
    proto.Request.TypeText.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 5, false)
      );
    };
    proto.Request.TypeText.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 5, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.FillText.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.FillText.toObject(opt_includeInstance, this);
      };
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
    proto.Request.FillText.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.FillText();
      return proto.Request.FillText.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.FillText.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setText(value);
            break;
          case 3:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          case 4:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setForce(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.FillText.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.FillText.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.FillText.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.FillText.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.FillText.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.FillText.prototype.getText = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.FillText.prototype.setText = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.FillText.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 3, false)
      );
    };
    proto.Request.FillText.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 3, value);
    };
    proto.Request.FillText.prototype.getForce = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 4, false)
      );
    };
    proto.Request.FillText.prototype.setForce = function(value) {
      return jspb.Message.setProto3BooleanField(this, 4, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.ClearText.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.ClearText.toObject(opt_includeInstance, this);
      };
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
    proto.Request.ClearText.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.ClearText();
      return proto.Request.ClearText.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.ClearText.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.ClearText.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.ClearText.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.ClearText.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.ClearText.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.ClearText.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.ClearText.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 2, false)
      );
    };
    proto.Request.ClearText.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 2, value);
    };
    proto.Request.PressKeys.repeatedFields_ = [3];
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.PressKeys.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.PressKeys.toObject(opt_includeInstance, this);
      };
      proto.Request.PressKeys.toObject = function(includeInstance, msg) {
        var f, obj = {
          selector: jspb.Message.getFieldWithDefault(msg, 1, ""),
          strict: jspb.Message.getBooleanFieldWithDefault(msg, 2, false),
          keyList: (f = jspb.Message.getRepeatedField(msg, 3)) == null ? void 0 : f,
          pressdelay: jspb.Message.getFieldWithDefault(msg, 4, 0),
          keydelay: jspb.Message.getFieldWithDefault(msg, 5, 0)
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.PressKeys.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.PressKeys();
      return proto.Request.PressKeys.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.PressKeys.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.addKey(value);
            break;
          case 4:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setPressdelay(value);
            break;
          case 5:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setKeydelay(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.PressKeys.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.PressKeys.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.PressKeys.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.PressKeys.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.PressKeys.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.PressKeys.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 2, false)
      );
    };
    proto.Request.PressKeys.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 2, value);
    };
    proto.Request.PressKeys.prototype.getKeyList = function() {
      return (
        /** @type {!Array<string>} */
        jspb.Message.getRepeatedField(this, 3)
      );
    };
    proto.Request.PressKeys.prototype.setKeyList = function(value) {
      return jspb.Message.setField(this, 3, value || []);
    };
    proto.Request.PressKeys.prototype.addKey = function(value, opt_index) {
      return jspb.Message.addToRepeatedField(this, 3, value, opt_index);
    };
    proto.Request.PressKeys.prototype.clearKeyList = function() {
      return this.setKeyList([]);
    };
    proto.Request.PressKeys.prototype.getPressdelay = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 4, 0)
      );
    };
    proto.Request.PressKeys.prototype.setPressdelay = function(value) {
      return jspb.Message.setProto3IntField(this, 4, value);
    };
    proto.Request.PressKeys.prototype.getKeydelay = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 5, 0)
      );
    };
    proto.Request.PressKeys.prototype.setKeydelay = function(value) {
      return jspb.Message.setProto3IntField(this, 5, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.ElementSelector.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.ElementSelector.toObject(opt_includeInstance, this);
      };
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
    proto.Request.ElementSelector.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.ElementSelector();
      return proto.Request.ElementSelector.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.ElementSelector.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          case 3:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setForce(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.ElementSelector.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.ElementSelector.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.ElementSelector.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.ElementSelector.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.ElementSelector.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.ElementSelector.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 2, false)
      );
    };
    proto.Request.ElementSelector.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 2, value);
    };
    proto.Request.ElementSelector.prototype.getForce = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 3, false)
      );
    };
    proto.Request.ElementSelector.prototype.setForce = function(value) {
      return jspb.Message.setProto3BooleanField(this, 3, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Timeout.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Timeout.toObject(opt_includeInstance, this);
      };
      proto.Request.Timeout.toObject = function(includeInstance, msg) {
        var f, obj = {
          timeout: jspb.Message.getFloatingPointFieldWithDefault(msg, 1, 0)
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.Timeout.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Timeout();
      return proto.Request.Timeout.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.Timeout.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {number} */
              reader.readFloat()
            );
            msg.setTimeout(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.Timeout.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Timeout.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Timeout.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getTimeout();
      if (f !== 0) {
        writer.writeFloat(
          1,
          f
        );
      }
    };
    proto.Request.Timeout.prototype.getTimeout = function() {
      return (
        /** @type {number} */
        jspb.Message.getFloatingPointFieldWithDefault(this, 1, 0)
      );
    };
    proto.Request.Timeout.prototype.setTimeout = function(value) {
      return jspb.Message.setProto3FloatField(this, 1, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Index.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Index.toObject(opt_includeInstance, this);
      };
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
    proto.Request.Index.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Index();
      return proto.Request.Index.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.Index.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setIndex(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.Index.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Index.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Index.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getIndex();
      if (f.length > 0) {
        writer.writeString(
          1,
          f
        );
      }
    };
    proto.Request.Index.prototype.getIndex = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.Index.prototype.setIndex = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.IdWithTimeout.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.IdWithTimeout.toObject(opt_includeInstance, this);
      };
      proto.Request.IdWithTimeout.toObject = function(includeInstance, msg) {
        var f, obj = {
          id: jspb.Message.getFieldWithDefault(msg, 1, ""),
          timeout: jspb.Message.getFloatingPointFieldWithDefault(msg, 2, 0)
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.IdWithTimeout.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.IdWithTimeout();
      return proto.Request.IdWithTimeout.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.IdWithTimeout.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setId(value);
            break;
          case 2:
            var value = (
              /** @type {number} */
              reader.readFloat()
            );
            msg.setTimeout(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.IdWithTimeout.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.IdWithTimeout.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.IdWithTimeout.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getId();
      if (f.length > 0) {
        writer.writeString(
          1,
          f
        );
      }
      f = message.getTimeout();
      if (f !== 0) {
        writer.writeFloat(
          2,
          f
        );
      }
    };
    proto.Request.IdWithTimeout.prototype.getId = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.IdWithTimeout.prototype.setId = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.IdWithTimeout.prototype.getTimeout = function() {
      return (
        /** @type {number} */
        jspb.Message.getFloatingPointFieldWithDefault(this, 2, 0)
      );
    };
    proto.Request.IdWithTimeout.prototype.setTimeout = function(value) {
      return jspb.Message.setProto3FloatField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.StyleTag.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.StyleTag.toObject(opt_includeInstance, this);
      };
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
    proto.Request.StyleTag.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.StyleTag();
      return proto.Request.StyleTag.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.StyleTag.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setContent(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.StyleTag.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.StyleTag.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.StyleTag.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getContent();
      if (f.length > 0) {
        writer.writeString(
          1,
          f
        );
      }
    };
    proto.Request.StyleTag.prototype.getContent = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.StyleTag.prototype.setContent = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.ElementSelectorWithOptions.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.ElementSelectorWithOptions.toObject(opt_includeInstance, this);
      };
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
    proto.Request.ElementSelectorWithOptions.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.ElementSelectorWithOptions();
      return proto.Request.ElementSelectorWithOptions.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.ElementSelectorWithOptions.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setOptions(value);
            break;
          case 3:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.ElementSelectorWithOptions.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.ElementSelectorWithOptions.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.ElementSelectorWithOptions.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.ElementSelectorWithOptions.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.ElementSelectorWithOptions.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.ElementSelectorWithOptions.prototype.getOptions = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.ElementSelectorWithOptions.prototype.setOptions = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.ElementSelectorWithOptions.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 3, false)
      );
    };
    proto.Request.ElementSelectorWithOptions.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 3, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.ElementSelectorWithDuration.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.ElementSelectorWithDuration.toObject(opt_includeInstance, this);
      };
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
    proto.Request.ElementSelectorWithDuration.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.ElementSelectorWithDuration();
      return proto.Request.ElementSelectorWithDuration.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.ElementSelectorWithDuration.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setDuration(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setWidth(value);
            break;
          case 4:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setStyle(value);
            break;
          case 5:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setColor(value);
            break;
          case 6:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          case 7:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setMode(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.ElementSelectorWithDuration.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.ElementSelectorWithDuration.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.ElementSelectorWithDuration.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.ElementSelectorWithDuration.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.ElementSelectorWithDuration.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.ElementSelectorWithDuration.prototype.getDuration = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 2, 0)
      );
    };
    proto.Request.ElementSelectorWithDuration.prototype.setDuration = function(value) {
      return jspb.Message.setProto3IntField(this, 2, value);
    };
    proto.Request.ElementSelectorWithDuration.prototype.getWidth = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.ElementSelectorWithDuration.prototype.setWidth = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Request.ElementSelectorWithDuration.prototype.getStyle = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 4, "")
      );
    };
    proto.Request.ElementSelectorWithDuration.prototype.setStyle = function(value) {
      return jspb.Message.setProto3StringField(this, 4, value);
    };
    proto.Request.ElementSelectorWithDuration.prototype.getColor = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 5, "")
      );
    };
    proto.Request.ElementSelectorWithDuration.prototype.setColor = function(value) {
      return jspb.Message.setProto3StringField(this, 5, value);
    };
    proto.Request.ElementSelectorWithDuration.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 6, false)
      );
    };
    proto.Request.ElementSelectorWithDuration.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 6, value);
    };
    proto.Request.ElementSelectorWithDuration.prototype.getMode = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 7, "")
      );
    };
    proto.Request.ElementSelectorWithDuration.prototype.setMode = function(value) {
      return jspb.Message.setProto3StringField(this, 7, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.SelectElementSelector.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.SelectElementSelector.toObject(opt_includeInstance, this);
      };
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
    proto.Request.SelectElementSelector.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.SelectElementSelector();
      return proto.Request.SelectElementSelector.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.SelectElementSelector.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setMatcherjson(value);
            break;
          case 3:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.SelectElementSelector.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.SelectElementSelector.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.SelectElementSelector.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.SelectElementSelector.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.SelectElementSelector.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.SelectElementSelector.prototype.getMatcherjson = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.SelectElementSelector.prototype.setMatcherjson = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.SelectElementSelector.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 3, false)
      );
    };
    proto.Request.SelectElementSelector.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 3, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.WaitForFunctionOptions.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.WaitForFunctionOptions.toObject(opt_includeInstance, this);
      };
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
    proto.Request.WaitForFunctionOptions.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.WaitForFunctionOptions();
      return proto.Request.WaitForFunctionOptions.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.WaitForFunctionOptions.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setScript(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setOptions(value);
            break;
          case 4:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.WaitForFunctionOptions.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.WaitForFunctionOptions.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.WaitForFunctionOptions.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.WaitForFunctionOptions.prototype.getScript = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.WaitForFunctionOptions.prototype.setScript = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.WaitForFunctionOptions.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.WaitForFunctionOptions.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.WaitForFunctionOptions.prototype.getOptions = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.WaitForFunctionOptions.prototype.setOptions = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Request.WaitForFunctionOptions.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 4, false)
      );
    };
    proto.Request.WaitForFunctionOptions.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 4, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.PlaywrightObject.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.PlaywrightObject.toObject(opt_includeInstance, this);
      };
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
    proto.Request.PlaywrightObject.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.PlaywrightObject();
      return proto.Request.PlaywrightObject.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.PlaywrightObject.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setInfo(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.PlaywrightObject.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.PlaywrightObject.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.PlaywrightObject.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getInfo();
      if (f.length > 0) {
        writer.writeString(
          1,
          f
        );
      }
    };
    proto.Request.PlaywrightObject.prototype.getInfo = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.PlaywrightObject.prototype.setInfo = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Viewport.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Viewport.toObject(opt_includeInstance, this);
      };
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
    proto.Request.Viewport.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Viewport();
      return proto.Request.Viewport.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.Viewport.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setWidth(value);
            break;
          case 2:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setHeight(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.Viewport.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Viewport.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Viewport.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.Viewport.prototype.getWidth = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 1, 0)
      );
    };
    proto.Request.Viewport.prototype.setWidth = function(value) {
      return jspb.Message.setProto3IntField(this, 1, value);
    };
    proto.Request.Viewport.prototype.getHeight = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 2, 0)
      );
    };
    proto.Request.Viewport.prototype.setHeight = function(value) {
      return jspb.Message.setProto3IntField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.HttpRequest.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.HttpRequest.toObject(opt_includeInstance, this);
      };
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
    proto.Request.HttpRequest.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.HttpRequest();
      return proto.Request.HttpRequest.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.HttpRequest.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setUrl(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setMethod(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setBody(value);
            break;
          case 4:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setHeaders(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.HttpRequest.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.HttpRequest.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.HttpRequest.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.HttpRequest.prototype.getUrl = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.HttpRequest.prototype.setUrl = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.HttpRequest.prototype.getMethod = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.HttpRequest.prototype.setMethod = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.HttpRequest.prototype.getBody = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.HttpRequest.prototype.setBody = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Request.HttpRequest.prototype.getHeaders = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 4, "")
      );
    };
    proto.Request.HttpRequest.prototype.setHeaders = function(value) {
      return jspb.Message.setProto3StringField(this, 4, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.HttpCapture.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.HttpCapture.toObject(opt_includeInstance, this);
      };
      proto.Request.HttpCapture.toObject = function(includeInstance, msg) {
        var f, obj = {
          urlorpredicate: jspb.Message.getFieldWithDefault(msg, 1, ""),
          timeout: jspb.Message.getFloatingPointFieldWithDefault(msg, 2, 0)
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.HttpCapture.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.HttpCapture();
      return proto.Request.HttpCapture.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.HttpCapture.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setUrlorpredicate(value);
            break;
          case 2:
            var value = (
              /** @type {number} */
              reader.readFloat()
            );
            msg.setTimeout(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.HttpCapture.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.HttpCapture.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.HttpCapture.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getUrlorpredicate();
      if (f.length > 0) {
        writer.writeString(
          1,
          f
        );
      }
      f = message.getTimeout();
      if (f !== 0) {
        writer.writeFloat(
          2,
          f
        );
      }
    };
    proto.Request.HttpCapture.prototype.getUrlorpredicate = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.HttpCapture.prototype.setUrlorpredicate = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.HttpCapture.prototype.getTimeout = function() {
      return (
        /** @type {number} */
        jspb.Message.getFloatingPointFieldWithDefault(this, 2, 0)
      );
    };
    proto.Request.HttpCapture.prototype.setTimeout = function(value) {
      return jspb.Message.setProto3FloatField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Device.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Device.toObject(opt_includeInstance, this);
      };
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
    proto.Request.Device.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Device();
      return proto.Request.Device.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.Device.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setName(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.Device.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Device.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Device.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getName();
      if (f.length > 0) {
        writer.writeString(
          1,
          f
        );
      }
    };
    proto.Request.Device.prototype.getName = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.Device.prototype.setName = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.AlertAction.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.AlertAction.toObject(opt_includeInstance, this);
      };
      proto.Request.AlertAction.toObject = function(includeInstance, msg) {
        var f, obj = {
          alertaction: jspb.Message.getFieldWithDefault(msg, 1, ""),
          promptinput: jspb.Message.getFieldWithDefault(msg, 2, ""),
          timeout: jspb.Message.getFloatingPointFieldWithDefault(msg, 3, 0)
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.AlertAction.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.AlertAction();
      return proto.Request.AlertAction.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.AlertAction.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setAlertaction(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setPromptinput(value);
            break;
          case 3:
            var value = (
              /** @type {number} */
              reader.readFloat()
            );
            msg.setTimeout(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.AlertAction.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.AlertAction.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.AlertAction.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
      if (f !== 0) {
        writer.writeFloat(
          3,
          f
        );
      }
    };
    proto.Request.AlertAction.prototype.getAlertaction = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.AlertAction.prototype.setAlertaction = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.AlertAction.prototype.getPromptinput = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.AlertAction.prototype.setPromptinput = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.AlertAction.prototype.getTimeout = function() {
      return (
        /** @type {number} */
        jspb.Message.getFloatingPointFieldWithDefault(this, 3, 0)
      );
    };
    proto.Request.AlertAction.prototype.setTimeout = function(value) {
      return jspb.Message.setProto3FloatField(this, 3, value);
    };
    proto.Request.AlertActions.repeatedFields_ = [1];
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.AlertActions.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.AlertActions.toObject(opt_includeInstance, this);
      };
      proto.Request.AlertActions.toObject = function(includeInstance, msg) {
        var f, obj = {
          itemsList: jspb.Message.toObjectList(
            msg.getItemsList(),
            proto.Request.AlertAction.toObject,
            includeInstance
          )
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Request.AlertActions.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.AlertActions();
      return proto.Request.AlertActions.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.AlertActions.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = new proto.Request.AlertAction();
            reader.readMessage(value, proto.Request.AlertAction.deserializeBinaryFromReader);
            msg.addItems(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.AlertActions.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.AlertActions.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.AlertActions.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getItemsList();
      if (f.length > 0) {
        writer.writeRepeatedMessage(
          1,
          f,
          proto.Request.AlertAction.serializeBinaryToWriter
        );
      }
    };
    proto.Request.AlertActions.prototype.getItemsList = function() {
      return (
        /** @type{!Array<!proto.Request.AlertAction>} */
        jspb.Message.getRepeatedWrapperField(this, proto.Request.AlertAction, 1)
      );
    };
    proto.Request.AlertActions.prototype.setItemsList = function(value) {
      return jspb.Message.setRepeatedWrapperField(this, 1, value);
    };
    proto.Request.AlertActions.prototype.addItems = function(opt_value, opt_index) {
      return jspb.Message.addToRepeatedWrapperField(this, 1, opt_value, proto.Request.AlertAction, opt_index);
    };
    proto.Request.AlertActions.prototype.clearItemsList = function() {
      return this.setItemsList([]);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.Bool.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.Bool.toObject(opt_includeInstance, this);
      };
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
    proto.Request.Bool.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.Bool();
      return proto.Request.Bool.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.Bool.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setValue(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.Bool.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.Bool.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.Bool.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getValue();
      if (f) {
        writer.writeBool(
          1,
          f
        );
      }
    };
    proto.Request.Bool.prototype.getValue = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 1, false)
      );
    };
    proto.Request.Bool.prototype.setValue = function(value) {
      return jspb.Message.setProto3BooleanField(this, 1, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.EvaluateAll.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.EvaluateAll.toObject(opt_includeInstance, this);
      };
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
    proto.Request.EvaluateAll.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.EvaluateAll();
      return proto.Request.EvaluateAll.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.EvaluateAll.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setScript(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setArg(value);
            break;
          case 4:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setAllelements(value);
            break;
          case 5:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.EvaluateAll.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.EvaluateAll.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.EvaluateAll.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.EvaluateAll.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.EvaluateAll.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.EvaluateAll.prototype.getScript = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.EvaluateAll.prototype.setScript = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.EvaluateAll.prototype.getArg = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.EvaluateAll.prototype.setArg = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Request.EvaluateAll.prototype.getAllelements = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 4, false)
      );
    };
    proto.Request.EvaluateAll.prototype.setAllelements = function(value) {
      return jspb.Message.setProto3BooleanField(this, 4, value);
    };
    proto.Request.EvaluateAll.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 5, false)
      );
    };
    proto.Request.EvaluateAll.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 5, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Request.ElementStyle.prototype.toObject = function(opt_includeInstance) {
        return proto.Request.ElementStyle.toObject(opt_includeInstance, this);
      };
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
    proto.Request.ElementStyle.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Request.ElementStyle();
      return proto.Request.ElementStyle.deserializeBinaryFromReader(msg, reader);
    };
    proto.Request.ElementStyle.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setSelector(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setPseudo(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setStylekey(value);
            break;
          case 4:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setStrict(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Request.ElementStyle.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Request.ElementStyle.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Request.ElementStyle.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Request.ElementStyle.prototype.getSelector = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Request.ElementStyle.prototype.setSelector = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Request.ElementStyle.prototype.getPseudo = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Request.ElementStyle.prototype.setPseudo = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Request.ElementStyle.prototype.getStylekey = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Request.ElementStyle.prototype.setStylekey = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Request.ElementStyle.prototype.getStrict = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 4, false)
      );
    };
    proto.Request.ElementStyle.prototype.setStrict = function(value) {
      return jspb.Message.setProto3BooleanField(this, 4, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Types.prototype.toObject = function(opt_includeInstance) {
        return proto.Types.toObject(opt_includeInstance, this);
      };
      proto.Types.toObject = function(includeInstance, msg) {
        var f, obj = {};
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Types.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Types();
      return proto.Types.deserializeBinaryFromReader(msg, reader);
    };
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
    proto.Types.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Types.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Types.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Types.SelectEntry.prototype.toObject = function(opt_includeInstance) {
        return proto.Types.SelectEntry.toObject(opt_includeInstance, this);
      };
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
    proto.Types.SelectEntry.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Types.SelectEntry();
      return proto.Types.SelectEntry.deserializeBinaryFromReader(msg, reader);
    };
    proto.Types.SelectEntry.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setValue(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLabel(value);
            break;
          case 4:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setIndex(value);
            break;
          case 5:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setSelected(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Types.SelectEntry.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Types.SelectEntry.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Types.SelectEntry.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Types.SelectEntry.prototype.getValue = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Types.SelectEntry.prototype.setValue = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Types.SelectEntry.prototype.getLabel = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Types.SelectEntry.prototype.setLabel = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Types.SelectEntry.prototype.getIndex = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 4, 0)
      );
    };
    proto.Types.SelectEntry.prototype.setIndex = function(value) {
      return jspb.Message.setProto3IntField(this, 4, value);
    };
    proto.Types.SelectEntry.prototype.getSelected = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 5, false)
      );
    };
    proto.Types.SelectEntry.prototype.setSelected = function(value) {
      return jspb.Message.setProto3BooleanField(this, 5, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.toObject(opt_includeInstance, this);
      };
      proto.Response.toObject = function(includeInstance, msg) {
        var f, obj = {};
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Response.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response();
      return proto.Response.deserializeBinaryFromReader(msg, reader);
    };
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
    proto.Response.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.Empty.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.Empty.toObject(opt_includeInstance, this);
      };
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
    proto.Response.Empty.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.Empty();
      return proto.Response.Empty.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.Empty.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLog(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.Empty.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.Empty.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.Empty.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getLog();
      if (f.length > 0) {
        writer.writeString(
          1,
          f
        );
      }
    };
    proto.Response.Empty.prototype.getLog = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Response.Empty.prototype.setLog = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.String.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.String.toObject(opt_includeInstance, this);
      };
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
    proto.Response.String.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.String();
      return proto.Response.String.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.String.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLog(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setBody(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.String.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.String.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.String.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Response.String.prototype.getLog = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Response.String.prototype.setLog = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Response.String.prototype.getBody = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Response.String.prototype.setBody = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Response.ListString.repeatedFields_ = [1];
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.ListString.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.ListString.toObject(opt_includeInstance, this);
      };
      proto.Response.ListString.toObject = function(includeInstance, msg) {
        var f, obj = {
          itemsList: (f = jspb.Message.getRepeatedField(msg, 1)) == null ? void 0 : f
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Response.ListString.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.ListString();
      return proto.Response.ListString.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.ListString.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.addItems(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.ListString.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.ListString.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.ListString.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getItemsList();
      if (f.length > 0) {
        writer.writeRepeatedString(
          1,
          f
        );
      }
    };
    proto.Response.ListString.prototype.getItemsList = function() {
      return (
        /** @type {!Array<string>} */
        jspb.Message.getRepeatedField(this, 1)
      );
    };
    proto.Response.ListString.prototype.setItemsList = function(value) {
      return jspb.Message.setField(this, 1, value || []);
    };
    proto.Response.ListString.prototype.addItems = function(value, opt_index) {
      return jspb.Message.addToRepeatedField(this, 1, value, opt_index);
    };
    proto.Response.ListString.prototype.clearItemsList = function() {
      return this.setItemsList([]);
    };
    proto.Response.Keywords.repeatedFields_ = [2, 3, 4];
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.Keywords.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.Keywords.toObject(opt_includeInstance, this);
      };
      proto.Response.Keywords.toObject = function(includeInstance, msg) {
        var f, obj = {
          log: jspb.Message.getFieldWithDefault(msg, 1, ""),
          keywordsList: (f = jspb.Message.getRepeatedField(msg, 2)) == null ? void 0 : f,
          keyworddocumentationsList: (f = jspb.Message.getRepeatedField(msg, 3)) == null ? void 0 : f,
          keywordargumentsList: (f = jspb.Message.getRepeatedField(msg, 4)) == null ? void 0 : f
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Response.Keywords.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.Keywords();
      return proto.Response.Keywords.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.Keywords.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLog(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.addKeywords(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.addKeyworddocumentations(value);
            break;
          case 4:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.addKeywordarguments(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.Keywords.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.Keywords.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.Keywords.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Response.Keywords.prototype.getLog = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Response.Keywords.prototype.setLog = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Response.Keywords.prototype.getKeywordsList = function() {
      return (
        /** @type {!Array<string>} */
        jspb.Message.getRepeatedField(this, 2)
      );
    };
    proto.Response.Keywords.prototype.setKeywordsList = function(value) {
      return jspb.Message.setField(this, 2, value || []);
    };
    proto.Response.Keywords.prototype.addKeywords = function(value, opt_index) {
      return jspb.Message.addToRepeatedField(this, 2, value, opt_index);
    };
    proto.Response.Keywords.prototype.clearKeywordsList = function() {
      return this.setKeywordsList([]);
    };
    proto.Response.Keywords.prototype.getKeyworddocumentationsList = function() {
      return (
        /** @type {!Array<string>} */
        jspb.Message.getRepeatedField(this, 3)
      );
    };
    proto.Response.Keywords.prototype.setKeyworddocumentationsList = function(value) {
      return jspb.Message.setField(this, 3, value || []);
    };
    proto.Response.Keywords.prototype.addKeyworddocumentations = function(value, opt_index) {
      return jspb.Message.addToRepeatedField(this, 3, value, opt_index);
    };
    proto.Response.Keywords.prototype.clearKeyworddocumentationsList = function() {
      return this.setKeyworddocumentationsList([]);
    };
    proto.Response.Keywords.prototype.getKeywordargumentsList = function() {
      return (
        /** @type {!Array<string>} */
        jspb.Message.getRepeatedField(this, 4)
      );
    };
    proto.Response.Keywords.prototype.setKeywordargumentsList = function(value) {
      return jspb.Message.setField(this, 4, value || []);
    };
    proto.Response.Keywords.prototype.addKeywordarguments = function(value, opt_index) {
      return jspb.Message.addToRepeatedField(this, 4, value, opt_index);
    };
    proto.Response.Keywords.prototype.clearKeywordargumentsList = function() {
      return this.setKeywordargumentsList([]);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.Bool.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.Bool.toObject(opt_includeInstance, this);
      };
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
    proto.Response.Bool.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.Bool();
      return proto.Response.Bool.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.Bool.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLog(value);
            break;
          case 2:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setBody(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.Bool.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.Bool.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.Bool.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Response.Bool.prototype.getLog = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Response.Bool.prototype.setLog = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Response.Bool.prototype.getBody = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 2, false)
      );
    };
    proto.Response.Bool.prototype.setBody = function(value) {
      return jspb.Message.setProto3BooleanField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.Int.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.Int.toObject(opt_includeInstance, this);
      };
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
    proto.Response.Int.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.Int();
      return proto.Response.Int.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.Int.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLog(value);
            break;
          case 2:
            var value = (
              /** @type {number} */
              reader.readInt32()
            );
            msg.setBody(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.Int.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.Int.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.Int.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Response.Int.prototype.getLog = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Response.Int.prototype.setLog = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Response.Int.prototype.getBody = function() {
      return (
        /** @type {number} */
        jspb.Message.getFieldWithDefault(this, 2, 0)
      );
    };
    proto.Response.Int.prototype.setBody = function(value) {
      return jspb.Message.setProto3IntField(this, 2, value);
    };
    proto.Response.Select.repeatedFields_ = [1];
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.Select.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.Select.toObject(opt_includeInstance, this);
      };
      proto.Response.Select.toObject = function(includeInstance, msg) {
        var f, obj = {
          entryList: jspb.Message.toObjectList(
            msg.getEntryList(),
            proto.Types.SelectEntry.toObject,
            includeInstance
          )
        };
        if (includeInstance) {
          obj.$jspbMessageInstance = msg;
        }
        return obj;
      };
    }
    proto.Response.Select.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.Select();
      return proto.Response.Select.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.Select.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = new proto.Types.SelectEntry();
            reader.readMessage(value, proto.Types.SelectEntry.deserializeBinaryFromReader);
            msg.addEntry(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.Select.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.Select.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.Select.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
      f = message.getEntryList();
      if (f.length > 0) {
        writer.writeRepeatedMessage(
          1,
          f,
          proto.Types.SelectEntry.serializeBinaryToWriter
        );
      }
    };
    proto.Response.Select.prototype.getEntryList = function() {
      return (
        /** @type{!Array<!proto.Types.SelectEntry>} */
        jspb.Message.getRepeatedWrapperField(this, proto.Types.SelectEntry, 1)
      );
    };
    proto.Response.Select.prototype.setEntryList = function(value) {
      return jspb.Message.setRepeatedWrapperField(this, 1, value);
    };
    proto.Response.Select.prototype.addEntry = function(opt_value, opt_index) {
      return jspb.Message.addToRepeatedWrapperField(this, 1, opt_value, proto.Types.SelectEntry, opt_index);
    };
    proto.Response.Select.prototype.clearEntryList = function() {
      return this.setEntryList([]);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.Json.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.Json.toObject(opt_includeInstance, this);
      };
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
    proto.Response.Json.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.Json();
      return proto.Response.Json.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.Json.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLog(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setJson(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setBodypart(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.Json.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.Json.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.Json.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Response.Json.prototype.getLog = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Response.Json.prototype.setLog = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Response.Json.prototype.getJson = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Response.Json.prototype.setJson = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Response.Json.prototype.getBodypart = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Response.Json.prototype.setBodypart = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.JavascriptExecutionResult.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.JavascriptExecutionResult.toObject(opt_includeInstance, this);
      };
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
    proto.Response.JavascriptExecutionResult.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.JavascriptExecutionResult();
      return proto.Response.JavascriptExecutionResult.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.JavascriptExecutionResult.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLog(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setResult(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.JavascriptExecutionResult.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.JavascriptExecutionResult.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.JavascriptExecutionResult.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Response.JavascriptExecutionResult.prototype.getLog = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Response.JavascriptExecutionResult.prototype.setLog = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Response.JavascriptExecutionResult.prototype.getResult = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Response.JavascriptExecutionResult.prototype.setResult = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.NewContextResponse.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.NewContextResponse.toObject(opt_includeInstance, this);
      };
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
    proto.Response.NewContextResponse.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.NewContextResponse();
      return proto.Response.NewContextResponse.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.NewContextResponse.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setId(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLog(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setContextoptions(value);
            break;
          case 4:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setNewbrowser(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.NewContextResponse.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.NewContextResponse.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.NewContextResponse.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Response.NewContextResponse.prototype.getId = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Response.NewContextResponse.prototype.setId = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Response.NewContextResponse.prototype.getLog = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Response.NewContextResponse.prototype.setLog = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Response.NewContextResponse.prototype.getContextoptions = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Response.NewContextResponse.prototype.setContextoptions = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Response.NewContextResponse.prototype.getNewbrowser = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 4, false)
      );
    };
    proto.Response.NewContextResponse.prototype.setNewbrowser = function(value) {
      return jspb.Message.setProto3BooleanField(this, 4, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.NewPersistentContextResponse.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.NewPersistentContextResponse.toObject(opt_includeInstance, this);
      };
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
    proto.Response.NewPersistentContextResponse.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.NewPersistentContextResponse();
      return proto.Response.NewPersistentContextResponse.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.NewPersistentContextResponse.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setId(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLog(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setContextoptions(value);
            break;
          case 4:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setNewbrowser(value);
            break;
          case 5:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setVideo(value);
            break;
          case 6:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setPageid(value);
            break;
          case 7:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setBrowserid(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.NewPersistentContextResponse.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.NewPersistentContextResponse.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.NewPersistentContextResponse.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Response.NewPersistentContextResponse.prototype.getId = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Response.NewPersistentContextResponse.prototype.setId = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Response.NewPersistentContextResponse.prototype.getLog = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Response.NewPersistentContextResponse.prototype.setLog = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Response.NewPersistentContextResponse.prototype.getContextoptions = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Response.NewPersistentContextResponse.prototype.setContextoptions = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Response.NewPersistentContextResponse.prototype.getNewbrowser = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 4, false)
      );
    };
    proto.Response.NewPersistentContextResponse.prototype.setNewbrowser = function(value) {
      return jspb.Message.setProto3BooleanField(this, 4, value);
    };
    proto.Response.NewPersistentContextResponse.prototype.getVideo = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 5, "")
      );
    };
    proto.Response.NewPersistentContextResponse.prototype.setVideo = function(value) {
      return jspb.Message.setProto3StringField(this, 5, value);
    };
    proto.Response.NewPersistentContextResponse.prototype.getPageid = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 6, "")
      );
    };
    proto.Response.NewPersistentContextResponse.prototype.setPageid = function(value) {
      return jspb.Message.setProto3StringField(this, 6, value);
    };
    proto.Response.NewPersistentContextResponse.prototype.getBrowserid = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 7, "")
      );
    };
    proto.Response.NewPersistentContextResponse.prototype.setBrowserid = function(value) {
      return jspb.Message.setProto3StringField(this, 7, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.NewPageResponse.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.NewPageResponse.toObject(opt_includeInstance, this);
      };
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
    proto.Response.NewPageResponse.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.NewPageResponse();
      return proto.Response.NewPageResponse.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.NewPageResponse.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLog(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setBody(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setVideo(value);
            break;
          case 4:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setNewbrowser(value);
            break;
          case 5:
            var value = (
              /** @type {boolean} */
              reader.readBool()
            );
            msg.setNewcontext(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.NewPageResponse.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.NewPageResponse.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.NewPageResponse.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Response.NewPageResponse.prototype.getLog = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Response.NewPageResponse.prototype.setLog = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Response.NewPageResponse.prototype.getBody = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Response.NewPageResponse.prototype.setBody = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Response.NewPageResponse.prototype.getVideo = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Response.NewPageResponse.prototype.setVideo = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Response.NewPageResponse.prototype.getNewbrowser = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 4, false)
      );
    };
    proto.Response.NewPageResponse.prototype.setNewbrowser = function(value) {
      return jspb.Message.setProto3BooleanField(this, 4, value);
    };
    proto.Response.NewPageResponse.prototype.getNewcontext = function() {
      return (
        /** @type {boolean} */
        jspb.Message.getBooleanFieldWithDefault(this, 5, false)
      );
    };
    proto.Response.NewPageResponse.prototype.setNewcontext = function(value) {
      return jspb.Message.setProto3BooleanField(this, 5, value);
    };
    if (jspb.Message.GENERATE_TO_OBJECT) {
      proto.Response.PageReportResponse.prototype.toObject = function(opt_includeInstance) {
        return proto.Response.PageReportResponse.toObject(opt_includeInstance, this);
      };
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
    proto.Response.PageReportResponse.deserializeBinary = function(bytes) {
      var reader = new jspb.BinaryReader(bytes);
      var msg = new proto.Response.PageReportResponse();
      return proto.Response.PageReportResponse.deserializeBinaryFromReader(msg, reader);
    };
    proto.Response.PageReportResponse.deserializeBinaryFromReader = function(msg, reader) {
      while (reader.nextField()) {
        if (reader.isEndGroup()) {
          break;
        }
        var field = reader.getFieldNumber();
        switch (field) {
          case 1:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setLog(value);
            break;
          case 2:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setErrors(value);
            break;
          case 3:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setConsole(value);
            break;
          case 4:
            var value = (
              /** @type {string} */
              reader.readString()
            );
            msg.setPageid(value);
            break;
          default:
            reader.skipField();
            break;
        }
      }
      return msg;
    };
    proto.Response.PageReportResponse.prototype.serializeBinary = function() {
      var writer = new jspb.BinaryWriter();
      proto.Response.PageReportResponse.serializeBinaryToWriter(this, writer);
      return writer.getResultBuffer();
    };
    proto.Response.PageReportResponse.serializeBinaryToWriter = function(message, writer) {
      var f = void 0;
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
    proto.Response.PageReportResponse.prototype.getLog = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 1, "")
      );
    };
    proto.Response.PageReportResponse.prototype.setLog = function(value) {
      return jspb.Message.setProto3StringField(this, 1, value);
    };
    proto.Response.PageReportResponse.prototype.getErrors = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 2, "")
      );
    };
    proto.Response.PageReportResponse.prototype.setErrors = function(value) {
      return jspb.Message.setProto3StringField(this, 2, value);
    };
    proto.Response.PageReportResponse.prototype.getConsole = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 3, "")
      );
    };
    proto.Response.PageReportResponse.prototype.setConsole = function(value) {
      return jspb.Message.setProto3StringField(this, 3, value);
    };
    proto.Response.PageReportResponse.prototype.getPageid = function() {
      return (
        /** @type {string} */
        jspb.Message.getFieldWithDefault(this, 4, "")
      );
    };
    proto.Response.PageReportResponse.prototype.setPageid = function(value) {
      return jspb.Message.setProto3StringField(this, 4, value);
    };
    goog.object.extend(exports2, proto);
  }
});

// node/playwright-wrapper/generated/playwright_grpc_pb.js
var require_playwright_grpc_pb = __commonJS({
  "node/playwright-wrapper/generated/playwright_grpc_pb.js"(exports2) {
    "use strict";
    var grpc = require("@grpc/grpc-js");
    var playwright_pb = require_playwright_pb();
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
    var PlaywrightService2 = exports2.PlaywrightService = {
      ariaSnapShot: {
        path: "/Playwright/AriaSnapShot",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.AriaSnapShot,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_AriaSnapShot,
        requestDeserialize: deserialize_Request_AriaSnapShot,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      addCookie: {
        path: "/Playwright/AddCookie",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Json,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Json,
        requestDeserialize: deserialize_Request_Json,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      getCookies: {
        path: "/Playwright/GetCookies",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      deleteAllCookies: {
        path: "/Playwright/DeleteAllCookies",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      takeScreenshot: {
        path: "/Playwright/TakeScreenshot",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ScreenshotOptions,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_ScreenshotOptions,
        requestDeserialize: deserialize_Request_ScreenshotOptions,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      goTo: {
        path: "/Playwright/GoTo",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.UrlOptions,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_UrlOptions,
        requestDeserialize: deserialize_Request_UrlOptions,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      goBack: {
        path: "/Playwright/GoBack",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      goForward: {
        path: "/Playwright/GoForward",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      getTitle: {
        path: "/Playwright/GetTitle",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      getElementCount: {
        path: "/Playwright/GetElementCount",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.Int,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_Int,
        responseDeserialize: deserialize_Response_Int
      },
      typeText: {
        path: "/Playwright/TypeText",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.TypeText,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_TypeText,
        requestDeserialize: deserialize_Request_TypeText,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      fillText: {
        path: "/Playwright/FillText",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.FillText,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_FillText,
        requestDeserialize: deserialize_Request_FillText,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      clearText: {
        path: "/Playwright/ClearText",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ClearText,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ClearText,
        requestDeserialize: deserialize_Request_ClearText,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      getDomProperty: {
        path: "/Playwright/GetDomProperty",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementProperty,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_ElementProperty,
        requestDeserialize: deserialize_Request_ElementProperty,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      getText: {
        path: "/Playwright/GetText",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      getElementAttribute: {
        path: "/Playwright/GetElementAttribute",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementProperty,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_ElementProperty,
        requestDeserialize: deserialize_Request_ElementProperty,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      getBoolProperty: {
        path: "/Playwright/GetBoolProperty",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementProperty,
        responseType: playwright_pb.Response.Bool,
        requestSerialize: serialize_Request_ElementProperty,
        requestDeserialize: deserialize_Request_ElementProperty,
        responseSerialize: serialize_Response_Bool,
        responseDeserialize: deserialize_Response_Bool
      },
      getViewportSize: {
        path: "/Playwright/GetViewportSize",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      getUrl: {
        path: "/Playwright/GetUrl",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      getPageSource: {
        path: "/Playwright/GetPageSource",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      press: {
        path: "/Playwright/Press",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.PressKeys,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_PressKeys,
        requestDeserialize: deserialize_Request_PressKeys,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      getSelectContent: {
        path: "/Playwright/GetSelectContent",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.Select,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_Select,
        responseDeserialize: deserialize_Response_Select
      },
      selectOption: {
        path: "/Playwright/SelectOption",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.SelectElementSelector,
        responseType: playwright_pb.Response.Select,
        requestSerialize: serialize_Request_SelectElementSelector,
        requestDeserialize: deserialize_Request_SelectElementSelector,
        responseSerialize: serialize_Response_Select,
        responseDeserialize: deserialize_Response_Select
      },
      deselectOption: {
        path: "/Playwright/DeselectOption",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      checkCheckbox: {
        path: "/Playwright/CheckCheckbox",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      uncheckCheckbox: {
        path: "/Playwright/UncheckCheckbox",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      health: {
        path: "/Playwright/Health",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      getElement: {
        path: "/Playwright/GetElement",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      getElements: {
        path: "/Playwright/GetElements",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      getByX: {
        path: "/Playwright/GetByX",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.GetByOptions,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_GetByOptions,
        requestDeserialize: deserialize_Request_GetByOptions,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      getElementStates: {
        path: "/Playwright/GetElementStates",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      setTimeout: {
        path: "/Playwright/SetTimeout",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Timeout,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Timeout,
        requestDeserialize: deserialize_Request_Timeout,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      addStyleTag: {
        path: "/Playwright/AddStyleTag",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.StyleTag,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_StyleTag,
        requestDeserialize: deserialize_Request_StyleTag,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      highlightElements: {
        path: "/Playwright/HighlightElements",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelectorWithDuration,
        responseType: playwright_pb.Response.Int,
        requestSerialize: serialize_Request_ElementSelectorWithDuration,
        requestDeserialize: deserialize_Request_ElementSelectorWithDuration,
        responseSerialize: serialize_Response_Int,
        responseDeserialize: deserialize_Response_Int
      },
      download: {
        path: "/Playwright/Download",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.DownloadOptions,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_DownloadOptions,
        requestDeserialize: deserialize_Request_DownloadOptions,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      click: {
        path: "/Playwright/Click",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelectorWithOptions,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ElementSelectorWithOptions,
        requestDeserialize: deserialize_Request_ElementSelectorWithOptions,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      tap: {
        path: "/Playwright/Tap",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelectorWithOptions,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ElementSelectorWithOptions,
        requestDeserialize: deserialize_Request_ElementSelectorWithOptions,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      hover: {
        path: "/Playwright/Hover",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelectorWithOptions,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ElementSelectorWithOptions,
        requestDeserialize: deserialize_Request_ElementSelectorWithOptions,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      focus: {
        path: "/Playwright/Focus",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      waitForElementsState: {
        path: "/Playwright/WaitForElementsState",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelectorWithOptions,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ElementSelectorWithOptions,
        requestDeserialize: deserialize_Request_ElementSelectorWithOptions,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      waitForFunction: {
        path: "/Playwright/WaitForFunction",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.WaitForFunctionOptions,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_WaitForFunctionOptions,
        requestDeserialize: deserialize_Request_WaitForFunctionOptions,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      evaluateJavascript: {
        path: "/Playwright/EvaluateJavascript",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.EvaluateAll,
        responseType: playwright_pb.Response.JavascriptExecutionResult,
        requestSerialize: serialize_Request_EvaluateAll,
        requestDeserialize: deserialize_Request_EvaluateAll,
        responseSerialize: serialize_Response_JavascriptExecutionResult,
        responseDeserialize: deserialize_Response_JavascriptExecutionResult
      },
      recordSelector: {
        path: "/Playwright/RecordSelector",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Label,
        responseType: playwright_pb.Response.JavascriptExecutionResult,
        requestSerialize: serialize_Request_Label,
        requestDeserialize: deserialize_Request_Label,
        responseSerialize: serialize_Response_JavascriptExecutionResult,
        responseDeserialize: deserialize_Response_JavascriptExecutionResult
      },
      setViewportSize: {
        path: "/Playwright/SetViewportSize",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Viewport,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Viewport,
        requestDeserialize: deserialize_Request_Viewport,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      getStyle: {
        path: "/Playwright/GetStyle",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementStyle,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_ElementStyle,
        requestDeserialize: deserialize_Request_ElementStyle,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      getBoundingBox: {
        path: "/Playwright/GetBoundingBox",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      httpRequest: {
        path: "/Playwright/HttpRequest",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.HttpRequest,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_HttpRequest,
        requestDeserialize: deserialize_Request_HttpRequest,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      waitForRequest: {
        path: "/Playwright/WaitForRequest",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.HttpCapture,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_HttpCapture,
        requestDeserialize: deserialize_Request_HttpCapture,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      waitForDownload: {
        path: "/Playwright/WaitForDownload",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.DownloadOptions,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_DownloadOptions,
        requestDeserialize: deserialize_Request_DownloadOptions,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      waitForNavigation: {
        path: "/Playwright/WaitForNavigation",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.UrlOptions,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_UrlOptions,
        requestDeserialize: deserialize_Request_UrlOptions,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      waitForPageLoadState: {
        path: "/Playwright/WaitForPageLoadState",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.PageLoadState,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_PageLoadState,
        requestDeserialize: deserialize_Request_PageLoadState,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      setGeolocation: {
        path: "/Playwright/SetGeolocation",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Json,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Json,
        requestDeserialize: deserialize_Request_Json,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      getDevice: {
        path: "/Playwright/GetDevice",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Device,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_Device,
        requestDeserialize: deserialize_Request_Device,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      getDevices: {
        path: "/Playwright/GetDevices",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      addLocatorHandlerCustom: {
        path: "/Playwright/AddLocatorHandlerCustom",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.LocatorHandlerAddCustom,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_LocatorHandlerAddCustom,
        requestDeserialize: deserialize_Request_LocatorHandlerAddCustom,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      removeLocatorHandler: {
        path: "/Playwright/RemoveLocatorHandler",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.LocatorHandlerRemove,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_LocatorHandlerRemove,
        requestDeserialize: deserialize_Request_LocatorHandlerRemove,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      handleAlert: {
        path: "/Playwright/HandleAlert",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.AlertAction,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_AlertAction,
        requestDeserialize: deserialize_Request_AlertAction,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      waitForAlerts: {
        path: "/Playwright/WaitForAlerts",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.AlertActions,
        responseType: playwright_pb.Response.ListString,
        requestSerialize: serialize_Request_AlertActions,
        requestDeserialize: deserialize_Request_AlertActions,
        responseSerialize: serialize_Response_ListString,
        responseDeserialize: deserialize_Response_ListString
      },
      mouseButton: {
        path: "/Playwright/MouseButton",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.MouseButtonOptions,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_MouseButtonOptions,
        requestDeserialize: deserialize_Request_MouseButtonOptions,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      mouseMove: {
        path: "/Playwright/MouseMove",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Json,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Json,
        requestDeserialize: deserialize_Request_Json,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      mouseWheel: {
        path: "/Playwright/MouseWheel",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.MouseWheel,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_MouseWheel,
        requestDeserialize: deserialize_Request_MouseWheel,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      keyboardKey: {
        path: "/Playwright/KeyboardKey",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.KeyboardKeypress,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_KeyboardKeypress,
        requestDeserialize: deserialize_Request_KeyboardKeypress,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      keyboardInput: {
        path: "/Playwright/KeyboardInput",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.KeyboardInputOptions,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_KeyboardInputOptions,
        requestDeserialize: deserialize_Request_KeyboardInputOptions,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      getTableRowIndex: {
        path: "/Playwright/GetTableRowIndex",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.Int,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_Int,
        responseDeserialize: deserialize_Response_Int
      },
      getTableCellIndex: {
        path: "/Playwright/GetTableCellIndex",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.Int,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_Int,
        responseDeserialize: deserialize_Response_Int
      },
      uploadFile: {
        path: "/Playwright/UploadFile",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.FilePath,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_FilePath,
        requestDeserialize: deserialize_Request_FilePath,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      scrollToElement: {
        path: "/Playwright/ScrollToElement",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElementSelector,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ElementSelector,
        requestDeserialize: deserialize_Request_ElementSelector,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      setOffline: {
        path: "/Playwright/SetOffline",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Bool,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Bool,
        requestDeserialize: deserialize_Request_Bool,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      reload: {
        path: "/Playwright/Reload",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Json,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Json,
        requestDeserialize: deserialize_Request_Json,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      switchPage: {
        path: "/Playwright/SwitchPage",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.IdWithTimeout,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_IdWithTimeout,
        requestDeserialize: deserialize_Request_IdWithTimeout,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      switchContext: {
        path: "/Playwright/SwitchContext",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Index,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_Index,
        requestDeserialize: deserialize_Request_Index,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      switchBrowser: {
        path: "/Playwright/SwitchBrowser",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Index,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_Index,
        requestDeserialize: deserialize_Request_Index,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      newPage: {
        path: "/Playwright/NewPage",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.UrlOptions,
        responseType: playwright_pb.Response.NewPageResponse,
        requestSerialize: serialize_Request_UrlOptions,
        requestDeserialize: deserialize_Request_UrlOptions,
        responseSerialize: serialize_Response_NewPageResponse,
        responseDeserialize: deserialize_Response_NewPageResponse
      },
      newContext: {
        path: "/Playwright/NewContext",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Context,
        responseType: playwright_pb.Response.NewContextResponse,
        requestSerialize: serialize_Request_Context,
        requestDeserialize: deserialize_Request_Context,
        responseSerialize: serialize_Response_NewContextResponse,
        responseDeserialize: deserialize_Response_NewContextResponse
      },
      newBrowser: {
        path: "/Playwright/NewBrowser",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Browser,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_Browser,
        requestDeserialize: deserialize_Request_Browser,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      launchBrowserServer: {
        path: "/Playwright/LaunchBrowserServer",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Browser,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_Browser,
        requestDeserialize: deserialize_Request_Browser,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      closeBrowserServer: {
        path: "/Playwright/CloseBrowserServer",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ConnectBrowser,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ConnectBrowser,
        requestDeserialize: deserialize_Request_ConnectBrowser,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      newPersistentContext: {
        path: "/Playwright/NewPersistentContext",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.PersistentContext,
        responseType: playwright_pb.Response.NewPersistentContextResponse,
        requestSerialize: serialize_Request_PersistentContext,
        requestDeserialize: deserialize_Request_PersistentContext,
        responseSerialize: serialize_Response_NewPersistentContextResponse,
        responseDeserialize: deserialize_Response_NewPersistentContextResponse
      },
      launchElectron: {
        path: "/Playwright/LaunchElectron",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ElectronLaunch,
        responseType: playwright_pb.Response.NewPersistentContextResponse,
        requestSerialize: serialize_Request_ElectronLaunch,
        requestDeserialize: deserialize_Request_ElectronLaunch,
        responseSerialize: serialize_Response_NewPersistentContextResponse,
        responseDeserialize: deserialize_Response_NewPersistentContextResponse
      },
      closeElectron: {
        path: "/Playwright/CloseElectron",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      connectToBrowser: {
        path: "/Playwright/ConnectToBrowser",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ConnectBrowser,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_ConnectBrowser,
        requestDeserialize: deserialize_Request_ConnectBrowser,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      closeBrowser: {
        path: "/Playwright/CloseBrowser",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      closeAllBrowsers: {
        path: "/Playwright/CloseAllBrowsers",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      closeContext: {
        path: "/Playwright/CloseContext",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Bool,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Bool,
        requestDeserialize: deserialize_Request_Bool,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      closePage: {
        path: "/Playwright/ClosePage",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ClosePage,
        responseType: playwright_pb.Response.PageReportResponse,
        requestSerialize: serialize_Request_ClosePage,
        requestDeserialize: deserialize_Request_ClosePage,
        responseSerialize: serialize_Response_PageReportResponse,
        responseDeserialize: deserialize_Response_PageReportResponse
      },
      openTraceGroup: {
        path: "/Playwright/OpenTraceGroup",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.TraceGroup,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_TraceGroup,
        requestDeserialize: deserialize_Request_TraceGroup,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      closeTraceGroup: {
        path: "/Playwright/CloseTraceGroup",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      getConsoleLog: {
        path: "/Playwright/GetConsoleLog",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Bool,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_Bool,
        requestDeserialize: deserialize_Request_Bool,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      getErrorMessages: {
        path: "/Playwright/GetErrorMessages",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Bool,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_Bool,
        requestDeserialize: deserialize_Request_Bool,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      getBrowserCatalog: {
        path: "/Playwright/GetBrowserCatalog",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Bool,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_Bool,
        requestDeserialize: deserialize_Request_Bool,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      getDownloadState: {
        path: "/Playwright/GetDownloadState",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.DownloadID,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_DownloadID,
        requestDeserialize: deserialize_Request_DownloadID,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      cancelDownload: {
        path: "/Playwright/CancelDownload",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.DownloadID,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_DownloadID,
        requestDeserialize: deserialize_Request_DownloadID,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      saveStorageState: {
        path: "/Playwright/SaveStorageState",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.FilePath,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_FilePath,
        requestDeserialize: deserialize_Request_FilePath,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      grantPermissions: {
        path: "/Playwright/GrantPermissions",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Permissions,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Permissions,
        requestDeserialize: deserialize_Request_Permissions,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      executePlaywright: {
        path: "/Playwright/ExecutePlaywright",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Json,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Json,
        requestDeserialize: deserialize_Request_Json,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      clearPermissions: {
        path: "/Playwright/ClearPermissions",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      initializeExtension: {
        path: "/Playwright/InitializeExtension",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.FilePath,
        responseType: playwright_pb.Response.Keywords,
        requestSerialize: serialize_Request_FilePath,
        requestDeserialize: deserialize_Request_FilePath,
        responseSerialize: serialize_Response_Keywords,
        responseDeserialize: deserialize_Response_Keywords
      },
      setPeerId: {
        path: "/Playwright/SetPeerId",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Index,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_Index,
        requestDeserialize: deserialize_Request_Index,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      pdf: {
        path: "/Playwright/Pdf",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Pdf,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_Pdf,
        requestDeserialize: deserialize_Request_Pdf,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      emulateMedia: {
        path: "/Playwright/EmulateMedia",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.EmulateMedia,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_EmulateMedia,
        requestDeserialize: deserialize_Request_EmulateMedia,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      setTime: {
        path: "/Playwright/SetTime",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ClockSetTime,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ClockSetTime,
        requestDeserialize: deserialize_Request_ClockSetTime,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      clockResume: {
        path: "/Playwright/ClockResume",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      clockPauseAt: {
        path: "/Playwright/ClockPauseAt",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ClockSetTime,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ClockSetTime,
        requestDeserialize: deserialize_Request_ClockSetTime,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      advanceClock: {
        path: "/Playwright/AdvanceClock",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.ClockAdvance,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_ClockAdvance,
        requestDeserialize: deserialize_Request_ClockAdvance,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      startCoverage: {
        path: "/Playwright/StartCoverage",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.CoverageStart,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_CoverageStart,
        requestDeserialize: deserialize_Request_CoverageStart,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      stopCoverage: {
        path: "/Playwright/StopCoverage",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.Empty,
        responseType: playwright_pb.Response.String,
        requestSerialize: serialize_Request_Empty,
        requestDeserialize: deserialize_Request_Empty,
        responseSerialize: serialize_Response_String,
        responseDeserialize: deserialize_Response_String
      },
      mergeCoverage: {
        path: "/Playwright/MergeCoverage",
        requestStream: false,
        responseStream: false,
        requestType: playwright_pb.Request.CoverageMerge,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_CoverageMerge,
        requestDeserialize: deserialize_Request_CoverageMerge,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      },
      waitForResponse: {
        path: "/Playwright/WaitForResponse",
        requestStream: false,
        responseStream: true,
        requestType: playwright_pb.Request.HttpCapture,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_HttpCapture,
        requestDeserialize: deserialize_Request_HttpCapture,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      callExtensionKeyword: {
        path: "/Playwright/CallExtensionKeyword",
        requestStream: false,
        responseStream: true,
        requestType: playwright_pb.Request.KeywordCall,
        responseType: playwright_pb.Response.Json,
        requestSerialize: serialize_Request_KeywordCall,
        requestDeserialize: deserialize_Request_KeywordCall,
        responseSerialize: serialize_Response_Json,
        responseDeserialize: deserialize_Response_Json
      },
      uploadFileBySelector: {
        path: "/Playwright/UploadFileBySelector",
        requestStream: true,
        responseStream: false,
        requestType: playwright_pb.Request.FileBySelector,
        responseType: playwright_pb.Response.Empty,
        requestSerialize: serialize_Request_FileBySelector,
        requestDeserialize: deserialize_Request_FileBySelector,
        responseSerialize: serialize_Response_Empty,
        responseDeserialize: deserialize_Response_Empty
      }
    };
    exports2.PlaywrightClient = grpc.makeGenericClientConstructor(PlaywrightService2, "Playwright", {});
  }
});

// node/playwright-wrapper/response-util.ts
var import_playwright_pb = __toESM(require_playwright_pb());
var import_playwright = require("playwright");
var import_grpc_js = require("@grpc/grpc-js");
function emptyWithLog(text) {
  const response = new import_playwright_pb.Response.Empty();
  response.setLog(text);
  return response;
}
function pageReportResponse(log, page) {
  const response = new import_playwright_pb.Response.PageReportResponse();
  response.setLog(log);
  response.setConsole(
    JSON.stringify(
      page.consoleMessages.map((m) => ({
        time: m.time,
        type: m.type,
        text: m.text,
        location: m.location
      }))
    )
  );
  response.setErrors(
    JSON.stringify(page.pageErrors.map((e) => e ? `${e.name}: ${e.message}
${e.stack}` : "unknown error"))
  );
  response.setPageid(page.id);
  return response;
}
function getConsoleLogResponse(page, fullLog, message) {
  const response = new import_playwright_pb.Response.Json();
  const consoleMessages = page.consoleMessages;
  const reponseMessages = fullLog ? consoleMessages : consoleMessages.slice(page.consoleIndex);
  page.consoleIndex = consoleMessages.length;
  response.setLog(message);
  response.setJson(JSON.stringify(reponseMessages));
  return response;
}
function getErrorMessagesResponse(page, fullLog, message) {
  const response = new import_playwright_pb.Response.Json();
  const pageErrors = page.pageErrors;
  const reponseErrors = fullLog ? pageErrors : pageErrors.slice(page.errorIndex);
  page.errorIndex = pageErrors.length;
  response.setLog(message);
  response.setJson(JSON.stringify(reponseErrors));
  return response;
}
function stringResponse(body, logMessage) {
  const response = new import_playwright_pb.Response.String();
  response.setBody(body);
  response.setLog(logMessage);
  return response;
}
function jsonResponse(body, logMessage, bodyPart = "") {
  const response = new import_playwright_pb.Response.Json();
  response.setJson(body);
  response.setLog(logMessage);
  response.setBodypart(bodyPart);
  return response;
}
function intResponse(body, logMessage) {
  const response = new import_playwright_pb.Response.Int();
  response.setBody(body);
  response.setLog(logMessage);
  return response;
}
function boolResponse(value, logMessage) {
  const response = new import_playwright_pb.Response.Bool();
  response.setBody(value);
  response.setLog(logMessage);
  return response;
}
function jsResponse(result, logMessage) {
  const response = new import_playwright_pb.Response.JavascriptExecutionResult();
  response.setResult(JSON.stringify(result));
  response.setLog(logMessage);
  return response;
}
function errorResponse(e) {
  console.log("================= Original suppressed error =================");
  console.log(e);
  console.log("=============================================================");
  if (!(e instanceof Error)) return null;
  const errorMessage = e.toString().substring(0, 5e3);
  let errorCode = import_grpc_js.status.RESOURCE_EXHAUSTED;
  if (e instanceof import_playwright.errors.TimeoutError) {
    errorCode = import_grpc_js.status.DEADLINE_EXCEEDED;
  }
  return { code: errorCode, message: errorMessage };
}
function keywordsResponse(keywords, keywordArguments, keywordDocs, logMessage) {
  const response = new import_playwright_pb.Response.Keywords();
  response.setKeywordsList(keywords);
  response.setKeyworddocumentationsList(keywordDocs);
  response.setKeywordargumentsList(keywordArguments);
  response.setLog(logMessage);
  return response;
}
function parseRegExpOrKeepString(str) {
  const regex = /^\/(?<matcher>.*)\/(?<flags>[gimsuy]+)?$/;
  try {
    const match = str.match(regex);
    if (match) {
      const { matcher, flags } = match.groups;
      return new RegExp(matcher, flags);
    }
    return str;
  } catch (e) {
    return str;
  }
}

// node/playwright-wrapper/playwright-invoke.ts
var import_pino = require("pino");
var logger = (0, import_pino.pino)({ timestamp: import_pino.pino.stdTimeFunctions.isoTime });
async function findLocator(state2, selector, strictMode, nthLocator, firstOnly) {
  const activePage = state2.getActivePage();
  exists(activePage, "Could not find active page");
  if (strictMode) {
    selector = selector.replaceAll(" >>> ", " >> internal:control=enter-frame >> ");
  } else {
    selector = selector.replaceAll(" >>> ", " >> nth=0 >> internal:control=enter-frame >> ");
  }
  if (nthLocator !== void 0) {
    return await findNthLocator(activePage, selector, nthLocator);
  } else if (strictMode) {
    logger.info(`Strict mode is enabled, find Locator with ${selector} in page.`);
    return activePage.locator(selector);
  } else {
    return await findLocatorNotStrict(activePage, selector, firstOnly);
  }
}
async function findNthLocator(activePage, selector, nthLocator) {
  logger.info(`Find ${nthLocator} Locator in page.`);
  return activePage.locator(selector).nth(nthLocator);
}
async function findLocatorNotStrict(activePage, selector, firstOnly) {
  if (firstOnly) {
    logger.info(`Strict mode is disabled, return first Locator: ${selector} in page.`);
    return activePage.locator(selector).first();
  } else {
    logger.info(`Strict mode is disabled, return Locator: ${selector} in page.`);
    return activePage.locator(selector);
  }
}
async function invokeOnMouse(page, methodName, args2) {
  exists(page, `Tried to execute mouse action '${methodName}' but no open page`);
  logger.info(`Invoking mouse action ${methodName} with params ${JSON.stringify(args2)}`);
  const fn = page?.mouse[methodName].bind(page.mouse);
  exists(fn, `Bind failure with '${fn}'`);
  return await fn(...Object.values(args2));
}
async function invokeOnKeyboard(page, methodName, ...args2) {
  logger.info(`Invoking keyboard action ${methodName} with params ${JSON.stringify(args2)}`);
  const fn = page.keyboard[methodName].bind(page.keyboard);
  exists(fn, `Bind failure with '${fn}'`);
  return await fn(...Object.values(args2));
}
function exists(obj, message) {
  if (!obj) {
    throw new Error(message);
  }
}

// node/playwright-wrapper/browser_logger.ts
var import_pino2 = require("pino");
var logger2 = (0, import_pino2.pino)({
  timestamp: import_pino2.stdTimeFunctions.isoTime,
  level: process.env.ROBOT_FRAMEWORK_BROWSER_PINO_LOG_LEVEL || "info"
});

// node/playwright-wrapper/browser-control.ts
var { program: pwProgram } = require("playwright-core/lib/cli/program");
async function executePlaywright(request2) {
  const args2 = JSON.parse(request2.getBody());
  pwProgram.exitOverride();
  await pwProgram.parseAsync(args2, { from: "user" });
  return emptyWithLog("Executed Playwright command: " + args2.join(" "));
}
async function grantPermissions(request2, state2) {
  const browserContext = state2.getActiveContext();
  if (!browserContext) {
    return emptyWithLog(`No browser context is active. Use 'Open Browser' to open a new one.`);
  }
  await browserContext.grantPermissions(request2.getPermissionsList(), {
    ...request2.getOrigin().length > 0 && { origin: request2.getOrigin() }
  });
  return emptyWithLog(
    `Granted permissions "${request2.getPermissionsList().join(", ")}"` + (request2.getOrigin().length > 0 ? ` for origin "${request2.getOrigin()}"` : "")
  );
}
async function clearPermissions(request2, state2) {
  const browserContext = state2.getActiveContext();
  if (!browserContext) {
    return emptyWithLog(`No browser context is active. Use 'Open Browser' to open a new one.`);
  }
  await browserContext.clearPermissions();
  return emptyWithLog("Cleared all permissions");
}
async function goTo(request2, page) {
  const url = request2.getUrl()?.getUrl() || "about:blank";
  const timeout = request2.getUrl()?.getDefaulttimeout();
  const goToOptions = { timeout };
  const waitUntil = request2.getWaituntil();
  if (waitUntil) {
    goToOptions.waitUntil = waitUntil;
  }
  const response = await page.goto(url, goToOptions);
  return stringResponse(response?.status().toString() || "", `Successfully opened URL ${url}`);
}
async function takeScreenshot(request2, state2) {
  const selector = request2.getSelector();
  const options2 = JSON.parse(request2.getOptions());
  const mask = JSON.parse(request2.getMask());
  const strictMode = request2.getStrict();
  const page = state2.getActivePage();
  exists(page, "Tried to take screenshot, but no page was open.");
  if (mask) {
    const mask_locators = [];
    for (const sel of mask) {
      mask_locators.push(await findLocator(state2, sel, false, void 0, false));
    }
    options2.mask = mask_locators;
  }
  logger2.info({ "Take screenshot with options: ": options2 });
  if (selector) {
    logger2.info({ "Using selecotr: ": selector });
    const locator = await findLocator(state2, selector, strictMode, void 0, true);
    await locator.screenshot(options2);
  } else {
    await page.screenshot(options2);
  }
  const message = "Screenshot successfully captured to: " + options2.path;
  return stringResponse(options2.path, message);
}
async function setTimeout2(request2, context) {
  if (!context) {
    return emptyWithLog(`No context open.`);
  }
  const timeout = request2.getTimeout();
  context.setDefaultTimeout(timeout);
  return emptyWithLog(`Set timeout to: ${timeout}`);
}
async function setViewportSize(request2, page) {
  const size = { width: request2.getWidth(), height: request2.getHeight() };
  await page.setViewportSize(size);
  return emptyWithLog(`Set viewport size to: ${size}`);
}
async function setOffline(request2, context) {
  exists(context, "Tried to toggle context to offline, no open context");
  const offline = request2.getValue();
  await context.setOffline(offline);
  return emptyWithLog(`Set context to ${offline}`);
}
async function reload(page, body) {
  const options2 = JSON.parse(body);
  logger2.info(`Reload page with options: ${body}`);
  await page.reload(options2);
  return emptyWithLog(`Reloaded page with options: ${body}`);
}
async function setGeolocation(request2, context) {
  const geolocation = JSON.parse(request2.getBody());
  await context?.setGeolocation(geolocation);
  return emptyWithLog("Geolocation set to: " + JSON.stringify(geolocation));
}

// node/playwright-wrapper/clock.ts
var import_pino3 = __toESM(require("pino"));
var logger3 = (0, import_pino3.default)({ timestamp: import_pino3.default.stdTimeFunctions.isoTime });
async function setTime(request2, state2) {
  const activePage = state2.getActivePage();
  exists(activePage, "Could not find active page");
  let time = request2.getTime();
  time = time * 1e3;
  const clockType = request2.getSettype();
  const setTime2 = new Date(time).toISOString();
  if (clockType === "fixed") {
    logger3.info(`Setting time to ${time} ${setTime2} as fixed`);
    activePage.clock.setFixedTime(time);
  } else if (clockType === "system") {
    logger3.info(`Setting time to ${time} ${setTime2} as system`);
    activePage.clock.setSystemTime(time);
  } else if (clockType === "install") {
    logger3.info(`Setting time to ${time} ${setTime2} as install`);
    activePage.clock.install({ time });
  } else {
    logger3.info(`Invalid clock type ${clockType}`);
    return emptyWithLog("Invalid clock type");
  }
  return emptyWithLog(`Time set to ${setTime2} as ${clockType}`);
}
async function clockResume(request2, state2) {
  const activePage = state2.getActivePage();
  exists(activePage, "Could not find active page");
  activePage.clock.resume();
  return emptyWithLog("Clock resumed");
}
async function clockPauseAt(request2, state2) {
  const activePage = state2.getActivePage();
  exists(activePage, "Could not find active page");
  let time = request2.getTime();
  time = time * 1e3;
  const setTime2 = new Date(time).toISOString();
  logger3.info(`Pausing clock at ${time} ${setTime2}`);
  await activePage.clock.pauseAt(time);
  return emptyWithLog(`Clock paused at ${setTime2}`);
}
async function advanceClock(request2, state2) {
  const activePage = state2.getActivePage();
  exists(activePage, "Could not find active page");
  const time = request2.getTime();
  const timeMs = time * 1e3;
  const advanceType = request2.getAdvancetype();
  logger3.info(`Advancing clock by ${timeMs} ${advanceType}`);
  if (advanceType === "fast_forward") {
    await activePage.clock.fastForward(timeMs);
  } else if (advanceType === "run_for") {
    await activePage.clock.runFor(timeMs);
  }
  return emptyWithLog(`Clock advanced by ${timeMs} seconds by ${advanceType}`);
}

// node/playwright-wrapper/cookie.ts
var import_pino4 = require("pino");
var logger4 = (0, import_pino4.pino)({ timestamp: import_pino4.pino.stdTimeFunctions.isoTime });
async function getCookies(context) {
  const allCookies = await context.cookies();
  logger4.info({ "Cookies: ": allCookies });
  const cookieName = [];
  for (const cookie of allCookies) {
    cookieName.push(cookie.name);
  }
  return jsonResponse(JSON.stringify(allCookies), cookieName.toString());
}
async function addCookie(request2, context) {
  const cookie = JSON.parse(request2.getBody());
  logger4.info({ "Cookie data: ": request2.getBody() });
  await context.addCookies([cookie]);
  return emptyWithLog('Cookie "' + cookie.name + '" added.');
}
async function deleteAllCookies(context) {
  await context.clearCookies();
  return emptyWithLog("All cookies deleted.");
}

// node/playwright-wrapper/device-descriptors.ts
var import_playwright2 = require("playwright");
function getDevice(request2) {
  const name2 = request2.getName();
  const device = import_playwright2.devices[name2];
  if (!device) throw new Error(`No device named ${name2}`);
  return jsonResponse(JSON.stringify(device), "");
}
function getDevices() {
  return jsonResponse(JSON.stringify(import_playwright2.devices), "");
}

// node/playwright-wrapper/evaluation.ts
var path2 = __toESM(require("path"));

// node/playwright-wrapper/network.ts
var path = __toESM(require("path"));

// node_modules/uuid/dist-node/stringify.js
var byteToHex = [];
for (let i = 0; i < 256; ++i) {
  byteToHex.push((i + 256).toString(16).slice(1));
}
function unsafeStringify(arr, offset = 0) {
  return (byteToHex[arr[offset + 0]] + byteToHex[arr[offset + 1]] + byteToHex[arr[offset + 2]] + byteToHex[arr[offset + 3]] + "-" + byteToHex[arr[offset + 4]] + byteToHex[arr[offset + 5]] + "-" + byteToHex[arr[offset + 6]] + byteToHex[arr[offset + 7]] + "-" + byteToHex[arr[offset + 8]] + byteToHex[arr[offset + 9]] + "-" + byteToHex[arr[offset + 10]] + byteToHex[arr[offset + 11]] + byteToHex[arr[offset + 12]] + byteToHex[arr[offset + 13]] + byteToHex[arr[offset + 14]] + byteToHex[arr[offset + 15]]).toLowerCase();
}

// node_modules/uuid/dist-node/rng.js
var import_node_crypto = require("node:crypto");
var rnds8Pool = new Uint8Array(256);
var poolPtr = rnds8Pool.length;
function rng() {
  if (poolPtr > rnds8Pool.length - 16) {
    (0, import_node_crypto.randomFillSync)(rnds8Pool);
    poolPtr = 0;
  }
  return rnds8Pool.slice(poolPtr, poolPtr += 16);
}

// node_modules/uuid/dist-node/native.js
var import_node_crypto2 = require("node:crypto");
var native_default = { randomUUID: import_node_crypto2.randomUUID };

// node_modules/uuid/dist-node/v4.js
function _v4(options2, buf, offset) {
  options2 = options2 || {};
  const rnds = options2.random ?? options2.rng?.() ?? rng();
  if (rnds.length < 16) {
    throw new Error("Random bytes length must be >= 16");
  }
  rnds[6] = rnds[6] & 15 | 64;
  rnds[8] = rnds[8] & 63 | 128;
  if (buf) {
    offset = offset || 0;
    if (offset < 0 || offset + 16 > buf.length) {
      throw new RangeError(`UUID byte range ${offset}:${offset + 15} is out of buffer bounds`);
    }
    for (let i = 0; i < 16; ++i) {
      buf[offset + i] = rnds[i];
    }
    return buf;
  }
  return unsafeStringify(rnds);
}
function v4(options2, buf, offset) {
  if (native_default.randomUUID && !buf && !options2) {
    return native_default.randomUUID();
  }
  return _v4(options2, buf, offset);
}
var v4_default = v4;

// node/playwright-wrapper/network.ts
var import_pino5 = require("pino");
var logger5 = (0, import_pino5.pino)({ timestamp: import_pino5.pino.stdTimeFunctions.isoTime });
async function httpRequest(request2, page) {
  const opts = {
    method: request2.getMethod(),
    url: request2.getUrl(),
    headers: JSON.parse(request2.getHeaders())
  };
  if (opts.method != "GET") {
    opts.body = request2.getBody();
  }
  const response = await page.evaluate(({ url, method, body, headers }) => {
    return fetch(url, { method, body, headers }).then((data) => {
      return data.text().then((body2) => {
        const headers2 = {};
        data.headers.forEach((value, name2) => headers2[name2] = value);
        return {
          status: data.status,
          body: body2,
          headers: JSON.stringify(headers2),
          type: data.type,
          statusText: data.statusText,
          url: data.url,
          ok: data.ok,
          redirected: data.redirected
        };
      });
    });
  }, opts);
  return jsonResponse(JSON.stringify(response), "Request performed successfully.");
}
function deserializeUrlOrPredicate(urlOrPredicate) {
  if (/^function.*{.*}$/.test(urlOrPredicate) || /([a-zA-Z]\w*|\([a-zA-Z]\w*(,\s*[a-zA-Z]\w*)*\)) =>/.test(urlOrPredicate)) {
    const fn = new Function(`return (${urlOrPredicate})`)();
    if (typeof fn === "function" || Object.prototype.toString.call(fn) === "[object Function]") {
      return fn;
    }
  }
  return parseRegExpOrKeepString(urlOrPredicate);
}
async function waitForResponse(request2, page) {
  const urlOrPredicate = deserializeUrlOrPredicate(request2.getUrlorpredicate());
  const timeout = request2.getTimeout();
  const data = await page.waitForResponse(urlOrPredicate, { timeout });
  let body = null;
  try {
    body = await data.text();
  } catch (e) {
    logger5.info(`Error reading response ${e}`);
  }
  const jsonData = JSON.stringify({
    status: data.status(),
    headers: JSON.stringify(data.headers()),
    statusText: data.statusText(),
    url: data.url(),
    ok: data.ok(),
    request: {
      headers: JSON.stringify(data.request().headers()),
      method: data.request().method(),
      postData: data.request().postData()
    }
  });
  const chunkSize = 35e5;
  const responseChunks = [];
  if (body && body.length > chunkSize) {
    logger5.info(`body.length: ${body.length}`);
    for (let i = 0; i < body.length; i += chunkSize) {
      const chunk = body.substring(i, i + chunkSize);
      const response = jsonResponse(jsonData, `Response received, chunk ${i}`, chunk);
      logger5.info(`chunked response: ${i}`);
      responseChunks.push(response);
    }
  } else {
    if (body !== null) {
      const response = jsonResponse(jsonData, "Response received", body);
      responseChunks.push(response);
    } else {
      const jsonDataMap = JSON.parse(jsonData);
      jsonDataMap.body = null;
      const response = jsonResponse(JSON.stringify(jsonDataMap), "Response received with empty body", "");
      responseChunks.push(response);
    }
  }
  logger5.info(`responseChunks.length: ${responseChunks.length}`);
  return responseChunks;
}
async function waitForRequest(request2, page) {
  const urlOrPredicate = deserializeUrlOrPredicate(request2.getUrlorpredicate());
  const timeout = request2.getTimeout();
  const result = await page.waitForRequest(urlOrPredicate, { timeout });
  return stringResponse(result.url(), "Request completed within timeout.");
}
async function waitForNavigation(request2, page) {
  const url = parseRegExpOrKeepString(request2.getUrl()?.getUrl());
  const timeout = request2.getUrl()?.getDefaulttimeout();
  const waitUntil = request2.getWaituntil();
  await page.waitForNavigation({ timeout, url, waitUntil });
  return emptyWithLog(`Navigated to: ${url}, location is: ${page.url()}`);
}
async function WaitForPageLoadState(request2, page) {
  const state2 = request2.getState();
  const timeout = request2.getTimeout();
  logger5.info(`timeout: ${timeout} state: ${state2}`);
  await page.waitForLoadState(state2, { timeout });
  return emptyWithLog(`Load state ${state2} got in ${timeout}`);
}
async function waitForDownload(request2, state2, page) {
  const saveAs = request2.getPath();
  const waitForFinish = request2.getWaitforfinish();
  const downloadTimeout = request2.getDownloadtimeout();
  return await _waitForDownload(page, state2, saveAs, downloadTimeout, waitForFinish);
}
async function _waitForDownload(page, state2, saveAs, downloadTimeout, waitForFinished) {
  const downloadObject = await page.waitForEvent("download");
  const downloadsPath = state2.activeBrowser.browser?._options?.downloadsPath;
  if (downloadsPath && saveAs) {
    logger5.info("saveAs: " + path.resolve(downloadsPath, saveAs));
    if (!path.isAbsolute(saveAs)) {
      saveAs = path.resolve(downloadsPath, saveAs);
    }
  }
  const fileName = downloadObject.suggestedFilename();
  if (!waitForFinished) {
    const downloadID = v4_default();
    const activeIndexedPage = state2.activeBrowser?.page;
    if (activeIndexedPage) {
      activeIndexedPage.activeDownloads.set(downloadID, {
        downloadObject,
        suggestedFilename: fileName,
        saveAs
      });
      return jsonResponse(
        JSON.stringify({
          saveAs: "",
          suggestedFilename: fileName,
          state: "in_progress",
          downloadID
        }),
        "Download started successfully."
      );
    } else {
      throw new Error("No active page found");
    }
  }
  if (downloadTimeout > 0) {
    const readStream = await Promise.race([
      downloadObject.createReadStream(),
      new Promise((resolve2) => setTimeout(resolve2, downloadTimeout))
    ]);
    if (!readStream) {
      downloadObject.cancel();
      throw new Error("Download failed, Timeout exceeded.");
    }
  }
  let filePath;
  if (saveAs) {
    await downloadObject.saveAs(saveAs);
    filePath = path.resolve(saveAs);
  } else {
    filePath = await downloadObject.path();
  }
  logger5.info("suggestedFilename: " + fileName + " saveAs path: " + filePath);
  return jsonResponse(
    JSON.stringify({ saveAs: filePath, suggestedFilename: fileName, state: "finished", downloadID: null }),
    "Download done successfully to: " + filePath
  );
}
async function getDownloadState(request2, state2) {
  const downloadID = request2.getId();
  const activeIndexedPage = state2.activeBrowser?.page;
  if (!activeIndexedPage) {
    throw new Error("No active page found");
  }
  const downloadInfo = activeIndexedPage.activeDownloads.get(downloadID);
  if (!downloadInfo) {
    throw new Error("No download object found for id: " + downloadID);
  }
  const downloadObject = downloadInfo.downloadObject;
  const suggestedFilename = downloadInfo.suggestedFilename;
  const failure = await Promise.race([downloadObject.failure(), new Promise((resolve2) => setTimeout(resolve2, 50))]);
  if (failure === null) {
    const saveAs = downloadInfo.saveAs;
    let filePath;
    if (saveAs) {
      await downloadObject.saveAs(saveAs);
      filePath = path.resolve(saveAs);
    } else {
      filePath = await downloadObject.path();
    }
    return jsonResponse(
      JSON.stringify({
        saveAs: filePath,
        suggestedFilename,
        state: "finished",
        downloadID
      }),
      "Download state received"
    );
  } else if (failure) {
    return jsonResponse(
      JSON.stringify({
        saveAs: "",
        suggestedFilename,
        state: failure,
        downloadID
      }),
      "Download state received"
    );
  } else {
    return jsonResponse(
      JSON.stringify({
        saveAs: "",
        suggestedFilename,
        state: "in_progress",
        downloadID
      }),
      "Download state received"
    );
  }
}
async function cancelDownload(request2, state2) {
  const downloadID = request2.getId();
  const activeIndexedPage = state2.activeBrowser?.page;
  if (!activeIndexedPage) {
    throw new Error("No active page found");
  }
  const downloadInfo = activeIndexedPage.activeDownloads.get(downloadID);
  if (!downloadInfo) {
    throw new Error("No download object found for id: " + downloadID);
  }
  const downloadObject = downloadInfo.downloadObject;
  downloadObject.cancel();
  const failure = await downloadObject.failure();
  if (failure == "canceled") {
    return emptyWithLog("Download canceled successfully.");
  } else if (failure === null) {
    return emptyWithLog("Canceling download not possible anymore, download finished.");
  } else {
    return emptyWithLog(`Canceling download not possible anymore, download ${failure}.`);
  }
}

// node/playwright-wrapper/evaluation.ts
var import_pino6 = require("pino");
var logger6 = (0, import_pino6.pino)({ timestamp: import_pino6.pino.stdTimeFunctions.isoTime });
async function getElement(request2, state2) {
  const strictMode = request2.getStrict();
  const selector = request2.getSelector();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  await locator.waitFor({ state: "attached" });
  return stringResponse(locator._selector, "Locator found successfully.");
}
async function getElements(request2, state2) {
  const selector = request2.getSelector();
  const locator = await findLocator(state2, selector, false, void 0, false);
  logger6.info(`Wait element to reach attached state.`);
  try {
    await locator.first().waitFor({ state: "attached" });
  } catch (e) {
    logger6.debug(`Attached state not reached, suppress error: ${e}.`);
  }
  const allLocators = await locator.all();
  logger6.info(`Found ${allLocators.length} elements.`);
  const allSelectors = allLocators.map((locator2) => locator2._selector);
  return jsonResponse(JSON.stringify(allSelectors), `Found ${allLocators} Locators successfully.`);
}
async function getByX(request2, state2) {
  const strategy = request2.getStrategy();
  const text = parseRegExpOrKeepString(request2.getText());
  const options2 = JSON.parse(request2.getOptions());
  const strictMode = request2.getStrict();
  const allElements = request2.getAll();
  const frameSelector = request2.getFrameselector();
  const activePage = state2.getActivePage();
  exists(activePage, "Could not find active page");
  let document2 = activePage;
  if (frameSelector) {
    document2 = activePage.frameLocator(frameSelector);
    if (!strictMode) {
      document2 = document2.first();
    }
  }
  let locator = null;
  switch (strategy) {
    case "AltText": {
      locator = document2.getByAltText(text, options2);
      break;
    }
    case "Label": {
      locator = document2.getByLabel(text, options2);
      break;
    }
    case "Placeholder": {
      locator = document2.getByPlaceholder(text, options2);
      break;
    }
    case "Role": {
      if (options2?.name) {
        options2.name = parseRegExpOrKeepString(options2.name);
      }
      locator = document2.getByRole(text, options2);
      break;
    }
    case "TestId": {
      locator = document2.getByTestId(text);
      break;
    }
    case "Text": {
      locator = document2.getByText(text, options2);
      break;
    }
    case "Title": {
      locator = document2.getByTitle(text, options2);
      break;
    }
    default: {
      throw new Error(`Strategy ${strategy} not supported.`);
    }
  }
  if (!allElements) {
    if (!strictMode) {
      locator = locator.first();
    }
    await locator.waitFor({ state: "attached" });
    return jsonResponse(JSON.stringify(locator._selector), "Locator found successfully.");
  }
  let allSelectors = [];
  try {
    await locator.first().waitFor({ state: "attached" });
    allSelectors = await locator.all().then((locators) => locators.map((loc) => loc._selector));
  } catch (e) {
    logger6.debug(`Attached state not reached, suppress error: ${e}.`);
  }
  return jsonResponse(JSON.stringify(allSelectors), `${allSelectors.length} locators found successfully.`);
}
var tryToTransformStringToFunction = (str) => {
  try {
    return new Function("return " + str)();
  } catch (ignored) {
    logger6.debug(`Failed to transform string to function: ${ignored}`);
    return str;
  }
};
async function evaluateJavascript(request2, state2, page) {
  const selector = request2.getSelector();
  const script = tryToTransformStringToFunction(request2.getScript());
  const strictMode = request2.getStrict();
  const arg = JSON.parse(request2.getArg());
  const allElements = request2.getAllelements();
  async function getJSResult() {
    if (selector !== "") {
      const locator = await findLocator(state2, selector, strictMode, void 0, !allElements);
      if (allElements) {
        return await locator.evaluateAll(script, arg);
      }
      return await locator.evaluate(script, arg);
    }
    return await page.evaluate(script, arg);
  }
  return jsResponse(await getJSResult(), "JavaScript executed successfully.");
}
async function waitForElementState(request2, pwState) {
  const selector = request2.getSelector();
  const { state: state2, timeout } = JSON.parse(request2.getOptions());
  const strictMode = request2.getStrict();
  const locator = await findLocator(pwState, selector, strictMode, void 0, true);
  if (state2 === "detached" || state2 === "attached" || state2 === "hidden" || state2 === "visible") {
    await locator.waitFor({ state: state2, timeout });
  } else {
    const element = await locator.elementHandle({ timeout });
    await element?.waitForElementState(state2, { timeout });
  }
  return emptyWithLog(`Waited for Element with selector ${selector} at state ${state2}`);
}
async function waitForFunction(request2, state2, page) {
  const script = tryToTransformStringToFunction(request2.getScript());
  const selector = request2.getSelector();
  const options2 = JSON.parse(request2.getOptions());
  const strictMode = request2.getStrict();
  logger6.info(`unparsed args: ${request2.getScript()}, ${request2.getSelector()}, ${request2.getOptions()}`);
  let elem;
  if (selector) {
    const locator = await findLocator(state2, selector, strictMode, void 0, true);
    elem = await locator.elementHandle();
  }
  const result = await page.waitForFunction(script, elem, options2);
  return jsonResponse(JSON.stringify(result.jsonValue), "Wait For Function completed successfully.");
}
async function addStyleTag(request2, page) {
  const content = request2.getContent();
  await page.addStyleTag({ content });
  return emptyWithLog("added Style: " + content);
}
var selectorsForPage = {};
async function recordSelector(request2, state2) {
  if (state2.getActiveBrowser().headless) {
    throw Error("Record Selector works only with visible browser. Use Open Browser or New Browser  headless=False");
  }
  const activeBrowser = state2.activeBrowser;
  if (!activeBrowser) {
    throw Error("No active browser.");
  }
  const indexedPage2 = activeBrowser.page;
  if (!indexedPage2) {
    throw Error("No active page.");
  }
  const page = indexedPage2.p;
  await page.bringToFront();
  if (!(indexedPage2.id in selectorsForPage)) {
    const myselectors = [];
    selectorsForPage[indexedPage2.id] = myselectors;
    await page.exposeFunction("setRecordedSelector", (index, item) => {
      while (myselectors.length > index) {
        myselectors.pop();
      }
      myselectors.push(item);
    });
    await page.exposeFunction("getRecordedSelectors", () => {
      return myselectors;
    });
    await page.exposeFunction("highlightPWSelector", (selector) => {
      highlightAll(selector, 1e3, "3px", "dotted", "blue", false, state2);
    });
  }
  const result = await recordSelectorIterator(request2.getLabel(), page.mainFrame());
  while (selectorsForPage[indexedPage2.id].length) {
    selectorsForPage[indexedPage2.id].pop();
  }
  return jsResponse(result, "Selector recorded.");
}
async function attachSelectorFinderScript(frame) {
  try {
    await frame.addScriptTag({
      type: "module",
      path: path2.join(__dirname, "/static/selector-finder.js")
    });
  } catch (e) {
    throw Error(
      `Adding selector recorder to page failed.
Try New Context  bypassCSP=True and retry recording.
Original error:${e}`
    );
  }
  await Promise.all(frame.childFrames().map((child) => attachSelectorFinderScript(child)));
}
async function attachSubframeListeners(subframe, index) {
  await subframe.evaluate((index2) => {
    function rafAsync() {
      return new Promise((resolve2) => {
        requestAnimationFrame(resolve2);
      });
    }
    function waitUntilRecorderAvailable() {
      if (!window.subframeSelectorRecorderFindSelector) {
        return rafAsync().then(() => waitUntilRecorderAvailable());
      } else {
        return Promise.resolve(window.subframeSelectorRecorderFindSelector(index2));
      }
    }
    return waitUntilRecorderAvailable();
  }, index);
  await Promise.all(
    subframe.childFrames().filter((f) => f.parentFrame() === subframe).map((child) => attachSubframeListeners(child, index + 1))
  );
}
async function recordSelectorIterator(label, frame) {
  await attachSelectorFinderScript(frame);
  await Promise.all(
    frame.childFrames().filter((f) => f.parentFrame() === frame).map((child) => attachSubframeListeners(child, 1))
  );
  return await frame.evaluate((label2) => {
    function rafAsync() {
      return new Promise((resolve2) => {
        requestAnimationFrame(resolve2);
      });
    }
    function waitUntilRecorderAvailable() {
      if (!window.selectorRecorderFindSelector) {
        return rafAsync().then(() => waitUntilRecorderAvailable());
      } else {
        return Promise.resolve(window.selectorRecorderFindSelector(label2));
      }
    }
    return waitUntilRecorderAvailable();
  }, label);
}
async function highlightElements(request2, state2) {
  const selector = request2.getSelector();
  const duration = request2.getDuration();
  const width = request2.getWidth();
  const style = request2.getStyle();
  const color = request2.getColor();
  const strictMode = request2.getStrict();
  const mode = request2.getMode();
  const count = await highlightAll(
    selector,
    duration,
    width,
    style,
    color,
    strictMode,
    state2,
    mode
  );
  const message = duration ? `Highlighted ${count} elements for ${duration} ms.` : `Highlighting ${count} elements`;
  return intResponse(count, message);
}
async function highlightAll(selector, duration, width, style, color, strictMode, state2, mode = "border") {
  const locator = await findLocator(state2, selector, strictMode, void 0, false);
  let count;
  try {
    count = await locator.count();
  } catch (e) {
    logger6.info(e);
    return 0;
  }
  logger6.info(`Locator count is ${count}`);
  if (["playwright", "both"].includes(mode)) {
    locator.highlight();
    if (duration !== 0) {
      setTimeout(() => {
        state2.getActivePage()?.locator("none.highlight-no-element").highlight();
      }, duration);
    }
    if (mode === "playwright") {
      return count;
    }
  }
  await locator.evaluateAll(
    (elements, options2) => {
      elements.forEach((e) => {
        const d = document.createElement("div");
        d.className = "robotframework-browser-highlight";
        d.appendChild(document.createTextNode(""));
        d.style.position = "fixed";
        const rect = e.getBoundingClientRect();
        d.style.zIndex = "2147483647";
        d.style.top = `calc(${rect.top}px - ${options2?.wdt ?? "1px"})`;
        d.style.left = `calc(${rect.left}px - ${options2?.wdt ?? "1px"})`;
        d.style.width = `${rect.width}px`;
        d.style.height = `${rect.height}px`;
        d.style.border = `${options2?.wdt ?? "1px"} ${options2?.stl ?? `dotted`} ${options2?.clr ?? `blue`}`;
        d.style.boxSizing = "content-box";
        document.body.appendChild(d);
        if (options2?.dur !== 0) {
          setTimeout(() => {
            d.remove();
          }, options2?.dur ?? 5e3);
        }
      });
    },
    { dur: duration, wdt: width, stl: style, clr: color }
  );
  return count;
}
async function download(request2, state2) {
  const browserState = state2.activeBrowser;
  if (browserState === void 0) {
    throw new Error("Download requires an active browser");
  }
  const context = browserState.context;
  if (context === void 0) {
    throw new Error("Download requires an active context");
  }
  if (!(context.options?.acceptDownloads ?? false)) {
    throw new Error("Context acceptDownloads is false");
  }
  const page = state2.getActivePage();
  if (page === void 0) {
    throw new Error("Download requires an active page");
  }
  const urlString = request2.getUrl();
  const saveAs = request2.getPath();
  const downloadTimeout = request2.getDownloadtimeout();
  const waitForFinish = request2.getWaitforfinish();
  const fromUrl = page.url();
  if (fromUrl === "about:blank") {
    throw new Error("Download requires that the page has been navigated to an url");
  }
  const script = (urlString2) => {
    return fetch(urlString2).then((resp) => {
      return resp.blob();
    }).then((blob) => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      a.download = urlString2;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      return a.download;
    });
  };
  const downloadStarted = _waitForDownload(page, state2, saveAs, downloadTimeout, waitForFinish);
  logger6.info(`Starting download from ${urlString} to ${saveAs}`);
  await page.evaluate(script, urlString);
  return await downloadStarted;
}

// node/playwright-wrapper/getters.ts
var import_playwright3 = require("playwright");
var import_playwright_pb2 = __toESM(require_playwright_pb());
async function getAriaSnapshot(request2, state2) {
  const selector = request2.getLocator();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  const snapshot = await locator.ariaSnapshot();
  logger2.info(`Aria snapshot for ${selector}: ${snapshot}`);
  return stringResponse(snapshot, "Aria snapshot received successfully.");
}
async function getTitle(page) {
  const title = await page.title();
  return stringResponse(title, "Active page title is: " + title);
}
async function getUrl(page) {
  const url = page.url();
  return stringResponse(url, url);
}
async function getElementCount(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, false);
  let count = 0;
  try {
    count = await locator.count();
  } catch (e) {
    if (!(e instanceof Error && e.message.includes("failed to find frame for selector"))) {
      throw e;
    }
  }
  return intResponse(count, `Found ${count} element(s).`);
}
async function getSelections(locator) {
  const response = new import_playwright_pb2.Response.Select();
  const selectElement = await locator.elementHandle();
  const selectOptions = await selectElement?.evaluate((e) => {
    return Array.from(e.options).map((option) => ({
      label: option.label,
      value: option.value,
      index: option.index,
      selected: option.selected
    }));
  });
  if (selectOptions) {
    const entries = selectOptions.map((e) => {
      const entry = new import_playwright_pb2.Types.SelectEntry();
      entry.setLabel(e.label);
      entry.setValue(e.value);
      entry.setIndex(e.index);
      entry.setSelected(e.selected);
      return entry;
    });
    logger2.info(`Option entries: ${entries.length}`);
    logger2.info(`Selected entries: ${entries.filter((e) => e.getSelected()).length}`);
    entries.forEach((e) => response.addEntry(e));
  }
  return response;
}
async function getSelectContent(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  await locator.elementHandle();
  return await getSelections(locator);
}
async function getDomProperty(request2, state2) {
  const content = await getProperty(request2, state2);
  return stringResponse(JSON.stringify(content), "Property received successfully.");
}
async function getTextContent(locator) {
  const element = await locator.elementHandle();
  exists(element, "Locator did not resolve to elementHandle.");
  const tag = await (await element.getProperty("tagName")).jsonValue();
  if (tag === "INPUT" || tag === "TEXTAREA") {
    return await (await element.getProperty("value")).jsonValue();
  }
  return await element.innerText();
}
async function getText(request2, state2) {
  const selector = request2.getSelector();
  const strict = request2.getStrict();
  const locator = await findLocator(state2, selector, strict, void 0, true);
  let content;
  try {
    content = await getTextContent(locator);
    logger2.info(`Retrieved text for element ${selector} containing ${content}`);
  } catch (e) {
    if (e instanceof Error) {
      logger2.error(e);
    }
    throw e;
  }
  return stringResponse(content, "Text received successfully.");
}
async function getBoolProperty(request2, state2) {
  const selector = request2.getSelector();
  const content = await getProperty(request2, state2);
  return boolResponse(content || false, "Retrieved dom property for element " + selector + " containing " + content);
}
async function getProperty(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const locator = findLocator(state2, selector, strictMode, void 0, true);
  try {
    const element = await (await locator).elementHandle();
    const propertyName = request2.getProperty();
    const property = await element?.getProperty(propertyName);
    const content = await property?.jsonValue();
    logger2.info(`Retrieved dom property for element ${selector} containing ${content}`);
    return content;
  } catch (e) {
    if (e instanceof Error) {
      logger2.error(e);
    }
    throw e;
  }
}
async function getElementAttribute(request2, state2) {
  const content = await getAttributeValue(request2, state2);
  return stringResponse(JSON.stringify(content), "Property received successfully.");
}
async function getAttributeValue(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const attributeName = request2.getProperty();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  await locator.elementHandle();
  const attribute = await locator.getAttribute(attributeName);
  logger2.info(`Retrieved attribute for element ${selector} containing ${attribute}`);
  return attribute;
}
var stateEnum = {
  attached: 1,
  detached: 2,
  visible: 4,
  hidden: 8,
  enabled: 16,
  disabled: 32,
  editable: 64,
  readonly: 128,
  selected: 256,
  deselected: 512,
  focused: 1024,
  defocused: 2048,
  checked: 4096,
  unchecked: 8192,
  stable: 16384
};
async function getCheckedState(locator) {
  try {
    return await locator.isChecked() ? stateEnum.checked : stateEnum.unchecked;
  } catch {
    return 0;
  }
}
async function getSelectState(element) {
  if (await element.evaluate((e) => "selected" in e)) {
    return await element.evaluate((e) => e.selected) ? stateEnum.selected : stateEnum.deselected;
  } else {
    return 0;
  }
}
async function getElementStates(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  let states = 0;
  try {
    await locator.waitFor({ state: "attached", timeout: 250 });
    states = stateEnum.attached;
    states += await locator.isVisible() ? stateEnum.visible : stateEnum.hidden;
    states += await locator.isEnabled() ? stateEnum.enabled : stateEnum.disabled;
    const disabled = await locator.getAttribute("disabled");
    try {
      const editable = await locator.isEditable();
      if (editable && disabled === null) {
        logger2.info(`Element ${selector} is editable: ${editable}`);
        states += stateEnum.editable;
      } else if (!editable && disabled !== null) {
        logger2.info(`Element ${selector} is disabled: ${disabled}`);
        states += stateEnum.readonly;
      } else {
        logger2.info(`Element ${selector} is readonly: ${!editable}`);
        states += stateEnum.readonly;
      }
    } catch (error) {
      logger2.info(`Element ${selector} is not editable: ${error}`);
      if (disabled !== null) {
        logger2.info(`Element ${selector} is disabled: ${disabled} and therefore readonly`);
        states += stateEnum.readonly;
      }
    }
    logger2.info("Checking checked state");
    states += await getCheckedState(locator);
    try {
      const element = await locator.elementHandle();
      exists(element, "Locator did not resolve to elementHandle.");
      states += await getSelectState(element);
      states += await element.evaluate((e) => document.activeElement === e) ? stateEnum.focused : stateEnum.defocused;
    } catch {
    }
  } catch (e) {
    if (e instanceof import_playwright3.errors.TimeoutError) {
      states = stateEnum.detached;
    } else {
      logger2.error(e);
      throw e;
    }
  }
  return jsonResponse(JSON.stringify(states), "Returned state.");
}
async function getStyle(request2, state2) {
  const selector = request2.getSelector();
  const option = {
    styleKey: request2.getStylekey() || null,
    pseudoElement: request2.getPseudo() || null
  };
  const strictMode = request2.getStrict();
  logger2.info("Getting css of element on page");
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  const result = await locator.evaluate((element, option2) => {
    const cssStyleDeclaration = window.getComputedStyle(element, option2.pseudoElement);
    if (option2.styleKey) {
      return cssStyleDeclaration.getPropertyValue(option2.styleKey);
    } else {
      return Object.fromEntries(
        Array.from(cssStyleDeclaration).map((key) => [key, cssStyleDeclaration.getPropertyValue(key)])
      );
    }
  }, option);
  return jsonResponse(JSON.stringify(result), "Style get successfully.");
}
async function getViewportSize(page) {
  const result = page.viewportSize();
  return jsonResponse(JSON.stringify(result), "View port size received sucesfully from page.");
}
async function getBoundingBox(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  const boundingBox = await locator.boundingBox();
  return jsonResponse(JSON.stringify(boundingBox), "Got bounding box successfully.");
}
async function getPageSource(page) {
  const result = await page.content();
  logger2.info(result);
  return stringResponse(JSON.stringify(result), "Page source obtained successfully.");
}
async function getTableCellIndex(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  const element = await locator.elementHandle();
  exists(element, "Locator did not resolve to elementHandle.");
  const count = await element.evaluate((element2) => {
    while (!["TD", "TH"].includes(element2.nodeName)) {
      const parent = element2.parentElement;
      if (!parent) {
        throw Error("Selector does not select a table cell!");
      }
      element2 = parent;
    }
    return Array.prototype.indexOf.call(element2.parentNode?.children, element2);
  });
  return intResponse(count, `Cell index in row is ${count}.`);
}
async function getTableRowIndex(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  const element = await locator.elementHandle();
  exists(element, "Locator did not resolve to elementHandle.");
  const count = await element.evaluate((element2) => {
    let table_row = null;
    while (element2.nodeName !== "TABLE") {
      if (element2.nodeName === "TR") {
        table_row = element2;
      }
      const parent = element2.parentElement;
      if (!parent) {
        throw Error("Selector does not select a table cell!");
      }
      element2 = parent;
    }
    let rows = element2.querySelectorAll(":scope > * > tr");
    if (rows.length == 0) {
      rows = element2.querySelectorAll(":scope > tr");
    }
    if (rows.length == 0) {
      throw Error(
        `Table rows could not be found. ChildNodes are: ${Array.prototype.slice.call(element2.childNodes).map((e) => `${e.nodeName}.${e.className}`)}`
      );
    }
    return Array.prototype.indexOf.call(rows, table_row);
  });
  return intResponse(count, `Row index in table is ${count}.`);
}

// node/playwright-wrapper/interaction.ts
var import_playwright_pb3 = __toESM(require_playwright_pb());
async function selectOption(request2, state2) {
  const selector = request2.getSelector();
  const matcher = JSON.parse(request2.getMatcherjson());
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  const result = await locator.selectOption(matcher);
  if (result.length == 0) {
    logger2.info("Couldn't select any options");
    throw new Error(`No options matched ${matcher}`);
  }
  return await getSelections(locator);
}
async function deSelectOption(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const locator = findLocator(state2, selector, strictMode, void 0, true);
  await (await locator).selectOption([]);
  return emptyWithLog(`Deselected options in element ${selector}`);
}
async function typeText(request2, state2) {
  const selector = request2.getSelector();
  const text = request2.getText();
  const delayValue = request2.getDelay();
  const clear = request2.getClear();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  if (clear) {
    await locator.fill("");
  }
  await locator.type(text, { delay: delayValue });
  return emptyWithLog(`Typed text "${text}" on "${selector}"`);
}
async function fillText(request2, state2) {
  const selector = request2.getSelector();
  const text = request2.getText();
  const strictMode = request2.getStrict();
  const force = request2.getForce();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  await locator.fill(text, { force });
  return emptyWithLog(`Fill text ${text} on ${selector} with force: ${force}`);
}
async function clearText(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  await locator.fill("");
  return emptyWithLog(`Text ${selector} field cleared.`);
}
async function press(request2, state2) {
  const selector = request2.getSelector();
  const keyList = request2.getKeyList();
  const strictMode = request2.getStrict();
  const pressDelay = request2.getPressdelay();
  const keyDelay = request2.getKeydelay();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  for (const i of keyList) {
    await locator.press(i, { delay: pressDelay });
    if (keyDelay > 0) {
      await new Promise((r) => setTimeout(r, keyDelay));
    }
  }
  return emptyWithLog(`Pressed keys: "${keyList}" on ${selector} `);
}
async function click(request2, state2) {
  const selector = request2.getSelector();
  const options2 = request2.getOptions();
  const strictMode = request2.getStrict();
  const result = await internalClick(selector, strictMode, options2, state2);
  if (result) {
    return emptyWithLog(`Clicked element: '${selector}' with options: '${options2}' successfully.`);
  }
  return emptyWithLog(
    `Clicked element: '${selector}' with options: '${options2}' but silenced: "Target closed error".`
  );
}
async function tap(request2, state2) {
  const selector = request2.getSelector();
  const options2 = request2.getOptions();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  await locator.tap(JSON.parse(options2));
  return emptyWithLog(`Tab element: '${selector}' with options: '${options2}'`);
}
async function internalClick(selector, strictMode, options2, state2) {
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  try {
    await locator.click(JSON.parse(options2));
    return true;
  } catch (error) {
    if (error instanceof Error && error.message.startsWith("locator.click: Target page, context or browser has been closed")) {
      logger2.warn("Supress locator.click: Target page, context or browser has been closed error");
      return false;
    }
    throw error;
  }
}
async function hover(request2, state2) {
  const selector = request2.getSelector();
  const options2 = request2.getOptions();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  await locator.hover(JSON.parse(options2));
  return emptyWithLog(`Hovered element: '${selector}' With options: '${options2}'`);
}
async function focus(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  await locator.focus();
  return emptyWithLog(`Focused element: ${selector}`);
}
async function checkCheckbox(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const force = request2.getForce();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  await locator.waitFor({ state: "attached" });
  await locator.check({ force });
  return emptyWithLog(`Checked checkbox: ${selector} with force: ${force}`);
}
async function uncheckCheckbox(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const force = request2.getForce();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  await locator.waitFor({ state: "attached" });
  await locator.uncheck({ force });
  return emptyWithLog(`Unchecked checkbox: ${selector} with force: ${force}`);
}
async function uploadFileBySelector(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const path4 = request2.getPathList();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  if (path4.length === 0) {
    const name2 = request2.getName();
    const mimeType = request2.getMimetype();
    const buffer = request2.getBuffer();
    logger2.info(`Uploading file ${name2} as buffer to ${selector}`);
    await locator.setInputFiles({ name: name2, mimeType, buffer: Buffer.from(buffer) });
    return emptyWithLog("Successfully uploaded buffer as file");
  } else {
    logger2.info(`Uploading file(s) ${path4} to ${selector}`);
    await locator.setInputFiles(path4);
    return emptyWithLog("Successfully uploaded file(s)");
  }
}
async function uploadFile(request2, page) {
  const path4 = request2.getPath();
  const fileChooser = await page.waitForEvent("filechooser");
  await fileChooser.setFiles(path4);
  return emptyWithLog("Successfully uploaded file");
}
async function handleAlert(request2, page) {
  const alertAction = request2.getAlertaction();
  const promptInput = request2.getPromptinput();
  const fn = async (dialog) => {
    const dialogueText = dialog.message();
    if (promptInput) await dialog[alertAction](promptInput);
    else await dialog[alertAction]();
    logger2.info(`Alert text: ${dialogueText}`);
  };
  page.on("dialog", fn);
  return emptyWithLog("Set event handler for next alert");
}
async function waitForAlerts(request2, page) {
  const response = new import_playwright_pb3.Response.ListString();
  const alertActions = request2.getItemsList();
  const alertMessages = [];
  for (let index = 0; index < alertActions.length; index++) {
    const alertAction = alertActions[index];
    const promptInput = alertAction.getPromptinput();
    const timeout = alertAction.getTimeout();
    const action = alertAction.getAlertaction();
    logger2.info(`Waiting for alert with action: ${action}, promptInput: "${promptInput}" and timeout: ${timeout}`);
    const dialogObject = await page.waitForEvent("dialog", { timeout });
    alertMessages.push(dialogObject.message());
    if (action === "accept" && promptInput) {
      dialogObject.accept(promptInput);
    } else if (alertAction.getAlertaction() === "accept") {
      dialogObject.accept();
    } else {
      dialogObject.dismiss();
    }
  }
  response.setItemsList(alertMessages);
  return response;
}
async function mouseButton(request2, page) {
  const action = request2.getAction();
  const params = JSON.parse(request2.getJson());
  await invokeOnMouse(page, action, params);
  return emptyWithLog(`Successfully executed ${action}`);
}
async function mouseMove(request2, page) {
  const params = JSON.parse(request2.getBody());
  await invokeOnMouse(page, "move", params);
  return emptyWithLog(`Successfully moved mouse to ${params.x}, ${params.y}`);
}
async function mouseWheel(request2, page) {
  const deltaX = request2.getDeltax();
  const deltaY = request2.getDeltay();
  exists(page, `but no open page`);
  await page?.mouse.wheel(deltaX, deltaY);
  return emptyWithLog(`Successfully scrolled mouse wheel with ${deltaX}, ${deltaY}`);
}
async function keyboardKey(request2, page) {
  const action = request2.getAction();
  const key = request2.getKey();
  await invokeOnKeyboard(page, action, key);
  return emptyWithLog(`Successfully did ${action} for ${key}`);
}
async function keyboardInput(request2, page) {
  const action = request2.getAction();
  const delay = request2.getDelay();
  const input = request2.getInput();
  await invokeOnKeyboard(page, action, input, { delay });
  return emptyWithLog(`Successfully did virtual keyboard action ${action} with input ${input}`);
}
async function scrollToElement(request2, state2) {
  const selector = request2.getSelector();
  const strictMode = request2.getStrict();
  const locator = await findLocator(state2, selector, strictMode, void 0, true);
  await locator.scrollIntoViewIfNeeded();
  return emptyWithLog(`Scrolled to ${selector} field if needed.`);
}

// node/playwright-wrapper/playwright-state.ts
var playwright = __toESM(require("playwright"));
var import_playwright4 = require("playwright");
var import_playwright5 = require("playwright");
var import_fs = __toESM(require("fs"));
var import_playwright_pb4 = __toESM(require_playwright_pb());
var path3 = __toESM(require("path"));
var import_monocart_coverage_reports = require("monocart-coverage-reports");
var import_strip_comments = __toESM(require("strip-comments"));
function lastItem(array) {
  return array[array.length - 1];
}
var extractArgumentsStringFromJavascript = (javascript) => {
  const regex = /\((.*?)\)/;
  const match = regex.exec((0, import_strip_comments.default)(javascript).replace(/\r?\n/g, ""));
  if (match) {
    return match[1];
  }
  logger2.error(`Could not extract arguments from javascript:
${javascript}
defaulting to *args`);
  return "*args";
};
async function initializeExtension(request2, state2) {
  logger2.info(`Initializing extension: ${request2.getPath()}`);
  const extension = require(request2.getPath());
  state2.extensions.push(extension);
  const kws = Object.keys(extension).filter((key) => extension[key] instanceof Function && !key.startsWith("__"));
  logger2.info(`Adding ${kws.length} keywords from JS Extension`);
  return keywordsResponse(
    kws,
    kws.map((v) => {
      return extractArgumentsStringFromJavascript(extension[v].toString());
    }),
    kws.map((v) => {
      const typedV = extension[v];
      return typedV.rfdoc ?? "TODO: Add rfdoc string to exposed function to create documentation";
    }),
    "ok"
  );
}
var getArgumentNamesFromJavascriptKeyword = (keyword) => extractArgumentsStringFromJavascript(keyword.toString()).split(",").map((s) => s.trim().match(/^\w*/)?.[0] || s.trim());
async function extensionKeywordCall(request2, call, state2) {
  const keywordName = request2.getName();
  const args2 = JSON.parse(request2.getArguments());
  const extension = state2.extensions.find((extension2) => Object.keys(extension2).includes(keywordName));
  if (!extension) throw Error(`Could not find keyword ${keywordName}`);
  const keyword = extension[keywordName];
  const namedArguments = Object.fromEntries(args2["arguments"]);
  const apiArguments = /* @__PURE__ */ new Map();
  apiArguments.set("page", state2.getActivePage());
  apiArguments.set("context", state2.getActiveContext());
  apiArguments.set("browser", state2.getActiveBrowser()?.browser);
  apiArguments.set("logger", (msg) => call.write(jsonResponse(JSON.stringify(""), msg)));
  apiArguments.set("playwright", playwright);
  const functionArguments = getArgumentNamesFromJavascriptKeyword(keyword).map(
    (argName) => apiArguments.get(argName) || namedArguments[argName]
  );
  const result = await keyword(...functionArguments);
  return jsonResponse(JSON.stringify(result), "ok");
}
async function _newBrowser(browserType, headless, timeout, options2) {
  const browser = await _getBrowserType(browserType).launch({ ...options2, headless, timeout });
  return {
    browser,
    browserType,
    headless
  };
}
function _getBrowserType(browserType) {
  let browserTyp;
  switch (browserType) {
    case "chromium":
      browserTyp = import_playwright5.chromium;
      break;
    case "firefox":
      browserTyp = import_playwright5.firefox;
      break;
    case "webkit":
      browserTyp = import_playwright5.webkit;
      break;
    default:
      throw new Error(`"${browserType} is an unsupported browser."`);
  }
  return browserTyp;
}
async function _launchBrowserServer(browserType, headless, timeout, options2) {
  let browser;
  const launchOptions = { ...options2, headless, timeout };
  if (browserType === "firefox") {
    browser = await import_playwright5.firefox.launchServer(launchOptions);
  } else if (browserType === "chromium") {
    browser = await import_playwright5.chromium.launchServer(launchOptions);
  } else if (browserType === "webkit") {
    browser = await import_playwright5.webkit.launchServer(launchOptions);
  } else {
    throw new Error("unsupported browser");
  }
  return browser;
}
async function _connectBrowser(browserName, url, connectCDP, timeout) {
  logger2.info(`Connecting to browser: ${browserName} at ${url} via ${connectCDP ? "CDP" : "WebSocket"}`);
  const browserType = _getBrowserType(browserName);
  timeout = timeout || 3e4;
  const browser = connectCDP ? await browserType.connectOverCDP(url, { timeout }) : await browserType.connect(url, { timeout });
  return {
    browser,
    browserType: browserName,
    headless: false
  };
}
async function _createIndexedContext(context, defaultTimeout, traceFile, options2) {
  const contextId = `context=${v4_default()}`;
  if (defaultTimeout) {
    logger2.info(`Setting default timeout for context ${contextId} to ${defaultTimeout}`);
    context.setDefaultTimeout(defaultTimeout);
  }
  if (traceFile) {
    if (!traceFile.toLowerCase().endsWith(".zip")) {
      traceFile = path3.join(traceFile, `trace_${contextId}.zip`);
    }
    traceFile = traceFile.replace("{contextid}", contextId);
  }
  const indexedContext = {
    id: contextId,
    c: context,
    pageStack: [],
    options: options2,
    traceFile
  };
  if (traceFile) {
    logger2.info("Tracing enabled with: { screenshots: true, snapshots: true }");
    context.tracing.start({ screenshots: true, snapshots: true });
  }
  indexedContext.c.on("page", async (page) => {
    indexedContext.pageStack.unshift(await _newPage(indexedContext, page));
  });
  return indexedContext;
}
function indexedPage(newPage2) {
  const timestamp = (/* @__PURE__ */ new Date()).getTime() / 1e3;
  const pageErrors = [];
  const consoleMessages = [];
  newPage2.on("pageerror", (error) => {
    const timedError = {
      name: error.name,
      message: error.message,
      stack: error.stack,
      time: /* @__PURE__ */ new Date()
    };
    pageErrors.push(timedError);
  });
  newPage2.on("console", (message) => {
    const timedMessage = {
      type: message.type(),
      text: message.text(),
      location: message.location(),
      time: /* @__PURE__ */ new Date()
    };
    consoleMessages.push(timedMessage);
  });
  return {
    id: `page=${v4_default()}`,
    p: newPage2,
    timestamp,
    pageErrors,
    errorIndex: 0,
    consoleMessages,
    consoleIndex: 0,
    activeDownloads: /* @__PURE__ */ new Map(),
    coverage: void 0
  };
}
async function _newPage(context, page = void 0) {
  const newPage2 = page === void 0 ? await context.c.newPage() : page;
  const contextPage = indexedPage(newPage2);
  newPage2.on("close", () => {
    const oldPageStackLength = context.pageStack.length;
    const filteredPageStack = context.pageStack.filter((page2) => page2.p != contextPage.p);
    if (oldPageStackLength != filteredPageStack.length) {
      context.pageStack = filteredPageStack;
      logger2.info("Removed " + contextPage.id + " from " + context.id + " page stack");
    }
  });
  return contextPage;
}
var PlaywrightState = class {
  constructor() {
    this.getActiveBrowser = () => {
      const currentBrowser = this.activeBrowser;
      if (currentBrowser === void 0) {
        throw new Error("Browser has been closed.");
      }
      return currentBrowser;
    };
    this.switchTo = (id) => {
      const browser = this.browserStack.find((b) => b.id === id);
      this.browserStack = this.browserStack.filter((b) => b.id !== id);
      exists(browser, `No browser for id '${id}'`);
      this.browserStack.push(browser);
      return this.getActiveBrowser();
    };
    this.addBrowserServer = (browserServer) => {
      this.browserServer.push(browserServer);
    };
    this.popBrowser = () => {
      return this.browserStack.pop();
    };
    this.getActiveContext = () => {
      return this.activeBrowser?.context?.c;
    };
    this.getTraceFile = () => {
      return this.activeBrowser?.context?.traceFile;
    };
    this.getActivePage = () => {
      return this.activeBrowser?.page?.p;
    };
    this.getActivePageId = () => {
      return this.activeBrowser?.page?.id;
    };
    this.getCoverageOptions = () => {
      return this.activeBrowser?.page?.coverage;
    };
    this.addCoverageOptions = (coverage) => {
      if (this.activeBrowser?.page) {
        this.activeBrowser.page.coverage = coverage;
      }
    };
    this.browserStack = [];
    this.extensions = [];
    this.browserServer = [];
    this.electronApp = null;
  }
  get activeBrowser() {
    return lastItem(this.browserStack);
  }
  async getOrCreateActiveBrowser(browserType, timeout) {
    const currentBrowser = this.activeBrowser;
    if (currentBrowser === void 0) {
      logger2.info("No active browser, creating a new one");
      const browserAndConfs = await _newBrowser(browserType || "chromium", true, timeout);
      const newState = new BrowserState(browserAndConfs);
      this.browserStack.push(newState);
      return { browser: newState, newBrowser: true };
    } else {
      logger2.info(`currentBrowser: ${JSON.stringify(currentBrowser)}`);
      return { browser: currentBrowser, newBrowser: false };
    }
  }
  async closeAll() {
    const browsers = this.browserStack;
    for (const browser of browsers) {
      try {
        await browser.close();
      } catch (e) {
      }
    }
    this.browserStack = [];
  }
  async closeAllServers() {
    const servers = this.browserServer;
    for (const server2 of servers) {
      try {
        await server2.close();
      } catch (e) {
      }
    }
    this.browserServer = [];
  }
  getBrowserServer(wsEndpoint) {
    return this.browserServer.find((server2) => server2.wsEndpoint() === wsEndpoint);
  }
  async closeServer(selectedServer) {
    if (!this.browserServer.includes(selectedServer)) {
      throw new Error(`BrowserServer not found.`);
    }
    this.browserServer.splice(this.browserServer.indexOf(selectedServer), 1);
    await selectedServer.close();
  }
  async getCatalog(includePageDetails = true) {
    const pageToContents = async (page) => {
      let title = null;
      let url = "";
      if (includePageDetails) {
        url = page.p.url();
        const titlePromise = page.p.title();
        const titleTimeout = new Promise((_r, rej) => setTimeout(() => rej(null), 350));
        try {
          title = await Promise.race([titlePromise, titleTimeout]);
        } catch (e) {
        }
      }
      return {
        type: "page",
        title: title || "",
        url,
        id: page.id,
        timestamp: page.timestamp
      };
    };
    const contextToContents = async (context) => {
      const activePage = lastItem(context.pageStack)?.id;
      return {
        type: "context",
        id: context?.id,
        activePage,
        pages: await Promise.all(context.pageStack.map(pageToContents))
      };
    };
    return Promise.all(
      this.browserStack.map(async (browser) => {
        return {
          type: browser.name,
          id: browser.id,
          contexts: await Promise.all(browser.contextStack.map(contextToContents)),
          activeContext: browser.context?.id,
          activeBrowser: this.activeBrowser === browser
        };
      })
    );
  }
  addBrowser(browserAndConfs) {
    const adding_browser = browserAndConfs.browser;
    logger2.info(`Adding browser to stack: ${browserAndConfs.browserType}, version: ${adding_browser?.version()}`);
    let browserState = this.browserStack.find((b) => b.browser === adding_browser);
    if (browserState !== void 0) {
      this.browserStack = this.browserStack.filter((b) => b.browser !== adding_browser);
    } else {
      browserState = new BrowserState(browserAndConfs);
    }
    const browserContexts = browserState.browser?.contexts();
    if (browserContexts !== void 0) {
      logger2.info(`Adding ${browserContexts.length} contexts to browser`);
      for (const context of browserContexts) {
        const indexedPages = context.pages().map((page) => indexedPage(page));
        logger2.info(`Adding ${indexedPages.length} pages to context`);
        const indexedContext = {
          id: `context=${v4_default()}`,
          c: context,
          pageStack: indexedPages,
          options: {},
          traceFile: ""
        };
        indexedContext.c.on("page", async (page) => {
          indexedContext.pageStack.unshift(await _newPage(indexedContext, page));
        });
        browserState?.pushContext(indexedContext);
      }
    }
    this.browserStack.push(browserState);
    return browserState;
  }
};
var LocatorCache = class {
  constructor() {
    this.cache = /* @__PURE__ */ new Map();
  }
  add(key, locator) {
    this.cache.set(key, locator);
  }
  get(key) {
    return this.cache.get(key);
  }
  delete(key) {
    return this.cache.delete(key);
  }
  has(key) {
    return this.cache.has(key);
  }
  clear() {
    this.cache.clear();
  }
};
var locatorCache = new LocatorCache();
var BrowserState = class {
  constructor(browserAndConfs) {
    this.name = browserAndConfs.browserType;
    this.browser = browserAndConfs.browser;
    this.headless = browserAndConfs.headless;
    this._contextStack = [];
    this.id = `browser=${v4_default()}`;
  }
  async close() {
    for (const context of this.contextStack) {
      const traceFile = context.traceFile;
      if (traceFile) {
        await context.c.tracing.stop({ path: traceFile });
      }
      await context.c.close();
    }
    this._contextStack = [];
    if (this.browser === null) {
      return;
    }
    await this.browser.close();
  }
  async getOrCreateActiveContext(defaultTimeout) {
    if (this.context) {
      return { context: this.context, newContext: false };
    } else if (this.browser === null) {
      throw new Error("Invalid persistent context browser without context");
    } else {
      const context = await _createIndexedContext(await this.browser.newContext(), defaultTimeout, "");
      this.pushContext(context);
      return { context, newContext: true };
    }
  }
  get context() {
    return lastItem(this._contextStack);
  }
  pushContext(newContext2) {
    if (newContext2 !== void 0) {
      if (newContext2.options === void 0) {
        newContext2.options = this._contextStack.find((c) => c.c === newContext2.c)?.options;
      }
      this._contextStack = this._contextStack.filter((c) => c.c !== newContext2.c);
      if (!newContext2.c) {
        throw new Error("Tried to switch to context, which did not exist anymore.");
      }
      this._contextStack.push(newContext2);
      logger2.info(`Changed active context: ${newContext2.id}`);
    } else logger2.info("Set active context to undefined");
  }
  unshiftContext(newContext2) {
    this._contextStack.unshift(newContext2);
  }
  get page() {
    const context = this.context;
    if (context) return lastItem(context.pageStack);
    else return void 0;
  }
  async activatePage(page) {
    this.pushPage(page);
    await page.p.bringToFront();
  }
  pushPage(newPage2) {
    const currentContext = this.context;
    if (newPage2 !== void 0 && currentContext !== void 0) {
      currentContext.pageStack = currentContext.pageStack.filter((p) => p.p !== newPage2.p);
      if (!newPage2.p) {
        throw new Error("Tried to switch to page, which did not exist anymore.");
      }
      currentContext.pageStack.push(newPage2);
      logger2.info("Changed active page");
    } else {
      logger2.info("Set active page to undefined");
    }
  }
  get contextStack() {
    return this._contextStack;
  }
  popPage() {
    const pageStack = this.context?.pageStack || [];
    return pageStack.pop();
  }
  popContext() {
    this._contextStack.pop();
  }
};
async function closeBrowserServer(request2, openBrowsers) {
  const wsEndpoint = request2.getUrl();
  if (wsEndpoint === "ALL") {
    await openBrowsers.closeAllServers();
    return emptyWithLog("Closed all browser servers");
  }
  const browserServer = openBrowsers.getBrowserServer(wsEndpoint);
  if (!browserServer) throw new Error(`BrowserServer with endpoint ${wsEndpoint} not found.`);
  openBrowsers.closeServer(browserServer);
  return emptyWithLog(`Closed browser server with endpoint: ${wsEndpoint}`);
}
async function closeBrowser(openBrowsers) {
  const currentBrowser = openBrowsers.activeBrowser;
  if (currentBrowser === void 0) {
    return stringResponse("no-browser", "No browser open, doing nothing");
  }
  openBrowsers.popBrowser();
  try {
    await currentBrowser.close();
    return stringResponse(currentBrowser.id, "Closed browser");
  } catch (e) {
    return stringResponse("", `Browser ${currentBrowser.id} was already closed`);
  }
}
async function closeAllBrowsers(openBrowsers) {
  await openBrowsers.closeAll();
  return emptyWithLog("Closed all browsers");
}
async function closeContext(request2, openBrowsers) {
  const saveTrace = request2.getValue();
  const activeBrowser = openBrowsers.getActiveBrowser();
  const traceFile = openBrowsers.getTraceFile();
  if (traceFile && saveTrace) {
    await openBrowsers.getActiveContext()?.tracing.stop({ path: traceFile });
  }
  for (const page of activeBrowser.context?.pageStack || []) {
    await _saveCoverageReport(page);
  }
  await openBrowsers.getActiveContext()?.close();
  activeBrowser.popContext();
  if (activeBrowser.contextStack.length === 0 && activeBrowser.browser === null) {
    closeBrowser(openBrowsers);
  }
  return emptyWithLog("Successfully closed Context");
}
async function closePage(request2, openBrowsers) {
  const activeBrowser = openBrowsers.getActiveBrowser();
  const closedPage = activeBrowser.popPage();
  if (closedPage) {
    await _saveCoverageReport(closedPage);
  }
  const unload = request2.getRunbeforeunload();
  if (!closedPage) throw new Error("No open page");
  logger2.info(`Closing page with runBeforeUnload ${unload}`);
  await closedPage.p.close({ runBeforeUnload: unload });
  return pageReportResponse(`Successfully closed Page with runBeforeUnload ${unload}`, closedPage);
}
async function newPage(request2, openBrowsers) {
  const defaultTimeout = request2.getUrl()?.getDefaulttimeout();
  const waitUntil = request2.getWaituntil();
  const browserState = await openBrowsers.getOrCreateActiveBrowser(null, defaultTimeout);
  const newBrowser2 = browserState.newBrowser;
  const context = await browserState.browser.getOrCreateActiveContext(defaultTimeout);
  const page = await _newPage(context.context);
  let videoPath = "";
  try {
    videoPath = await page.p.video()?.path();
  } catch (e) {
    logger2.info("Suppress video().path() error");
  }
  logger2.info("Video path: " + videoPath);
  browserState.browser.pushPage(page);
  const url = request2.getUrl()?.getUrl() || "about:blank";
  try {
    const goToOptions = { timeout: defaultTimeout };
    if (waitUntil) {
      goToOptions.waitUntil = waitUntil;
    }
    await page.p.goto(url, goToOptions);
    const response = new import_playwright_pb4.Response.NewPageResponse();
    response.setBody(page.id);
    response.setLog(`Successfully initialized new page object and opened url: ${url}`);
    const video = { video_path: videoPath || null, contextUuid: context.context.id };
    response.setVideo(JSON.stringify(video));
    response.setNewbrowser(newBrowser2);
    response.setNewcontext(context.newContext);
    return response;
  } catch (e) {
    browserState.browser.popPage()?.p.close();
    throw e;
  }
}
async function newContext(request2, openBrowsers) {
  const options2 = JSON.parse(request2.getRawoptions());
  logger2.info("Creating new context with options: " + JSON.stringify(options2));
  const defaultTimeout = request2.getDefaulttimeout();
  const browserState = await openBrowsers.getOrCreateActiveBrowser(options2.defaultBrowserType, defaultTimeout);
  const traceFile = request2.getTracefile();
  logger2.info(`Trace file: ${traceFile}`);
  if (browserState.browser.browser === null) {
    throw new Error("Trying to create a new context when a persistentContext is active");
  }
  const indexedContext = await _createIndexedContext(
    await browserState.browser.browser.newContext(options2),
    defaultTimeout,
    traceFile,
    options2
  );
  return await _finishContextResponse(indexedContext, browserState, options2, new import_playwright_pb4.Response.NewContextResponse());
}
async function _finishContextResponse(indexedContext, browserState, options2, response) {
  browserState.browser.pushContext(indexedContext);
  response.setId(indexedContext.id);
  if (indexedContext.traceFile) {
    response.setLog(`Successfully created context and trace file will be saved to: ${indexedContext.traceFile}`);
    options2.trace = { screenshots: true, snapshots: true };
  } else {
    response.setLog("Successfully created context. ");
  }
  response.setContextoptions(JSON.stringify(options2));
  response.setNewbrowser(browserState.newBrowser);
  return response;
}
async function newBrowser(request2, openBrowsers) {
  const browserType = request2.getBrowser();
  const options2 = JSON.parse(request2.getRawoptions());
  const browserAndConfs = await _newBrowser(
    browserType,
    options2["headless"],
    options2["timeout"],
    options2
  );
  const browserState = openBrowsers.addBrowser(browserAndConfs);
  return stringResponse(browserState.id, "Successfully created browser with options: " + JSON.stringify(options2));
}
async function launchBrowserServer(request2, openBrowsers) {
  const browserType = request2.getBrowser();
  const options2 = JSON.parse(request2.getRawoptions());
  logger2.info(`Launching browser server: ${browserType}`);
  logger2.info("Launching browser server with options: " + JSON.stringify(options2));
  const browserServer = await _launchBrowserServer(
    browserType,
    options2["headless"],
    options2["timeout"],
    options2
  );
  logger2.info(`Browser server launched. Endpoint: ${browserServer.wsEndpoint()}`);
  openBrowsers.addBrowserServer(browserServer);
  return stringResponse(
    browserServer.wsEndpoint(),
    "Successfully created browser server with options: " + JSON.stringify(options2)
  );
}
async function newPersistentContext(request2, openBrowsers) {
  const traceFile = request2.getTracefile();
  const timeout = request2.getDefaulttimeout();
  const options2 = JSON.parse(request2.getRawoptions());
  const userDataDir = options2?.userDataDir;
  const browserName = options2.defaultBrowserType || options2.browser || "chromium";
  const context = await _getBrowserType(browserName).launchPersistentContext(userDataDir, options2);
  const browserAndConfs = {
    browserType: browserName,
    browser: null,
    headless: options2?.headless || true
  };
  openBrowsers.addBrowser(browserAndConfs);
  const browserState = await openBrowsers.getOrCreateActiveBrowser(null, timeout);
  if (browserState.newBrowser === true) {
    throw new Error("A new browser was created in error while trying to create a persistent context");
  }
  const indexedContext = await _createIndexedContext(context, timeout, traceFile, options2);
  const page = indexedContext.c.pages()[0];
  indexedContext.pageStack.unshift(await _newPage(indexedContext, page));
  const response = await _finishContextResponse(
    indexedContext,
    browserState,
    options2,
    new import_playwright_pb4.Response.NewPersistentContextResponse()
  );
  const currentBrowser = openBrowsers.activeBrowser;
  const currentPage = indexedContext.pageStack[0];
  const videoPath = await currentPage.p.video()?.path();
  const video = { video_path: videoPath || null, contextUuid: indexedContext.id };
  response.setVideo(JSON.stringify(video));
  response.setPageid(currentPage.id);
  response.setBrowserid(currentBrowser?.id || "");
  return response;
}
async function launchElectron(request2, openBrowsers) {
  const executablePath = request2.getExecutablePath();
  const args2 = request2.getArgsList();
  const envMap = request2.getEnvMap();
  const timeout = request2.getTimeout() || void 0;
  const env = {};
  envMap.forEach((value, key) => {
    env[key] = value;
  });
  const launchOptions = { executablePath };
  if (args2 && args2.length > 0) launchOptions.args = args2;
  if (Object.keys(env).length > 0) launchOptions.env = { ...process.env, ...env };
  if (timeout) launchOptions.timeout = timeout;
  const electronApp = await import_playwright4._electron.launch(launchOptions);
  openBrowsers.electronApp = electronApp;
  let page = await electronApp.firstWindow();
  const firstTitle = await page.title().catch(() => "");
  if (!firstTitle) {
    const alreadyOpen = electronApp.windows().find((w) => w !== page);
    if (alreadyOpen) {
      page = alreadyOpen;
    } else {
      page = await electronApp.waitForEvent("window", { timeout: timeout || 3e4 }).catch(() => page);
    }
  }
  const context = page.context();
  const browserAndConfs = {
    browserType: "chromium",
    browser: null,
    headless: true
  };
  const browserState = openBrowsers.addBrowser(browserAndConfs);
  const indexedContext = await _createIndexedContext(context, timeout, "");
  const iPage = indexedPage(page);
  indexedContext.pageStack.push(iPage);
  browserState.pushContext(indexedContext);
  const response = new import_playwright_pb4.Response.NewPersistentContextResponse();
  response.setId(indexedContext.id);
  response.setLog(`Electron app launched. executablePath=${executablePath}`);
  response.setContextoptions("{}");
  response.setNewbrowser(true);
  response.setVideo("");
  response.setPageid(iPage.id);
  response.setBrowserid(browserState.id);
  return response;
}
async function openElectronDevTools(openBrowsers) {
  const app = openBrowsers.electronApp;
  if (!app) {
    return emptyWithLog("No Electron app open, doing nothing");
  }
  await app.evaluate(async ({ BrowserWindow }) => {
    const wins = BrowserWindow.getAllWindows();
    wins.forEach((w) => w.webContents.openDevTools());
  });
  return emptyWithLog("Opened DevTools for all Electron windows");
}
async function closeElectron(openBrowsers) {
  const app = openBrowsers.electronApp;
  if (!app) {
    return emptyWithLog("No Electron app open, doing nothing");
  }
  openBrowsers.electronApp = null;
  try {
    await app.close();
  } catch (e) {
  }
  openBrowsers.popBrowser();
  return emptyWithLog("Closed Electron application");
}
async function connectToBrowser(request2, openBrowsers) {
  const browserType = request2.getBrowser();
  const url = request2.getUrl();
  const connectCDP = request2.getConnectcdp();
  const timeout = request2.getTimeout();
  const browserAndConfs = await _connectBrowser(browserType, url, connectCDP, timeout);
  const browserState = openBrowsers.addBrowser(browserAndConfs);
  return stringResponse(browserState.id, "Successfully connected to browser");
}
async function openTraceGroup(request2, openBrowsers) {
  const name2 = request2.getName();
  const file = request2.getFile();
  const line = request2.getLine();
  const column = request2.getColumn();
  const contextId = request2.getContextid();
  if (openBrowsers?.browserStack) {
    for (const browserState of openBrowsers.browserStack) {
      for (const indexedContext of browserState.contextStack) {
        if (!contextId || indexedContext.id === contextId) {
          await indexedContext.c?.tracing?.group(name2, { location: { file, line, column } });
        }
      }
    }
  }
  return emptyWithLog("Opened trace group");
}
async function closeTraceGroup(openBrowsers) {
  if (openBrowsers?.browserStack) {
    for (const browserState of openBrowsers.browserStack) {
      for (const indexedContext of browserState.contextStack) {
        await indexedContext.c?.tracing?.groupEnd();
      }
    }
  }
  return emptyWithLog("Closed trace group");
}
async function _switchPage(id, browserState) {
  const context = browserState.context?.c;
  if (!context) throw new Error("Tried to switch page, no open context");
  const pages = browserState.context?.pageStack;
  logger2.info("Changing current active page: " + id);
  const page = pages?.find((elem) => elem.id == id);
  if (page) {
    await browserState.activatePage(page);
    return;
  } else {
    const mapped = pages?.map((page2) => `{ id: ${page2.id}, url: ${page2.p.url()} }`).join(",");
    const message = `No page for id ${id}. Open pages: ${mapped}`;
    const error = new Error(message);
    throw error;
  }
}
async function _switchContext(id, browserState) {
  const contexts = browserState.contextStack;
  const context = contexts.find((context2) => context2.id === id);
  if (contexts && context) {
    browserState.pushContext(context);
    return;
  } else {
    const mapped = contexts.map((context2) => context2.id);
    const message = `No context for id ${id}. Open contexts: ${mapped}`;
    throw new Error(message);
  }
}
async function switchPage(request2, browserState) {
  exists(browserState, "Tried to switch Page but browser wasn't open");
  const context = browserState.context;
  exists(context, "Tried to switch Page but no context was open");
  const id = request2.getId();
  if (id === "CURRENT") {
    const previous2 = browserState.page?.id || "NO PAGE OPEN";
    browserState.page?.p.bringToFront();
    return stringResponse(previous2, "Returned active page id");
  }
  if (id === "NEW") {
    const previous2 = browserState.page?.id || "NO PAGE OPEN";
    const previousTime = browserState.page?.timestamp || 0;
    const latest = await findLatestPageAfter(previousTime, request2.getTimeout(), context);
    exists(latest, "Tried to activate a new page but no new pages were detected in context.");
    await browserState.activatePage(latest);
    return stringResponse(previous2, `Activated new page ${latest.id}`);
  }
  const previous = browserState.page?.id || "";
  await _switchPage(id, browserState);
  return stringResponse(previous, "Successfully changed active page: " + id);
}
async function findLatestPageAfter(timestamp, timeout, context) {
  if (timeout < 0) {
    return null;
  }
  const latest = context.pageStack.reduce((acc, val) => {
    if (acc === void 0 || acc.timestamp < val.timestamp) {
      return val;
    }
    return acc;
  });
  if (!latest || timestamp && latest.timestamp <= timestamp) {
    await new Promise((resolve2) => setTimeout(resolve2, Math.min(15, timeout)));
    return findLatestPageAfter(timestamp, timeout - 15, context);
  }
  return latest;
}
async function switchContext(request2, browserState) {
  const id = request2.getIndex();
  const previous = browserState.context?.id || "";
  if (id === "CURRENT") {
    if (!previous) {
      return stringResponse("NO CONTEXT OPEN", "Returned info that no contexts are open");
    }
  } else {
    await _switchContext(id, browserState);
  }
  const page = browserState.page;
  if (page !== void 0) {
    await _switchPage(page.id, browserState);
  }
  return stringResponse(
    previous,
    id === "CURRENT" ? "Returned active context id: " + id : "Successfully changed active context: " + id
  );
}
async function switchBrowser(request2, openBrowsers) {
  const id = request2.getIndex();
  const previous = openBrowsers.activeBrowser;
  if (id !== "CURRENT") {
    openBrowsers.switchTo(id);
  }
  openBrowsers.getActivePage()?.bringToFront();
  return stringResponse(
    previous?.id || "NO BROWSER OPEN",
    id === "CURRENT" ? "Returned active browser id. " + id : "Successfully changed active browser: " + id
  );
}
async function getBrowserCatalog(request2, openBrowsers) {
  const includePageDetails = request2.getValue() || true;
  return jsonResponse(JSON.stringify(await openBrowsers.getCatalog(includePageDetails)), "Catalog received");
}
async function getConsoleLog(request2, openBrowsers) {
  const activePage = openBrowsers.getActiveBrowser().page;
  if (!activePage) throw new Error("No open page");
  return getConsoleLogResponse(activePage, request2.getValue(), "Console log received");
}
async function getErrorMessages(request2, openBrowsers) {
  const activePage = openBrowsers.getActiveBrowser().page;
  if (!activePage) throw new Error("No open page");
  return getErrorMessagesResponse(activePage, request2.getValue(), "Error messages received");
}
async function saveStorageState(request2, browserState) {
  exists(browserState, "Tried to save storage state but browser wasn't open");
  const context = browserState.context;
  exists(context, "Tried to save storage state butno context was open");
  const stateFile = request2.getPath();
  await context.c.storageState({ path: stateFile });
  return emptyWithLog("Current context state is saved to: " + stateFile);
}
async function startCoverage(request2, state2) {
  const activePage = state2.getActivePage();
  exists(activePage, "Could not find active page");
  const coverageOptions = {
    type: request2.getCoveragetype(),
    directory: request2.getCoveragedir(),
    configFile: request2.getConfigfile(),
    raw: request2.getRaw()
  };
  state2.addCoverageOptions(coverageOptions);
  const resetOnNavigation = request2.getResetonnavigation();
  const reportAnonymousScripts = request2.getReportanonymousscripts();
  if (["js", "all"].includes(coverageOptions.type)) {
    logger2.info(
      `Starting JS coverage with resetOnNavigation: ${resetOnNavigation} and reportAnonymousScripts: ${reportAnonymousScripts}`
    );
    await activePage.coverage.startJSCoverage({ reportAnonymousScripts, resetOnNavigation });
  }
  if (["css", "all"].includes(coverageOptions.type)) {
    logger2.info(`Starting CSS coverage with resetOnNavigation: ${resetOnNavigation}`);
    await activePage.coverage.startCSSCoverage({ resetOnNavigation });
  }
  return emptyWithLog(`Coverage started for ${coverageOptions.type}`);
}
async function stopCoverage(request2, state2) {
  const activeIndexedPage = state2.activeBrowser?.page;
  exists(activeIndexedPage, "Could not find active page");
  return _saveCoverageReport(activeIndexedPage);
}
async function _saveCoverageReport(activeIndexedPage) {
  const { coverage: coverageOptions, p: activePage, id: pageId } = activeIndexedPage;
  activeIndexedPage.coverage = void 0;
  if (!coverageOptions) {
    return stringResponse("", "Coverage not started");
  }
  const { directory: coverageDir = "", configFile: configFile2 = "", type: coverageType, raw = false } = coverageOptions;
  const allCoverage = [];
  if (["js", "all"].includes(coverageType)) {
    logger2.info("Stopping JS coverage");
    allCoverage.push(...await activePage.coverage.stopJSCoverage());
  }
  if (["css", "all"].includes(coverageType)) {
    logger2.info("Stopping CSS coverage");
    allCoverage.push(...await activePage.coverage.stopCSSCoverage());
  }
  const outputDir = path3.normalize(path3.join(coverageDir, pageId));
  const options2 = { outputDir };
  if (raw && configFile2 === "") {
    logger2.info("Raw and v8 coverage enabled");
    options2.reports = [["raw"], ["v8"]];
  } else {
    logger2.info("v8 coverage disabled");
  }
  let mergedOptions2;
  if (import_fs.default.existsSync(configFile2)) {
    logger2.info({ "Config file exists: ": configFile2 });
    const configFileModule2 = require(configFile2);
    mergedOptions2 = { ...configFileModule2, ...options2 };
    console.log({ "Merged options: ": mergedOptions2 });
  } else {
    console.log({ "No config file found": configFile2 });
    mergedOptions2 = { ...options2 };
  }
  const mcr = new import_monocart_coverage_reports.CoverageReport(mergedOptions2);
  await mcr.add(allCoverage);
  await mcr.generate();
  let message = "Coverage stopped and report generated";
  if (!import_fs.default.existsSync(configFile2)) {
    message += `. But no config file found at ${configFile2}`;
  }
  return stringResponse(outputDir, message);
}
async function mergeCoverage(request, state) {
  state.getActivePage();
  const inputFolder = request.getInputFolder();
  const outputFolder = request.getOutputFolder();
  const configFile = request.getConfig();
  const name = request.getName();
  const reports = request.getReportsList();
  if (!inputFolder) {
    throw Error("No input folders specified");
  }
  if (!outputFolder) {
    throw Error("No output folder specified");
  }
  const options = {
    name,
    inputDir: inputFolder,
    outputDir: outputFolder
  };
  logger2.info(`Reports to generate: ${reports}`);
  if (reports && reports.length > 0) {
    options.reports = reports.map((r) => [r]);
  }
  const defaultName = "Browser library Merged Coverage Report";
  let mergedOptions;
  if (import_fs.default.existsSync(configFile)) {
    logger2.info(`Config file exists:  ${configFile}`);
    const configFileModule = await eval("require")(configFile);
    logger2.info(`configFileModule options: ${JSON.stringify(configFileModule)}`);
    mergedOptions = { ...configFileModule, ...options };
    if (reports && reports.length === 1 && reports[0] === "v8") {
      mergedOptions.reports = [["v8"], configFileModule.reports || []].flat();
    }
    if (mergedOptions.name === "" && configFileModule.name) {
      mergedOptions.name = configFileModule.name;
    } else {
      mergedOptions.name = defaultName;
    }
    logger2.info(`Merged options: ${JSON.stringify(mergedOptions)}`);
  } else {
    logger2.info(`No config file found: ${configFile}`);
    mergedOptions = { ...options };
    if (mergedOptions.name === "") {
      mergedOptions.name = defaultName;
    }
  }
  logger2.info(`Final options: ${JSON.stringify(mergedOptions)}`);
  logger2.info(`Merging coverage from ${inputFolder} into ${outputFolder}`);
  await new import_monocart_coverage_reports.CoverageReport(mergedOptions).generate();
  return emptyWithLog(`Coverage merged from ${inputFolder} into ${outputFolder}`);
}

// node/playwright-wrapper/locator-handler.ts
var import_pino7 = __toESM(require("pino"));
var logger7 = (0, import_pino7.default)({ timestamp: import_pino7.default.stdTimeFunctions.isoTime });
async function addLocatorHandlerCustom(request2, state2) {
  const activePage = state2.getActivePage();
  exists(activePage, "Could not find active page");
  const overlaySelector = request2.getSelector();
  const timesString = request2.getTimes();
  let times;
  if (timesString === "None") {
    times = void 0;
  } else {
    times = parseInt(timesString);
  }
  logger7.info(`Adding locator handler for ${overlaySelector} as times: ${times}`);
  const noWaitAfter = request2.getNowaitafter();
  const hadlerSpecs = request2.getHandlerspecsList();
  const overlayLocator = await findLocator(state2, overlaySelector, false, void 0, true);
  locatorCache.add(`${state2.getActivePageId()}-${overlaySelector}`, overlayLocator);
  await activePage.addLocatorHandler(
    overlayLocator,
    async () => {
      logger7.info(`Overlay locator ${overlaySelector} is found`);
      for (const handlerSpec of hadlerSpecs) {
        const action = handlerSpec.getAction();
        const actionSelector = handlerSpec.getSelector();
        const actionLocator = await findLocator(state2, actionSelector, false, void 0, true);
        const options2 = JSON.parse(handlerSpec.getOptionsasjson());
        try {
          if (action === "click") {
            logger7.info(
              `Overlay click on element ${actionSelector} with options: ${JSON.stringify(options2)}`
            );
            await actionLocator.click({ ...options2 });
          } else if (action === "fill") {
            const value = handlerSpec.getValue();
            logger7.info(
              `Overlay fill on element ${actionSelector} with value ${value} with options: ${JSON.stringify(options2)}`
            );
            await actionLocator.fill(value, { ...options2 });
          } else if (action === "check") {
            logger7.info(
              `Overlay check on element ${actionSelector} with options: ${JSON.stringify(options2)}`
            );
            await actionLocator.check({ ...options2 });
          } else if (action === "uncheck") {
            logger7.info(
              `Overlay uncheck on element ${actionSelector} with options: ${JSON.stringify(options2)}`
            );
            await actionLocator.uncheck({ ...options2 });
          }
        } catch (error) {
          logger7.error(`Error in custom locator handler: ${error}`);
        }
      }
    },
    { times, noWaitAfter }
  );
  return emptyWithLog(`Custom locator handler added for element ${overlaySelector}`);
}
async function removeLocatorHandler(request2, state2) {
  logger7.info(`Removing locator handler for ${request2.getSelector()}`);
  const activePage = state2.getActivePage();
  exists(activePage, "Could not find active page");
  const activePageId = state2.getActivePageId();
  const overlaySelector = request2.getSelector();
  const locator = locatorCache.get(`${activePageId}-${overlaySelector}`);
  locatorCache.delete(`${activePageId}-${overlaySelector}`);
  if (locator === void 0) {
    return emptyWithLog(`No locator handler found for ${overlaySelector}`);
  }
  await activePage.removeLocatorHandler(locator);
  return emptyWithLog(`Removed locator handler ${overlaySelector}`);
}

// node/playwright-wrapper/pdf.ts
var import_pino8 = require("pino");
var logger8 = (0, import_pino8.pino)({ timestamp: import_pino8.pino.stdTimeFunctions.isoTime });
async function savePageAsPdf(request2, state2) {
  const activePage = state2.getActivePage();
  exists(activePage, "Could not find active page");
  const pdfPath = request2.getPath();
  const displayheaderfooter = request2.getDisplayheaderfooter();
  const footertemplate = request2.getFootertemplate();
  const format = request2.getFormat();
  const headerTemplate = request2.getHeadertemplate();
  const height = request2.getHeight();
  const landscape = request2.getLandscape();
  const marginString = request2.getMargin();
  const marging = JSON.parse(marginString);
  const outline = request2.getOutline();
  const pageRanges = request2.getPageranges();
  const preferCSSPageSize = request2.getPrefercsspagesize();
  const printBackground = request2.getPrintbackground();
  const scale = request2.getScale();
  const tagged = request2.getTagged();
  const width = request2.getWidth();
  logger8.info(`Saving pdf to ${pdfPath}`);
  const message = `Using options: displayHeaderFooter: ${displayheaderfooter}, footerTemplate: ${footertemplate}, format: ${format}, headerTemplate: ${headerTemplate}, height: ${height}, landscape: ${landscape}, margin (as string): ${marginString}, outline: ${outline}, pageRanges: ${pageRanges}, preferCSSPageSize: ${preferCSSPageSize}, printBackground: ${printBackground}, scale: ${scale}, tagged: ${tagged}  and width: ${width}`;
  logger8.info(message);
  await activePage.pdf({
    path: pdfPath,
    displayHeaderFooter: displayheaderfooter,
    footerTemplate: footertemplate,
    format,
    headerTemplate,
    height,
    landscape,
    margin: marging,
    outline,
    pageRanges,
    preferCSSPageSize,
    printBackground,
    scale,
    tagged,
    width
  });
  return stringResponse(pdfPath, `Pdf is saved to ${pdfPath}`);
}
async function emulateMedia(request2, state2) {
  const activePage = state2.getActivePage();
  exists(activePage, "Could not find active page");
  const options2 = {};
  const colorScheme = request2.getColorscheme();
  if (colorScheme === "not_set") {
    logger8.info(`Emulating colorScheme not set`);
  } else if (colorScheme === "null") {
    logger8.info(`Emulating colorScheme null`);
    options2.colorScheme = null;
  } else {
    logger8.info(`Emulating colorScheme ${colorScheme}`);
    options2.colorScheme = colorScheme;
  }
  const forcedColors = request2.getForcedcolors();
  if (forcedColors === "not_set") {
    logger8.info(`Emulating forcedColors not set`);
  } else if (forcedColors === "null") {
    logger8.info(`Emulating forcedColors null`);
    options2.forcedColors = null;
  } else {
    logger8.info(`Emulating forcedColors ${forcedColors}`);
    options2.forcedColors = forcedColors;
  }
  const media = request2.getMedia();
  if (media === "not_set") {
    logger8.info(`Emulating media not set`);
  } else if (media === "null") {
    logger8.info(`Emulating media null`);
    options2.media = null;
  } else {
    logger8.info(`Emulating media ${media}`);
    options2.media = media;
  }
  const reducedMotion = request2.getReducedmotion();
  if (reducedMotion === "not_set") {
    logger8.info(`Emulating reducedMotion not set`);
  } else if (reducedMotion === "null") {
    logger8.info(`Emulating reducedMotion null`);
    options2.reducedMotion = null;
  } else {
    logger8.info(`Emulating reducedMotion ${reducedMotion}`);
    options2.reducedMotion = reducedMotion;
  }
  await activePage.emulateMedia(options2);
  return stringResponse(JSON.stringify(options2), `Emulating media ${JSON.stringify(options2)}`);
}

// node/playwright-wrapper/grpc-service.ts
var import_playwright_pb5 = __toESM(require_playwright_pb());

// node/playwright-wrapper/keyword-decorators.ts
function class_async_logger(target) {
  for (const propertyName of Object.keys(target.prototype)) {
    const descriptor = Object.getOwnPropertyDescriptor(target.prototype, propertyName);
    const isMethod = descriptor?.value instanceof Function;
    if (!isMethod || !descriptor) continue;
    const timered_method = async_logger(propertyName, descriptor);
    Object.defineProperty(target.prototype, propertyName, timered_method);
  }
}
function async_logger(propertyKey, propertyDescriptor) {
  const originalMethod = propertyDescriptor.value;
  propertyDescriptor.value = async function(...args2) {
    try {
      logger2.info(`Start of node method ${propertyKey}`);
      const result = await originalMethod.apply(this, args2);
      logger2.info(`End of node method ${propertyKey}`);
      return result;
    } catch (err) {
      logger2.info(`Error of node method  ${propertyKey}`);
      throw err;
    }
  };
  return propertyDescriptor;
}

// node/playwright-wrapper/grpc-service.ts
var PlaywrightServer = class {
  constructor() {
    this.states = {};
    this.peerMap = {};
    this.createState = (key) => {
      if (!(key in this.states)) {
        this.states[key] = new PlaywrightState();
      }
      return this.states[key];
    };
    this.getState = (peer) => {
      const mapPeer = this.peerMap[peer.getPeer()];
      if (mapPeer) {
        return this.createState(mapPeer);
      } else {
        this.peerMap[peer.getPeer()] = peer.getPeer();
        const p = peer.getPeer();
        return this.createState(p);
      }
    };
    this.getActiveBrowser = (peer) => this.getState(peer).getActiveBrowser();
    this.getActiveContext = (peer) => this.getState(peer).getActiveContext();
    this.getActivePage = (peer) => {
      const page = this.getState(peer).getActivePage();
      if (!page) throw Error("No page open.");
      return page;
    };
    this.wrapping = (func) => {
      return async (call, callback) => {
        try {
          const request2 = call.request;
          if (request2 === null) throw Error("No request");
          logger2.info(`Start of node method ${func.name}`);
          const response = await func(request2, this.getState(call));
          logger2.info(`End of node method ${func.name}`);
          callback(null, response);
        } catch (e) {
          logger2.info(`Error of node method  ${func.name}`);
          callback(errorResponse(e), null);
        }
      };
    };
    this.wrappingState = (func) => {
      return async (call, callback) => {
        try {
          logger2.info(`Start of node method ${func.name}`);
          const response = await func(this.getState(call));
          logger2.info(`End of node method ${func.name}`);
          callback(null, response);
        } catch (e) {
          logger2.info(`Error of node method ${func.name}`);
          callback(errorResponse(e), null);
        }
      };
    };
    this.wrappingPage = (func) => {
      return async (call, callback) => {
        try {
          const request2 = call.request;
          if (request2 === null) throw Error("No request");
          logger2.info(`Start of node method ${func.name}`);
          const response = await func(request2, this.getActivePage(call));
          logger2.info(`End of node method ${func.name}`);
          callback(null, response);
        } catch (e) {
          logger2.info(`Error of node method ${func.name}`);
          callback(errorResponse(e), null);
        }
      };
    };
    this.wrappingStatePage = (func) => {
      return async (call, callback) => {
        try {
          const request2 = call.request;
          if (request2 === null) throw Error("No request");
          logger2.info(`Start of node method ${func.name}`);
          const response = await func(request2, this.getState(call), this.getActivePage(call));
          logger2.info(`End of node method ${func.name}`);
          callback(null, response);
        } catch (e) {
          logger2.info(`Error of node method  ${func.name}`);
          callback(errorResponse(e), null);
        }
      };
    };
    this.initializeExtension = this.wrapping(initializeExtension);
    this.closeBrowser = this.wrappingState(closeBrowser);
    this.closeBrowserServer = this.wrapping(closeBrowserServer);
    this.closeAllBrowsers = this.wrappingState(closeAllBrowsers);
    this.closeContext = this.wrapping(closeContext);
    this.closePage = this.wrapping(closePage);
    this.openTraceGroup = this.wrapping(openTraceGroup);
    this.closeTraceGroup = this.wrappingState(closeTraceGroup);
    this.getBrowserCatalog = this.wrapping(getBrowserCatalog);
    this.getConsoleLog = this.wrapping(getConsoleLog);
    this.getErrorMessages = this.wrapping(getErrorMessages);
    this.switchBrowser = this.wrapping(switchBrowser);
    this.newPage = this.wrapping(newPage);
    this.newContext = this.wrapping(newContext);
    this.newBrowser = this.wrapping(newBrowser);
    this.startCoverage = this.wrapping(startCoverage);
    this.stopCoverage = this.wrapping(stopCoverage);
    this.mergeCoverage = this.wrapping(mergeCoverage);
    this.launchBrowserServer = this.wrapping(launchBrowserServer);
    this.newPersistentContext = this.wrapping(newPersistentContext);
    this.launchElectron = this.wrapping(launchElectron);
    this.closeElectron = this.wrappingState(closeElectron);
    this.openElectronDevTools = this.wrappingState(openElectronDevTools);
    this.connectToBrowser = this.wrapping(connectToBrowser);
    this.goTo = this.wrappingPage(goTo);
    this.pdf = this.wrapping(savePageAsPdf);
    this.emulateMedia = this.wrapping(emulateMedia);
    this.takeScreenshot = this.wrapping(takeScreenshot);
    this.getBoundingBox = this.wrapping(getBoundingBox);
    this.ariaSnapShot = this.wrappingStatePage(getAriaSnapshot);
    this.getElementCount = this.wrapping(getElementCount);
    this.getSelectContent = this.wrapping(getSelectContent);
    this.getDomProperty = this.wrapping(getDomProperty);
    this.getText = this.wrapping(getText);
    this.getBoolProperty = this.wrapping(getBoolProperty);
    this.getElementAttribute = this.wrapping(getElementAttribute);
    this.getElementStates = this.wrapping(getElementStates);
    this.getStyle = this.wrapping(getStyle);
    this.getTableCellIndex = this.wrapping(getTableCellIndex);
    this.getTableRowIndex = this.wrapping(getTableRowIndex);
    this.scrollToElement = this.wrapping(scrollToElement);
    this.selectOption = this.wrapping(selectOption);
    this.executePlaywright = this.wrapping(executePlaywright);
    this.grantPermissions = this.wrapping(grantPermissions);
    this.clearPermissions = this.wrapping(clearPermissions);
    this.deselectOption = this.wrapping(deSelectOption);
    this.typeText = this.wrapping(typeText);
    this.fillText = this.wrapping(fillText);
    this.clearText = this.wrapping(clearText);
    this.press = this.wrapping(press);
    this.click = this.wrapping(click);
    this.addLocatorHandlerCustom = this.wrapping(addLocatorHandlerCustom);
    this.removeLocatorHandler = this.wrapping(removeLocatorHandler);
    this.tap = this.wrapping(tap);
    this.hover = this.wrapping(hover);
    this.focus = this.wrapping(focus);
    this.checkCheckbox = this.wrapping(checkCheckbox);
    this.uncheckCheckbox = this.wrapping(uncheckCheckbox);
    this.getElement = this.wrapping(getElement);
    this.getElements = this.wrapping(getElements);
    this.getByX = this.wrapping(getByX);
    this.addStyleTag = this.wrappingPage(addStyleTag);
    this.setTime = this.wrapping(setTime);
    this.clockResume = this.wrapping(clockResume);
    this.clockPauseAt = this.wrapping(clockPauseAt);
    this.advanceClock = this.wrapping(advanceClock);
    this.waitForElementsState = this.wrapping(waitForElementState);
    this.waitForRequest = this.wrappingPage(waitForRequest);
    this.waitForNavigation = this.wrappingPage(waitForNavigation);
    this.waitForPageLoadState = this.wrappingPage(WaitForPageLoadState);
    this.getDownloadState = this.wrapping(getDownloadState);
    this.cancelDownload = this.wrapping(cancelDownload);
    this.waitForDownload = this.wrappingStatePage(waitForDownload);
    this.evaluateJavascript = this.wrappingStatePage(evaluateJavascript);
    this.recordSelector = this.wrapping(recordSelector);
    this.highlightElements = this.wrapping(highlightElements);
    this.download = this.wrapping(download);
    this.setViewportSize = this.wrappingPage(setViewportSize);
    this.httpRequest = this.wrappingPage(httpRequest);
    this.uploadFile = this.wrappingPage(uploadFile);
    this.handleAlert = this.wrappingPage(handleAlert);
    this.waitForAlerts = this.wrappingPage(waitForAlerts);
    this.mouseMove = this.wrappingPage(mouseMove);
    this.mouseWheel = this.wrappingPage(mouseWheel);
    this.mouseButton = this.wrappingPage(mouseButton);
    this.keyboardKey = this.wrappingPage(keyboardKey);
    this.keyboardInput = this.wrappingPage(keyboardInput);
  }
  async callExtensionKeyword(call) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const result = await extensionKeywordCall(request2, call, this.getState(call));
      call.write(result);
    } catch (e) {
      call.emit("error", errorResponse(e));
    }
    call.end();
  }
  async getCookies(call, callback) {
    try {
      const context = this.getActiveContext(call);
      if (!context) throw Error("no open context.");
      const result = await getCookies(context);
      callback(null, result);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async addCookie(call, callback) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const context = this.getActiveContext(call);
      if (!context) throw Error("no open context.");
      const result = await addCookie(request2, context);
      callback(null, result);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async deleteAllCookies(call, callback) {
    try {
      const context = this.getActiveContext(call);
      if (!context) throw Error("no open context.");
      const result = await deleteAllCookies(context);
      callback(null, result);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async switchPage(call, callback) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const response = await switchPage(request2, this.getActiveBrowser(call));
      callback(null, response);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async switchContext(call, callback) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const response = await switchContext(request2, this.getActiveBrowser(call));
      callback(null, response);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async saveStorageState(call, callback) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const response = await saveStorageState(request2, this.getActiveBrowser(call));
      callback(null, response);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async goBack(call, callback) {
    try {
      await this.getActivePage(call).goBack();
      callback(null, emptyWithLog("Did Go Back"));
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async goForward(call, callback) {
    try {
      await this.getActivePage(call).goForward();
      callback(null, emptyWithLog("Did Go Forward"));
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async getPageSource(call, callback) {
    try {
      const response = await getPageSource(this.getActivePage(call));
      callback(null, response);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async setTimeout(call, callback) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const response = await setTimeout2(request2, this.getActiveBrowser(call)?.context?.c);
      callback(null, response);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async getTitle(call, callback) {
    try {
      const response = await getTitle(this.getActivePage(call));
      callback(null, response);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async getUrl(call, callback) {
    try {
      const response = await getUrl(this.getActivePage(call));
      callback(null, response);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async getViewportSize(call, callback) {
    try {
      const response = await getViewportSize(this.getActivePage(call));
      callback(null, response);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async waitForResponse(call) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const results = await waitForResponse(request2, this.getActivePage(call));
      for (const result of results) {
        logger2.info(`Sending response ${result.getLog()}`);
        call.write(result);
      }
    } catch (e) {
      call.emit("error", errorResponse(e));
    }
    call.end();
  }
  async waitForFunction(call, callback) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const result = await waitForFunction(request2, this.getState(call), this.getActivePage(call));
      callback(null, result);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async health(call, callback) {
    const response = new import_playwright_pb5.Response.String();
    response.setBody("OK");
    callback(null, response);
  }
  async getDevice(call, callback) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const result = getDevice(request2);
      callback(null, result);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async getDevices(call, callback) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const result = getDevices();
      callback(null, result);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async uploadFileBySelector(call, callback) {
    let buffer = "";
    let lastRequest;
    call.on("data", async (request2) => {
      try {
        logger2.info(`Reading multiplepart uploadFileBySelector`);
        const newBuffer = request2.getBuffer();
        buffer += newBuffer;
        lastRequest = request2;
      } catch (e) {
        callback(errorResponse(e), null);
      }
    });
    call.on("error", (e) => {
      callback(errorResponse(e), null);
    });
    call.on("end", async () => {
      try {
        lastRequest.setBuffer(buffer);
        const result = await uploadFileBySelector(lastRequest, this.getState(call));
        callback(null, result);
      } catch (e) {
        callback(errorResponse(e), null);
      }
    });
  }
  async setOffline(call, callback) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const result = await setOffline(request2, this.getActiveContext(call));
      callback(null, result);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async setGeolocation(call, callback) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const result = await setGeolocation(request2, this.getActiveContext(call));
      callback(null, result);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async reload(call, callback) {
    try {
      const request2 = call.request;
      const body = request2.getBody();
      if (request2 === null) throw Error("No request");
      const result = await reload(this.getActivePage(call), body);
      callback(null, result);
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
  async setPeerId(call, callback) {
    try {
      const request2 = call.request;
      if (request2 === null) throw Error("No request");
      const oldPeer = this.peerMap[call.getPeer()];
      this.peerMap[call.getPeer()] = request2.getIndex();
      callback(null, stringResponse(oldPeer, "Successfully overrode peer id"));
    } catch (e) {
      callback(errorResponse(e), null);
    }
  }
};
PlaywrightServer = __decorateClass([
  class_async_logger
], PlaywrightServer);

// node/playwright-wrapper/index.ts
var import_grpc_js2 = require("@grpc/grpc-js");
var import_playwright_grpc_pb = __toESM(require_playwright_grpc_pb());
var args = process.argv.slice(2);
var host = args[0];
var port = args[1];
if (!host) {
  throw new Error(`No host defined`);
}
if (!port) {
  throw new Error(`No port defined`);
}
var server = new import_grpc_js2.Server();
server.addService(
  import_playwright_grpc_pb.PlaywrightService,
  new PlaywrightServer()
);
server.bindAsync(`${host}:${port}`, import_grpc_js2.ServerCredentials.createInsecure(), () => {
  logger2.info(`Listening on ${host}:${port}`);
});
