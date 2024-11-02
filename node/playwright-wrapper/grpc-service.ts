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
import * as clock from './clock';
import * as cookie from './cookie';
import * as deviceDescriptors from './device-descriptors';
import * as evaluation from './evaluation';
import * as getters from './getters';
import * as interaction from './interaction';
import * as locatorHandler from './locator-handler';
import * as network from './network';
import * as pdf from './pdf';
import * as playwrightState from './playwright-state';
import { IPlaywrightServer } from './generated/playwright_grpc_pb';
import { Page } from 'playwright';
import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { ServerReadableStream, ServerUnaryCall, ServerWritableStream, sendUnaryData } from '@grpc/grpc-js';
import { ServerSurfaceCall } from '@grpc/grpc-js/build/src/server-call';
import { class_async_logger } from './keyword-decorators';
import { emptyWithLog, errorResponse, stringResponse } from './response-util';
import { pino } from 'pino';
const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

@class_async_logger
export class PlaywrightServer implements IPlaywrightServer {
    private states: { [peer: string]: PlaywrightState } = {};
    peerMap: { [peer: string]: string } = {};

    private createState = (key: string): PlaywrightState => {
        if (!(key in this.states)) {
            this.states[key] = new PlaywrightState();
        }
        return this.states[key];
    };

    private getState = (peer: ServerSurfaceCall): PlaywrightState => {
        const mapPeer = this.peerMap[peer.getPeer()];
        if (mapPeer) {
            return this.createState(mapPeer);
        } else {
            this.peerMap[peer.getPeer()] = peer.getPeer();
            const p = peer.getPeer();
            return this.createState(p);
        }
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
                logger.info(`Start of node method ${func.name}`);
                const response = await func(request, this.getState(call));
                logger.info(`End of node method ${func.name}`);
                callback(null, response);
            } catch (e) {
                logger.info(`Error of node method  ${func.name}`);
                callback(errorResponse(e), null);
            }
        };
    };

    private wrappingState = <T, K>(
        func: (state: PlaywrightState) => Promise<K>,
    ): ((call: ServerUnaryCall<T, K>, callback: sendUnaryData<K>) => Promise<void>) => {
        return async (call: ServerUnaryCall<T, K>, callback: sendUnaryData<K>) => {
            try {
                logger.info(`Start of node method ${func.name}`);
                const response = await func(this.getState(call));
                logger.info(`End of node method ${func.name}`);
                callback(null, response);
            } catch (e) {
                logger.info(`Error of node method ${func.name}`);
                callback(errorResponse(e), null);
            }
        };
    };

    private wrappingPage = <T, K>(
        func: (request: T, page: Page) => Promise<K>,
    ): ((call: ServerUnaryCall<T, K>, callback: sendUnaryData<K>) => Promise<void>) => {
        return async (call: ServerUnaryCall<T, K>, callback: sendUnaryData<K>) => {
            try {
                const request = call.request;
                if (request === null) throw Error('No request');
                logger.info(`Start of node method ${func.name}`);
                const response = await func(request, this.getActivePage(call));
                logger.info(`End of node method ${func.name}`);
                callback(null, response);
            } catch (e) {
                logger.info(`Error of node method ${func.name}`);
                callback(errorResponse(e), null);
            }
        };
    };

    private wrappingStatePage = <T, K>(
        func: (request: T, state: PlaywrightState, page: Page) => Promise<K>,
    ): ((call: ServerUnaryCall<T, K>, callback: sendUnaryData<K>) => Promise<void>) => {
        return async (call: ServerUnaryCall<T, K>, callback: sendUnaryData<K>) => {
            try {
                const request = call.request;
                if (request === null) throw Error('No request');
                logger.info(`Start of node method ${func.name}`);
                const response = await func(request, this.getState(call), this.getActivePage(call));
                logger.info(`End of node method ${func.name}`);
                callback(null, response);
            } catch (e) {
                logger.info(`Error of node method  ${func.name}`);
                callback(errorResponse(e), null);
            }
        };
    };

    initializeExtension = this.wrapping(playwrightState.initializeExtension);

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

    closeBrowser = this.wrappingState(playwrightState.closeBrowser);
    closeBrowserServer = this.wrapping(playwrightState.closeBrowserServer);
    closeAllBrowsers = this.wrappingState(playwrightState.closeAllBrowsers);
    closeContext = this.wrappingState(playwrightState.closeContext);
    closePage = this.wrapping(playwrightState.closePage);
    getBrowserCatalog = this.wrappingState(playwrightState.getBrowserCatalog);
    getConsoleLog = this.wrapping(playwrightState.getConsoleLog);
    getErrorMessages = this.wrapping(playwrightState.getErrorMessages);

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
            const response = await playwrightState.switchPage(request, this.getActiveBrowser(call));
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
            const response = await playwrightState.switchContext(request, this.getActiveBrowser(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async saveStorageState(
        call: ServerUnaryCall<Request.FilePath, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const response = await playwrightState.saveStorageState(request, this.getActiveBrowser(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    switchBrowser = this.wrapping(playwrightState.switchBrowser);
    newPage = this.wrapping(playwrightState.newPage);
    newContext = this.wrapping(playwrightState.newContext);
    newBrowser = this.wrapping(playwrightState.newBrowser);
    launchBrowserServer = this.wrapping(playwrightState.launchBrowserServer);
    newPersistentContext = this.wrapping(playwrightState.newPersistentContext);
    connectToBrowser = this.wrapping(playwrightState.connectToBrowser);
    goTo = this.wrappingPage(browserControl.goTo);
    pdf = this.wrapping(pdf.savePageAsPdf);
    emulateMedia = this.wrapping(pdf.emulateMedia);

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

    takeScreenshot = this.wrapping(browserControl.takeScreenshot);
    getBoundingBox = this.wrapping(getters.getBoundingBox);

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

    getElementCount = this.wrapping(getters.getElementCount);
    getSelectContent = this.wrapping(getters.getSelectContent);
    getDomProperty = this.wrapping(getters.getDomProperty);
    getText = this.wrapping(getters.getText);
    getBoolProperty = this.wrapping(getters.getBoolProperty);
    getElementAttribute = this.wrapping(getters.getElementAttribute);
    getElementStates = this.wrapping(getters.getElementStates);
    getStyle = this.wrapping(getters.getStyle);
    getTableCellIndex = this.wrapping(getters.getTableCellIndex);
    getTableRowIndex = this.wrapping(getters.getTableRowIndex);
    scrollToElement = this.wrapping(interaction.scrollToElement);

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

    selectOption = this.wrapping(interaction.selectOption);
    grantPermissions = this.wrapping(browserControl.grantPermissions);
    clearPermissions = this.wrapping(browserControl.clearPermissions);
    deselectOption = this.wrapping(interaction.deSelectOption);
    typeText = this.wrapping(interaction.typeText);
    fillText = this.wrapping(interaction.fillText);
    clearText = this.wrapping(interaction.clearText);
    press = this.wrapping(interaction.press);
    click = this.wrapping(interaction.click);
    addLocatorHandlerCustom = this.wrapping(locatorHandler.addLocatorHandlerCustom);
    removeLocatorHandler = this.wrapping(locatorHandler.removeLocatorHandler);
    tap = this.wrapping(interaction.tap);
    hover = this.wrapping(interaction.hover);
    focus = this.wrapping(interaction.focus);
    checkCheckbox = this.wrapping(interaction.checkCheckbox);
    uncheckCheckbox = this.wrapping(interaction.uncheckCheckbox);
    getElement = this.wrapping(evaluation.getElement);
    getElements = this.wrapping(evaluation.getElements);
    getByX = this.wrapping(evaluation.getByX);
    addStyleTag = this.wrappingPage(evaluation.addStyleTag);
    setTime = this.wrapping(clock.setTime);
    clockResume = this.wrapping(clock.clockResume);
    clockPauseAt = this.wrapping(clock.clockPauseAt);
    advanceClock = this.wrapping(clock.advanceClock);
    waitForElementsState = this.wrapping(evaluation.waitForElementState);
    waitForRequest = this.wrappingPage(network.waitForRequest);
    waitForResponse = this.wrappingPage(network.waitForResponse);
    waitForNavigation = this.wrappingPage(network.waitForNavigation);
    waitForPageLoadState = this.wrappingPage(network.WaitForPageLoadState);
    getDownloadState = this.wrapping(network.getDownloadState);
    cancelDownload = this.wrapping(network.cancelDownload);

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

    waitForDownload = this.wrappingStatePage(network.waitForDownload);

    evaluateJavascript = this.wrappingStatePage(evaluation.evaluateJavascript);

    recordSelector = this.wrapping(evaluation.recordSelector);

    async health(
        call: ServerUnaryCall<Request.Empty, Response.String>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        const response = new Response.String();
        response.setBody('OK');
        callback(null, response);
    }

    highlightElements = this.wrapping(evaluation.highlightElements);
    download = this.wrapping(evaluation.download);
    setViewportSize = this.wrappingPage(browserControl.setViewportSize);
    httpRequest = this.wrappingPage(network.httpRequest);

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

    async uploadFileBySelector(
        call: ServerReadableStream<Request.FileBySelector, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        let buffer = '';
        let lastRequest: Request.FileBySelector;
        call.on('data', async (request: Request.FileBySelector) => {
            try {
                logger.info(`Reading multiplepart uploadFileBySelector`);
                const newBuffer = request.getBuffer();
                buffer += newBuffer;
                lastRequest = request;
            } catch (e) {
                callback(errorResponse(e), null);
            }
        });
        call.on('error', (e) => {
            callback(errorResponse(e), null);
        });
        call.on('end', async () => {
            try {
                lastRequest.setBuffer(buffer);
                const result = await interaction.uploadFileBySelector(lastRequest, this.getState(call));
                callback(null, result);
            } catch (e) {
                callback(errorResponse(e), null);
            }
        });
    }

    uploadFile = this.wrappingPage(interaction.uploadFile);
    handleAlert = this.wrappingPage(interaction.handleAlert);
    waitForAlerts = this.wrappingPage(interaction.waitForAlerts);
    mouseMove = this.wrappingPage(interaction.mouseMove);
    mouseWheel = this.wrappingPage(interaction.mouseWheel);
    mouseButton = this.wrappingPage(interaction.mouseButton);
    keyboardKey = this.wrappingPage(interaction.keyboardKey);
    keyboardInput = this.wrappingPage(interaction.keyboardInput);

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

    async setPeerId(
        call: ServerUnaryCall<Request.Index, Response.Empty>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const oldPeer = this.peerMap[call.getPeer()];
            this.peerMap[call.getPeer()] = request.getIndex();
            callback(null, stringResponse(oldPeer, 'Successfully overrode peer id'));
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }
}
