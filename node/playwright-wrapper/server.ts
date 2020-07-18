import { sendUnaryData, ServerUnaryCall } from 'grpc';

import { IPlaywrightServer } from './generated/playwright_grpc_pb';
import { Response, Request } from './generated/playwright_pb';
import * as browserControl from './browser-control';
import * as evaluation from './evaluation';
import * as getters from './getters';
import * as interaction from './interaction';
import * as playwrightState from './playwright-state';
import { PlaywrightState } from './playwright-state';

export class PlaywrightServer implements IPlaywrightServer {
    openBrowsers: PlaywrightState;

    constructor() {
        this.openBrowsers = new PlaywrightState();
    }
    private getActiveBrowser = <T>(callback: sendUnaryData<T>) => this.openBrowsers.getActiveBrowser(callback);
    private getActivePage = () => this.openBrowsers.getActivePage();

    async closeBrowser(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        playwrightState.closeBrowser(callback, this.openBrowsers);
    }
    async closeAllBrowsers(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        playwrightState.closeAllBrowsers(callback, this.openBrowsers);
    }

    async closeContext(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        playwrightState.closeContext(callback, this.openBrowsers);
    }

    async closePage(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        playwrightState.closePage(callback, this.openBrowsers);
    }

    async getBrowserCatalog(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        playwrightState.getBrowserCatalog(callback, this.openBrowsers);
    }

    async autoActivatePages(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        playwrightState.autoActivatePages(call, callback, this.getActiveBrowser(callback));
    }

    async switchPage(call: ServerUnaryCall<Request.Index>, callback: sendUnaryData<Response.Int>): Promise<void> {
        playwrightState.switchPage(call, callback, this.openBrowsers.getActiveBrowser(callback));
    }

    async switchContext(call: ServerUnaryCall<Request.Index>, callback: sendUnaryData<Response.Int>): Promise<void> {
        playwrightState.switchContext(call, callback, this.openBrowsers.getActiveBrowser(callback));
    }

    async switchBrowser(call: ServerUnaryCall<Request.Index>, callback: sendUnaryData<Response.Int>): Promise<void> {
        playwrightState.switchBrowser(call, callback, this.openBrowsers);
    }

    async newPage(call: ServerUnaryCall<Request.Url>, callback: sendUnaryData<Response.Int>): Promise<void> {
        playwrightState.newPage(call, callback, this.openBrowsers);
    }

    async newContext(call: ServerUnaryCall<Request.Context>, callback: sendUnaryData<Response.Int>): Promise<void> {
        playwrightState.newContext(call, callback, this.openBrowsers);
    }

    async newBrowser(call: ServerUnaryCall<Request.Browser>, callback: sendUnaryData<Response.Int>): Promise<void> {
        playwrightState.newBrowser(call, callback, this.openBrowsers);
    }

    async goTo(call: ServerUnaryCall<Request.Url>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        browserControl.goTo(call, callback, this.getActivePage());
    }

    async goBack(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        browserControl.goBack(callback, this.getActivePage());
    }

    async goForward(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        browserControl.goForward(callback, this.getActivePage());
    }

    async takeScreenshot(
        call: ServerUnaryCall<Request.ScreenshotPath>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        browserControl.takeScreenshot(call, callback, this.getActivePage());
    }

    async setTimeout(call: ServerUnaryCall<Request.Timeout>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        browserControl.setTimeout(call, callback, this.getActiveBrowser(callback)?.context?.c);
    }

    async getTitle(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        getters.getTitle(callback, this.getActivePage());
    }

    async getUrl(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        getters.getUrl(callback, this.getActivePage());
    }

    async getTextContent(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        getters.getTextContent(call, callback, this.getActivePage());
    }

    async getElementCount(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Int>,
    ): Promise<void> {
        getters.getElementCount(call, callback, this.getActivePage());
    }

    async getSelectContent(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Select>,
    ): Promise<void> {
        getters.getSelectContent(call, callback, this.getActivePage());
    }

    async getDomProperty(
        call: ServerUnaryCall<Request.ElementProperty>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        getters.getDomProperty(call, callback, this.getActivePage());
    }

    async getBoolProperty(
        call: ServerUnaryCall<Request.ElementProperty>,
        callback: sendUnaryData<Response.Bool>,
    ): Promise<void> {
        getters.getBoolProperty(call, callback, this.getActivePage());
    }

    async getViewportSize(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        getters.getViewportSize(call, callback, this.getActivePage());
    }

    async selectOption(
        call: ServerUnaryCall<Request.SelectElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        interaction.selectOption(call, callback, this.getActivePage());
    }

    async deselectOption(call: ServerUnaryCall<Request.ElementSelector>, callback: sendUnaryData<Response.Empty>) {
        interaction.deSelectOption(call, callback, this.getActivePage());
    }

    async inputText(call: ServerUnaryCall<Request.TextInput>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        interaction.inputText(call, callback, this.getActivePage());
    }

    async typeText(call: ServerUnaryCall<Request.TypeText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        interaction.typeText(call, callback, this.getActivePage());
    }

    async fillText(call: ServerUnaryCall<Request.FillText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        interaction.fillText(call, callback, this.getActivePage());
    }

    async clearText(call: ServerUnaryCall<Request.ClearText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        interaction.clearText(call, callback, this.getActivePage());
    }

    async press(call: ServerUnaryCall<Request.PressKeys>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        interaction.press(call, callback, this.getActivePage());
    }

    async click(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        interaction.click(call, callback, this.getActivePage());
    }

    async clickWithOptions(
        call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        interaction.clickWithOptions(call, callback, this.getActivePage());
    }

    async focus(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        interaction.focus(call, callback, this.getActivePage());
    }

    async checkCheckbox(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        interaction.checkCheckbox(call, callback, this.getActivePage());
    }

    async uncheckCheckbox(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        interaction.uncheckCheckbox(call, callback, this.getActivePage());
    }

    async addStyleTag(call: ServerUnaryCall<Request.StyleTag>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        evaluation.addStyleTag(call, callback, this.getActivePage());
    }

    async waitForElementsState(
        call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        evaluation.waitForElementState(call, callback, this.getActivePage());
    }

    async executeJavascriptOnPage(
        call: ServerUnaryCall<Request.JavascriptCode>,
        callback: sendUnaryData<Response.JavascriptExecutionResult>,
    ): Promise<void> {
        evaluation.executeJavascriptOnPage(call, callback, this.getActivePage());
    }

    async getPageState(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.JavascriptExecutionResult>,
    ): Promise<void> {
        evaluation.getPageState(callback, this.getActivePage());
    }

    async health(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        const response = new Response.String();
        response.setBody('OK');
        callback(null, response);
    }

    async highlightElements(
        call: ServerUnaryCall<Request.ElementSelectorWithDuration>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        evaluation.highlightElements(call, callback, this.getActivePage());
    }

    async setViewportSize(
        call: ServerUnaryCall<Request.Viewport>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        browserControl.setViewportSize(call, callback, this.getActivePage());
    }
}
