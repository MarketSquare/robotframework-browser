// Copyright 2020-     Robot Framework Foundation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import * as browserControl from './browser-control';
import * as cookie from './cookie';
import * as deviceDescriptors from './device-descriptors';
import * as evaluation from './evaluation';
import * as getters from './getters';
import * as interaction from './interaction';
import * as network from './network';
import * as pino from 'pino';
import * as playwrightState from './playwright-state';
import { IPlaywrightServer } from './generated/playwright_grpc_pb';
import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { ServerSurfaceCall } from '@grpc/grpc-js/build/src/server-call';
import { ServerUnaryCall, ServerWritableStream, sendUnaryData } from '@grpc/grpc-js';
import { emptyWithLog, errorResponse } from './response-util';


export class PlaywrightServer implements IPlaywrightServer {
    private states: { [peer: string]: PlaywrightState } = {};

    private getState = (peer: ServerSurfaceCall): PlaywrightState => {
        const p = peer.getPeer();
        if (!(p in this.states)) {
            this.states[p] = new PlaywrightState();
        }
        return this.states[p];
    };
    private getActiveBrowser = (peer: ServerSurfaceCall) => this.getState(peer).getActiveBrowser();
    private getActiveContext = (peer: ServerSurfaceCall) => this.getState(peer).getActiveContext();
    private getActivePage = (peer: ServerSurfaceCall) => {
        const page = this.getState(peer).getActivePage();
        if (!page) throw Error('No page open.');
        return page;
    };

    private wrapping = <T, K>(
        func: (request: T, state: PlaywrightState) => Promise<K>,
    ): ((call: ServerUnaryCall<T, K>, callback: sendUnaryData<K>) => Promise<void>) => {
        return async (call: ServerUnaryCall<T, K>, callback: sendUnaryData<K>) => {
            try {
                const request = call.request;
                if (request === null) throw Error('No request');
                const response = await func(request, this.getState(call));
                callback(null, response);
            } catch (e) {
                callback(errorResponse(e), null);
            }
        };
    };

    async initializeExtension(
        call: ServerUnaryCall<Request.FilePath, Response.Keywords>,
        callback: sendUnaryData<Response.Keywords>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await playwrightState.initializeExtension(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async callExtensionKeyword(call: ServerWritableStream<Request.KeywordCall, Response.Json>): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await playwrightState.extensionKeywordCall(request, call, this.getState(call));
            call.write(result);
        } catch (e) {
            call.emit('error', errorResponse(e));
        }
        call.end();
    }

    async closeBrowser(
        call: ServerUnaryCall<Request.Empty, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const result = await playwrightState.closeBrowser(this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }
    async closeAllBrowsers(
        call: ServerUnaryCall<Request.Empty, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const result = await playwrightState.closeAllBrowsers(this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async closeContext(
        call: ServerUnaryCall<Request.Empty, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const result = await playwrightState.closeContext(this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async closePage(
        call: ServerUnaryCall<Request.Empty, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const result = await playwrightState.closePage(this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getBrowserCatalog(
        call: ServerUnaryCall<Request.Empty, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const result = await playwrightState.getBrowserCatalog(this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getCookies(
        call: ServerUnaryCall<Request.Empty, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const context = this.getActiveContext(call);
            if (!context) throw Error('no open context.');
            const result = await cookie.getCookies(context);
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async addCookie(
        call: ServerUnaryCall<Request.Json, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const context = this.getActiveContext(call);
            if (!context) throw Error('no open context.');
            const result = await cookie.addCookie(request, context);
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async deleteAllCookies(
        call: ServerUnaryCall<Request.Empty, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const context = this.getActiveContext(call);
            if (!context) throw Error('no open context.');
            const result = await cookie.deleteAllCookies(context);
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async switchPage(
        call: ServerUnaryCall<Request.IdWithTimeout, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await playwrightState.switchPage(request, this.getState(call).getActiveBrowser());
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async switchContext(
        call: ServerUnaryCall<Request.Index, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await playwrightState.switchContext(request, this.getState(call).getActiveBrowser());
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async switchBrowser(
        call: ServerUnaryCall<Request.Index, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await playwrightState.switchBrowser(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async newPage(
        call: ServerUnaryCall<Request.Url, Response.String>,
        callback: sendUnaryData<Response.NewPageResponse>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await playwrightState.newPage(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async newContext(
        call: ServerUnaryCall<Request.Context, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await playwrightState.newContext(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async newBrowser(
        call: ServerUnaryCall<Request.Browser, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await playwrightState.newBrowser(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async connectToBrowser(
        call: ServerUnaryCall<Request.ConnectBrowser, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await playwrightState.connectToBrowser(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async goTo(
        call: ServerUnaryCall<Request.Url, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await browserControl.goTo(request, this.getActivePage(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async goBack(
        call: ServerUnaryCall<Request.Empty, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            await this.getActivePage(call).goBack();
            callback(null, emptyWithLog('Did Go Back'));
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async goForward(
        call: ServerUnaryCall<Request.Empty, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            await this.getActivePage(call).goForward();
            callback(null, emptyWithLog('Did Go Forward'));
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async takeScreenshot(
        call: ServerUnaryCall<Request.ScreenshotOptions, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await browserControl.takeScreenshot(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getBoundingBox(
        call: ServerUnaryCall<Request.ElementSelector, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await getters.getBoundingBox(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getPageSource(
        call: ServerUnaryCall<Request.Empty, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const response = await getters.getPageSource(this.getActivePage(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async setTimeout(
        call: ServerUnaryCall<Request.Timeout, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await browserControl.setTimeout(request, this.getActiveBrowser(call)?.context?.c);
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getTitle(
        call: ServerUnaryCall<Request.Empty, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const response = await getters.getTitle(this.getActivePage(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getUrl(
        call: ServerUnaryCall<Request.Empty, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const response = await getters.getUrl(this.getActivePage(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getElementCount(
        call: ServerUnaryCall<Request.ElementSelector, Response.Int>,
        callback: sendUnaryData<Response.Int>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await getters.getElementCount(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getSelectContent(
        call: ServerUnaryCall<Request.ElementSelector, Response.Select>,
        callback: sendUnaryData<Response.Select>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await getters.getSelectContent(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getDomProperty(
        call: ServerUnaryCall<Request.ElementProperty, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await getters.getDomProperty(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getText(
        call: ServerUnaryCall<Request.ElementSelector, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await getters.getText(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getBoolProperty(
        call: ServerUnaryCall<Request.ElementProperty, Response.Bool>,
        callback: sendUnaryData<Response.Bool>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await getters.getBoolProperty(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getElementAttribute(
        call: ServerUnaryCall<Request.ElementProperty, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await getters.getElementAttribute(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getStyle(
        call: ServerUnaryCall<Request.ElementSelector, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await getters.getStyle(request, this.getState(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getViewportSize(
        call: ServerUnaryCall<Request.Empty, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const response = await getters.getViewportSize(this.getActivePage(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async selectOption(
        call: ServerUnaryCall<Request.SelectElementSelector, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.selectOption(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async deselectOption(
        call: ServerUnaryCall<Request.ElementSelector, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ) {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.deSelectOption(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async inputText(
        call: ServerUnaryCall<Request.TextInput, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.inputText(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async typeText(
        call: ServerUnaryCall<Request.TypeText, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.typeText(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async fillText(
        call: ServerUnaryCall<Request.FillText, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.fillText(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async clearText(
        call: ServerUnaryCall<Request.ClearText, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.clearText(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async press(
        call: ServerUnaryCall<Request.PressKeys, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.press(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async click(
        call: ServerUnaryCall<Request.ElementSelectorWithOptions, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.click(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async hover(
        call: ServerUnaryCall<Request.ElementSelectorWithOptions, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.hover(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async focus(
        call: ServerUnaryCall<Request.ElementSelector, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.focus(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async checkCheckbox(
        call: ServerUnaryCall<Request.ElementSelector, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.checkCheckbox(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async uncheckCheckbox(
        call: ServerUnaryCall<Request.ElementSelector, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.uncheckCheckbox(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getElement(
        call: ServerUnaryCall<Request.ElementSelector, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await evaluation.getElement(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getElements(
        call: ServerUnaryCall<Request.ElementSelector, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await evaluation.getElements(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async addStyleTag(
        call: ServerUnaryCall<Request.StyleTag, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await evaluation.addStyleTag(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async waitForElementsState(
        call: ServerUnaryCall<Request.ElementSelectorWithOptions, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await evaluation.waitForElementState(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async waitForRequest(
        call: ServerUnaryCall<Request.HttpCapture, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const page = this.getActivePage(call);
            if (!page) throw Error('No page open.');
            const result = await network.waitForRequest(request, page);
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async waitForResponse(
        call: ServerUnaryCall<Request.HttpCapture, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await network.waitForResponse(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async waitUntilNetworkIsIdle(
        call: ServerUnaryCall<Request.Timeout, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await network.waitUntilNetworkIsIdle(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async waitForNavigation(
        call: ServerUnaryCall<Request.Url, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await network.waitForNavigation(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async waitForFunction(
        call: ServerUnaryCall<Request.WaitForFunctionOptions, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await evaluation.waitForFunction(request, this.getState(call), this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async waitForDownload(
        call: ServerUnaryCall<Request.FilePath, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await network.waitForDownload(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async executeJavascript(
        call: ServerUnaryCall<Request.JavascriptCode, Response.JavascriptExecutionResult>,
        callback: sendUnaryData<Response.JavascriptExecutionResult>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await evaluation.executeJavascript(request, this.getState(call), this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getPageState(
        call: ServerUnaryCall<Request.Empty, Response.JavascriptExecutionResult>,
        callback: sendUnaryData<Response.JavascriptExecutionResult>,
    ): Promise<void> {
        try {
            const result = await evaluation.getPageState(this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async health(
        call: ServerUnaryCall<Request.Empty, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        const response = new Response.String();
        response.setBody('OK');
        callback(null, response);
    }

    async highlightElements(
        call: ServerUnaryCall<Request.ElementSelectorWithDuration, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await evaluation.highlightElements(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async download(
        call: ServerUnaryCall<Request.Url, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await evaluation.download(request, this.getState(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async setViewportSize(
        call: ServerUnaryCall<Request.Viewport, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await browserControl.setViewportSize(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async httpRequest(
        call: ServerUnaryCall<Request.HttpRequest, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await network.httpRequest(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getDevice(
        call: ServerUnaryCall<Request.Device, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = deviceDescriptors.getDevice(request);
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }
    async getDevices(
        call: ServerUnaryCall<Request.Empty, Response.Json>,
        callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = deviceDescriptors.getDevices();
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async uploadFile(
        call: ServerUnaryCall<Request.FilePath, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.uploadFile(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async handleAlert(
        call: ServerUnaryCall<Request.AlertAction, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.handleAlert(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async mouseMove(
        call: ServerUnaryCall<Request.Json, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.mouseMove(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async mouseButton(
        call: ServerUnaryCall<Request.MouseButtonOptions, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.mouseButton(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async keyboardKey(
        call: ServerUnaryCall<Request.KeyboardKeypress, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.keyboardKey(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async keyboardInput(
        call: ServerUnaryCall<Request.KeyboardInputOptions, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await interaction.keyboardInput(request, this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async setOffline(
        call: ServerUnaryCall<Request.Bool, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await browserControl.setOffline(request, this.getActiveContext(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async setGeolocation(
        call: ServerUnaryCall<Request.Json, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await browserControl.setGeolocation(request, this.getActiveContext(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async reload(
        call: ServerUnaryCall<Request.Empty, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const result = await browserControl.reload(this.getActivePage(call));
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }
}
