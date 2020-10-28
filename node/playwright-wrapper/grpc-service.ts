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
import * as playwrightState from './playwright-state';
import { IPlaywrightServer } from './generated/playwright_grpc_pb';
import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { ServerUnaryCall, sendUnaryData } from '@grpc/grpc-js';

export class PlaywrightServer implements IPlaywrightServer {
    state: PlaywrightState;

    constructor() {
        this.state = new PlaywrightState();
    }

    private getActiveBrowser = () => this.state.getActiveBrowser();
    private getActiveContext = () => this.state.getActiveContext();
    private getActivePage = () => this.state.getActivePage();

    async closeBrowser(
        call: ServerUnaryCall<Request.Empty, Response.String>,
        callback: sendUnaryData<Response.String>): Promise<void> {
        try {
            const result = await playwrightState.closeBrowser(this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }
    async closeAllBrowsers(
        call: ServerUnaryCall<Request.Empty, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const result = await playwrightState.closeAllBrowsers(this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async closeContext(call: ServerUnaryCall<Request.Empty, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        try {
            const result = await playwrightState.closeContext(this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async closePage(call: ServerUnaryCall<Request.Empty, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        try {
            const result = await playwrightState.closePage(this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async getBrowserCatalog(
        call: ServerUnaryCall<Request.Empty, Response.Json>, callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const result = await playwrightState.getBrowserCatalog(this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async getCookies(call: ServerUnaryCall<Request.Empty, Response.Json>, callback: sendUnaryData<Response.Json>): Promise<void> {
        try {
            const result = await cookie.getCookies(this.getActiveContext());
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async addCookie(call: ServerUnaryCall<Request.Json, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error("No request");
            const result = await cookie.addCookie(request, this.getActiveContext());
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async deleteAllCookies(
        call: ServerUnaryCall<Request.Empty, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const result = await cookie.deleteAllCookies(this.getActiveContext());
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async switchPage(
        call: ServerUnaryCall<Request.IdWithTimeout, Response.String>, callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error("No request");
            const response = await playwrightState.switchPage(request, this.state.getActiveBrowser());
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async switchContext(call: ServerUnaryCall<Request.Index, Response.String>, callback: sendUnaryData<Response.String>): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error("No request");
            const response = await playwrightState.switchContext(request, this.state.getActiveBrowser());
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async switchBrowser(call: ServerUnaryCall<Request.Index, Response.String>, callback: sendUnaryData<Response.String>): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error("No request");
            const response = await playwrightState.switchBrowser(request, this.state);
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async newPage(call: ServerUnaryCall<Request.Url, Response.String>, callback: sendUnaryData<Response.String>): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error("No request");
            const response = await playwrightState.newPage(request, this.state);
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async newContext(call: ServerUnaryCall<Request.Context, Response.String>, callback: sendUnaryData<Response.String>): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error("No request");
            const response = await playwrightState.newContext(request, this.state);
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async newBrowser(call: ServerUnaryCall<Request.Browser, Response.String>, callback: sendUnaryData<Response.String>): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error("No request");
            const response = await playwrightState.newBrowser(request, this.state);
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async goTo(call: ServerUnaryCall<Request.Url, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error("No request");
            const response = await browserControl.goTo(request, this.getActivePage());
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async goBack(call: ServerUnaryCall<Request.Empty, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        try {
            const response = await browserControl.goBack(this.getActivePage());
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async goForward(call: ServerUnaryCall<Request.Empty, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        try {
            const response = await browserControl.goForward(this.getActivePage());
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async takeScreenshot(
        call: ServerUnaryCall<Request.ScreenshotOptions, Response.String>, callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const response = await browserControl.takeScreenshot(call, this.state);
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async getBoundingBox(
        call: ServerUnaryCall<Request.ElementSelector, Response.Json>, callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error("No request");
            const response = await getters.getBoundingBox(request, this.state);
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    // <--- HERE ---> // CONTINUE CALL AND CALLBACKS!

    async getPageSource(call: ServerUnaryCall<Request.Empty, Response.String>, callback: sendUnaryData<Response.String>): Promise<void> {
        return getters.getPageSource(call, callback, this.getActivePage());
    }

    async setTimeout(call: ServerUnaryCall<Request.Timeout, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return browserControl.setTimeout(call, callback, this.getActiveBrowser()?.context?.c);
    }

    async getTitle(call: ServerUnaryCall<Request.Empty, Response.String>, callback: sendUnaryData<Response.String>): Promise<void> {
        return getters.getTitle(callback, this.getActivePage());
    }

    async getUrl(call: ServerUnaryCall<Request.Empty, Response.String>, callback: sendUnaryData<Response.String>): Promise<void> {
        return getters.getUrl(callback, this.getActivePage());
    }

    async getElementCount(
        call: ServerUnaryCall<Request.ElementSelector, Response.Int>, callback: sendUnaryData<Response.Int>,
    ): Promise<void> {
        return getters.getElementCount(call, callback, this.state);
    }

    async getSelectContent(
        call: ServerUnaryCall<Request.ElementSelector, Response.Select>, callback: sendUnaryData<Response.Select>,
    ): Promise<void> {
        try {
            const response = await getters.getSelectContent(call, this.state);
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async getDomProperty(
        call: ServerUnaryCall<Request.ElementProperty, Response.String>, callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        try {
            const response = await getters.getDomProperty(call, this.state);
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async getBoolProperty(
        call: ServerUnaryCall<Request.ElementProperty, Response.Bool>, callback: sendUnaryData<Response.Bool>,
    ): Promise<void> {
        try {
            const response = await getters.getBoolProperty(call, this.state);
            callback(null, response);
        } catch (e) {
            callback(e, null);
        }
    }

    async getElementAttribute(
        call: ServerUnaryCall<Request.ElementProperty, Response.String>, callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return getters.getElementAttribute(call, callback, this.state);
    }

    async getStyle(
        call: ServerUnaryCall<Request.ElementSelector, Response.Json>, callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        return getters.getStyle(call, callback, this.state);
    }

    async getViewportSize(call: ServerUnaryCall<Request.Empty, Response.Json>, callback: sendUnaryData<Response.Json>): Promise<void> {
        return getters.getViewportSize(call, callback, this.getActivePage());
    }

    async selectOption(
        call: ServerUnaryCall<Request.SelectElementSelector, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const result = await interaction.selectOption(call, this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async deselectOption(call: ServerUnaryCall<Request.ElementSelector, Response.Empty>, callback: sendUnaryData<Response.Empty>) {
        try {
            const result = await interaction.deSelectOption(call, this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async inputText(call: ServerUnaryCall<Request.TextInput, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return interaction.inputText(call, callback, this.state);
    }

    async typeText(call: ServerUnaryCall<Request.TypeText, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        try {
            const result = await interaction.typeText(call, this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async fillText(call: ServerUnaryCall<Request.FillText, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        try {
            const result = await interaction.fillText(call, this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async clearText(call: ServerUnaryCall<Request.ClearText, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        try {
            const result = await interaction.clearText(call, this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async press(call: ServerUnaryCall<Request.PressKeys, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        try {
            const result = await interaction.press(call, this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async click(
        call: ServerUnaryCall<Request.ElementSelectorWithOptions, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const result = await interaction.click(call, this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async hover(
        call: ServerUnaryCall<Request.ElementSelectorWithOptions, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.hover(call, callback, this.state);
    }

    async focus(
        call: ServerUnaryCall<Request.ElementSelector, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.focus(call, callback, this.state);
    }

    async checkCheckbox(
        call: ServerUnaryCall<Request.ElementSelector, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.checkCheckbox(call, callback, this.state);
    }

    async uncheckCheckbox(
        call: ServerUnaryCall<Request.ElementSelector, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.uncheckCheckbox(call, callback, this.state);
    }

    async getElement(
        call: ServerUnaryCall<Request.ElementSelector, Response.String>, callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return evaluation.getElement(call, callback, this.state);
    }

    async getElements(
        call: ServerUnaryCall<Request.ElementSelector, Response.Json>, callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const result = await evaluation.getElements(call, this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async addStyleTag(call: ServerUnaryCall<Request.StyleTag, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return evaluation.addStyleTag(call, callback, this.getActivePage());
    }

    async waitForElementsState(
        call: ServerUnaryCall<Request.ElementSelectorWithOptions, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const result = await evaluation.waitForElementState(call, this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }
    async waitForRequest(
        call: ServerUnaryCall<Request.HttpCapture, Response.String>, callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return network.waitForRequest(call, callback, this.getActivePage());
    }
    async waitForResponse(
        call: ServerUnaryCall<Request.HttpCapture, Response.Json>, callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        return network.waitForResponse(call, callback, this.getActivePage());
    }
    async waitUntilNetworkIsIdle(
        call: ServerUnaryCall<Request.Timeout, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return network.waitUntilNetworkIsIdle(call, callback, this.getActivePage());
    }

    async waitForFunction(
        call: ServerUnaryCall<Request.WaitForFunctionOptions, Response.Json>, callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        try {
            const result = await evaluation.waitForFunction(call, this.state);
            callback(null, result);
        } catch (e) {
            callback(e, null);
        }
    }

    async waitForDownload(
        call: ServerUnaryCall<Request.FilePath, Response.Json>, callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        return network.waitForDownload(call, callback, this.getActivePage());
    }

    async executeJavascript(
        call: ServerUnaryCall<Request.JavascriptCode, Response.JavascriptExecutionResult>, callback: sendUnaryData<Response.JavascriptExecutionResult>,
    ): Promise<void> {
        return evaluation.executeJavascript(call, callback, this.state);
    }

    async getPageState(
        call: ServerUnaryCall<Request.Empty, Response.JavascriptExecutionResult>, callback: sendUnaryData<Response.JavascriptExecutionResult>,
    ): Promise<void> {
        return evaluation.getPageState(callback, this.getActivePage());
    }

    async health(call: ServerUnaryCall<Request.Empty, Response.String>, callback: sendUnaryData<Response.String>): Promise<void> {
        const response = new Response.String();
        response.setBody('OK');
        callback(null, response);
        return;
    }

    async highlightElements(
        call: ServerUnaryCall<Request.ElementSelectorWithDuration, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return evaluation.highlightElements(call, callback, this.state);
    }

    async download(call: ServerUnaryCall<Request.Url, Response.String>, callback: sendUnaryData<Response.String>): Promise<void> {
        return evaluation.download(call, callback, this.state);
    }

    async setViewportSize(
        call: ServerUnaryCall<Request.Viewport, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return browserControl.setViewportSize(call, callback, this.getActivePage());
    }

    async httpRequest(
        call: ServerUnaryCall<Request.HttpRequest, Response.Json>, callback: sendUnaryData<Response.Json>,
    ): Promise<void> {
        return network.httpRequest(call, callback, this.getActivePage());
    }

    async getDevice(call: ServerUnaryCall<Request.Device, Response.Json>, callback: sendUnaryData<Response.Json>): Promise<void> {
        return deviceDescriptors.getDevice(call, callback);
    }
    async getDevices(call: ServerUnaryCall<Request.Empty, Response.Json>, callback: sendUnaryData<Response.Json>): Promise<void> {
        return deviceDescriptors.getDevices(callback);
    }

    async uploadFile(call: ServerUnaryCall<Request.FilePath, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return interaction.uploadFile(call, callback, this.getActivePage());
    }

    async handleAlert(
        call: ServerUnaryCall<Request.AlertAction, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.handleAlert(call, callback, this.getActivePage());
    }

    async mouseMove(call: ServerUnaryCall<Request.Json, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return interaction.mouseMove(call, callback, this.getActivePage());
    }

    async mouseButton(
        call: ServerUnaryCall<Request.MouseButtonOptions, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.mouseButton(call, callback, this.getActivePage());
    }

    async keyboardKey(
        call: ServerUnaryCall<Request.KeyboardKeypress, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.keyboardKey(call, callback, this.getActivePage());
    }

    async keyboardInput(
        call: ServerUnaryCall<Request.KeyboardInputOptions, Response.Empty>, callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.keyboardInput(call, callback, this.getActivePage());
    }

    async setOffline(call: ServerUnaryCall<Request.Bool, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return browserControl.setOffline(call, callback, this.getActiveContext());
    }

    async setGeolocation(call: ServerUnaryCall<Request.Json, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return browserControl.setGeolocation(call, callback, this.getActiveContext());
    }

    async reload(call: ServerUnaryCall<Request.Empty, Response.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return browserControl.reload(call, callback, this.getActivePage());
    }
}
