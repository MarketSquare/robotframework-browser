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
    private getActivePage = <T>(callback: sendUnaryData<T>) => this.openBrowsers.getActivePage(callback);

    async closeBrowser(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        playwrightState.closeBrowser(callback, this.openBrowsers);
    }
    async closeAllBrowsers(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        playwrightState.closeAllBrowsers(callback, this.openBrowsers);
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

    async createPage(call: ServerUnaryCall<Request.Url>, callback: sendUnaryData<Response.Int>): Promise<void> {
        playwrightState.createPage(call, callback, this.openBrowsers);
    }

    async createContext(call: ServerUnaryCall<Request.Context>, callback: sendUnaryData<Response.Int>): Promise<void> {
        playwrightState.createContext(call, callback, this.openBrowsers);
    }

    async createBrowser(call: ServerUnaryCall<Request.Browser>, callback: sendUnaryData<Response.Int>): Promise<void> {
        playwrightState.createBrowser(call, callback, this.openBrowsers);
    }

    async goTo(call: ServerUnaryCall<Request.Url>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        browserControl.goTo(call, callback, this.getActivePage(callback));
    }

    async goBack(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        browserControl.goBack(callback, this.getActivePage(callback));
    }

    async goForward(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        browserControl.goForward(callback, this.getActivePage(callback));
    }

    async takeScreenshot(
        call: ServerUnaryCall<Request.ScreenshotPath>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        browserControl.takeScreenshot(call, callback, this.getActivePage(callback));
    }

    async setTimeout(call: ServerUnaryCall<Request.Timeout>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        browserControl.setTimeout(call, callback, this.getActiveBrowser(callback)?.context?.c);
    }

    async getTitle(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        getters.getTitle(callback, this.getActivePage(callback));
    }

    async getUrl(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        getters.getUrl(callback, this.getActivePage(callback));
    }

    async getTextContent(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        getters.getTextContent(call, callback, this.getActivePage(callback));
    }

    async getElementCount(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Int>,
    ): Promise<void> {
        getters.getElementCount(call, callback, this.getActivePage(callback));
    }

    async getSelectContent(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Select>,
    ): Promise<void> {
        getters.getSelectContent(call, callback, this.getActivePage(callback));
    }

    async getDomProperty(
        call: ServerUnaryCall<Request.ElementProperty>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        getters.getDomProperty(call, callback, this.getActivePage(callback));
    }

    async getBoolProperty(
        call: ServerUnaryCall<Request.ElementProperty>,
        callback: sendUnaryData<Response.Bool>,
    ): Promise<void> {
        getters.getBoolProperty(call, callback, this.getActivePage(callback));
    }

    async selectOption(
        call: ServerUnaryCall<Request.SelectElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        interaction.selectOption(call, callback, this.getActivePage(callback));
    }

    async deselectOption(call: ServerUnaryCall<Request.ElementSelector>, callback: sendUnaryData<Response.Empty>) {
        interaction.deSelectOption(call, callback, this.getActivePage(callback));
    }

    async inputText(call: ServerUnaryCall<Request.TextInput>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        interaction.inputText(call, callback, this.getActivePage(callback));
    }

    async typeText(call: ServerUnaryCall<Request.TypeText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        interaction.typeText(call, callback, this.getActivePage(callback));
    }

    async fillText(call: ServerUnaryCall<Request.FillText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        interaction.fillText(call, callback, this.getActivePage(callback));
    }

    async clearText(call: ServerUnaryCall<Request.ClearText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        interaction.clearText(call, callback, this.getActivePage(callback));
    }

    async press(call: ServerUnaryCall<Request.PressKeys>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        interaction.press(call, callback, this.getActivePage(callback));
    }

    async click(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        interaction.click(call, callback, this.getActivePage(callback));
    }

    async clickWithOptions(
        call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        interaction.clickWithOptions(call, callback, this.getActivePage(callback));
    }

    async focus(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        interaction.focus(call, callback, this.getActivePage(callback));
    }

    async checkCheckbox(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        interaction.checkCheckbox(call, callback, this.getActivePage(callback));
    }

    async uncheckCheckbox(
        call: ServerUnaryCall<Request.ElementSelector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        interaction.uncheckCheckbox(call, callback, this.getActivePage(callback));
    }

    async addStyleTag(call: ServerUnaryCall<Request.StyleTag>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        evaluation.addStyleTag(call, callback, this.getActivePage(callback));
    }

    async waitForElementsState(
        call: ServerUnaryCall<Request.ElementSelectorWithOptions>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        evaluation.waitForElementState(call, callback, this.getActivePage(callback));
    }

    async executeJavascriptOnPage(
        call: ServerUnaryCall<Request.JavascriptCode>,
        callback: sendUnaryData<Response.JavascriptExecutionResult>,
    ): Promise<void> {
        evaluation.executeJavascriptOnPage(call, callback, this.getActivePage(callback));
    }

    async getPageState(
        call: ServerUnaryCall<Request.Empty>,
        callback: sendUnaryData<Response.JavascriptExecutionResult>,
    ): Promise<void> {
        evaluation.getPageState(callback, this.getActivePage(callback));
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
        evaluation.highlightElements(call, callback, this.getActivePage(callback));
    }
}
