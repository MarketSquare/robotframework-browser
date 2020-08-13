import { Server, ServerUnaryCall, sendUnaryData } from 'grpc';

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
import { class_async_timer } from './execution-time-decorators';

@class_async_timer
export class PlaywrightServer implements IPlaywrightServer {
    state: PlaywrightState;

    constructor() {
        this.state = new PlaywrightState();
    }

    private getActiveBrowser = <T>(callback: sendUnaryData<T>) => this.state.getActiveBrowser(callback);
    private getActiveContext = () => this.state.getActiveContext();
    private getActivePage = () => this.state.getActivePage();
    async closeBrowser(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return playwrightState.closeBrowser(callback, this.state);
    }
    async closeAllBrowsers(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return playwrightState.closeAllBrowsers(callback, this.state);
    }

    async closeContext(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return playwrightState.closeContext(callback, this.state);
    }

    async closePage(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return playwrightState.closePage(callback, this.state);
    }

    async getBrowserCatalog(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return playwrightState.getBrowserCatalog(callback, this.state);
    }

    async getCookies(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        return cookie.getCookies(callback, this.getActiveContext());
    }

    async addCookie(call: ServerUnaryCall<Request.Json>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return cookie.addCookie(call, callback, this.getActiveContext());
    }

    async deleteAllCookies(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return cookie.deleteAllCookies(callback, this.getActiveContext());
    }

    async autoActivatePages(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return playwrightState.autoActivatePages(call, callback, this.getActiveBrowser(callback));
    }

    async switchPage(call: ServerUnaryCall<Request.Index>, callback: sendUnaryData<Response.Int>): Promise<void> {
        return playwrightState.switchPage(call, callback, this.state.getActiveBrowser(callback));
    }

    async switchContext(call: ServerUnaryCall<Request.Index>, callback: sendUnaryData<Response.Int>): Promise<void> {
        return playwrightState.switchContext(call, callback, this.state.getActiveBrowser(callback));
    }

    async switchBrowser(call: ServerUnaryCall<Request.Index>, callback: sendUnaryData<Response.Int>): Promise<void> {
        return playwrightState.switchBrowser(call, callback, this.state);
    }

    async newPage(call: ServerUnaryCall<Request.Url>, callback: sendUnaryData<Response.Int>): Promise<void> {
        return playwrightState.newPage(call, callback, this.state);
    }

    async newContext(call: ServerUnaryCall<Request.Context>, callback: sendUnaryData<Response.Int>): Promise<void> {
        return playwrightState.newContext(call, callback, this.state);
    }

    async newBrowser(call: ServerUnaryCall<Request.Browser>, callback: sendUnaryData<Response.Int>): Promise<void> {
        return playwrightState.newBrowser(call, callback, this.state);
    }

    async goTo(call: ServerUnaryCall<Request.Url>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return browserControl.goTo(call, callback, this.getActivePage());
    }

    async goBack(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return browserControl.goBack(callback, this.getActivePage());
    }

    async goForward(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return browserControl.goForward(callback, this.getActivePage());
    }

    async takeScreenshot(
        call: ServerUnaryCall<Request.ScreenshotOptions>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return browserControl.takeScreenshot(call, callback, this.state);
    }

    async getBoundingBox(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return getters.getBoundingBox(call, callback, this.state);
    }

    async getPageSource(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        return getters.getPageSource(call, callback, this.getActivePage());
    }

    async setTimeout(call: ServerUnaryCall<Request.Timeout>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return browserControl.setTimeout(call, callback, this.getActiveBrowser(callback)?.context?.c);
    }

    async getTitle(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        return getters.getTitle(callback, this.getActivePage());
    }

    async getUrl(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        return getters.getUrl(callback, this.getActivePage());
    }

    async getElementCount(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Int>,
    ): Promise<void> {
        return getters.getElementCount(call, callback, this.state);
    }

    async getSelectContent(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Select>,
    ): Promise<void> {
        return getters.getSelectContent(call, callback, this.state);
    }

    async getDomProperty(
        call: ServerUnaryCall<Request.ElementProperty>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return getters.getDomProperty(call, callback, this.state);
    }

    async getBoolProperty(
        call: ServerUnaryCall<Request.ElementProperty>,
        callback: sendUnaryData<Response.Bool>,
    ): Promise<void> {
        return getters.getBoolProperty(call, callback, this.state);
    }

    async getStyle(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return getters.getStyle(call, callback, this.state);
    }

    async getViewportSize(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return getters.getViewportSize(call, callback, this.getActivePage());
    }

    async selectOption(
        call: ServerUnaryCall<Request.SelectElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.selectOption(call, callback, this.state);
    }

    async deselectOption(call: ServerUnaryCall<Request.ElementSelector>, callback: sendUnaryData<Response.Empty>) {
        return interaction.deSelectOption(call, callback, this.state);
    }

    async inputText(call: ServerUnaryCall<Request.TextInput>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return interaction.inputText(call, callback, this.state);
    }

    async typeText(call: ServerUnaryCall<Request.TypeText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return interaction.typeText(call, callback, this.state);
    }

    async fillText(call: ServerUnaryCall<Request.FillText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return interaction.fillText(call, callback, this.state);
    }

    async clearText(call: ServerUnaryCall<Request.ClearText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return interaction.clearText(call, callback, this.state);
    }

    async press(call: ServerUnaryCall<Request.PressKeys>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return interaction.press(call, callback, this.state);
    }

    async click(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.click(call, callback, this.state);
    }

    async clickWithOptions(
        call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.clickWithOptions(call, callback, this.state);
    }

    async focus(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.focus(call, callback, this.state);
    }

    async checkCheckbox(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.checkCheckbox(call, callback, this.state);
    }

    async uncheckCheckbox(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.uncheckCheckbox(call, callback, this.state);
    }

    async getElement(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return evaluation.getElement(call, callback, this.state);
    }

    async getElements(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return evaluation.getElements(call, callback, this.state);
    }

    async addStyleTag(call: ServerUnaryCall<Request.StyleTag>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return evaluation.addStyleTag(call, callback, this.getActivePage());
    }

    async waitForElementsState(
        call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return evaluation.waitForElementState(call, callback, this.state);
    }
    async waitForRequest(call: ServerUnaryCall<Request.HttpCapture>, callback: sendUnaryData<Response.String>) {
        return network.waitForRequest(call, callback, this.getActivePage());
    }
    async waitForResponse(call: ServerUnaryCall<Request.HttpCapture>, callback: sendUnaryData<Response.String>) {
        return network.waitForResponse(call, callback, this.getActivePage());
    }
    async waitUntilNetworkIsIdle(call: ServerUnaryCall<Request.Timeout>, callback: sendUnaryData<Response.Empty>) {
        return network.waitUntilNetworkIsIdle(call, callback, this.getActivePage());
    }

    async waitForFunction(
        call: ServerUnaryCall<Request.WaitForFunctionOptions>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return evaluation.waitForFunction(call, callback, this.state);
    }

    async waitForDownload(
        call: ServerUnaryCall<Request.FilePath>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return network.waitForDownload(call, callback, this.getActivePage());
    }

    async executeJavascript(
        call: ServerUnaryCall<Request.JavascriptCode>,
        callback: sendUnaryData<Response.JavascriptExecutionResult>,
    ): Promise<void> {
        return evaluation.executeJavascript(call, callback, this.state);
    }

    async getPageState(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.JavascriptExecutionResult>,
    ): Promise<void> {
        return evaluation.getPageState(callback, this.getActivePage());
    }

    async health(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        const response = new Response.String();
        response.setBody('OK');
        callback(null, response);
        return;
    }

    async highlightElements(
        call: ServerUnaryCall<Request.ElementSelectorWithDuration>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return evaluation.highlightElements(call, callback, this.state);
    }

    async setViewportSize(
        call: ServerUnaryCall<Request.Viewport>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return browserControl.setViewportSize(call, callback, this.getActivePage());
    }

    async httpRequest(
        call: ServerUnaryCall<Request.HttpRequest>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        return network.httpRequest(call, callback, this.getActivePage());
    }

    async getDevice(call: ServerUnaryCall<Request.Device>, callback: sendUnaryData<Response.String>): Promise<void> {
        return deviceDescriptors.getDevice(call, callback);
    }
    async getDevices(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        return deviceDescriptors.getDevices(callback);
    }

    async uploadFile(call: ServerUnaryCall<Request.FilePath>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return interaction.uploadFile(call, callback, this.getActivePage());
    }

    async handleAlert(
        call: ServerUnaryCall<Request.AlertAction>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.handleAlert(call, callback, this.getActivePage());
    }

    async mouseMove(call: ServerUnaryCall<Request.Json>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return interaction.mouseMove(call, callback, this.getActivePage());
    }

    async mouseButton(
        call: ServerUnaryCall<Request.MouseButtonOptions>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.mouseButton(call, callback, this.getActivePage());
    }

    async keyboardKey(
        call: ServerUnaryCall<Request.KeyboardKeypress>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.keyboardKey(call, callback, this.getActivePage());
    }

    async keyboardInput(
        call: ServerUnaryCall<Request.KeyboardInputOptions>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        return interaction.keyboardInput(call, callback, this.getActivePage());
    }

    async setOffline(call: ServerUnaryCall<Request.Bool>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        return browserControl.setOffline(call, callback, this.getActiveContext());
    }
}
