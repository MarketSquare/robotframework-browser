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

import { sendUnaryData, ServerReadableStream, ServerUnaryCall, ServerWritableStream } from '@grpc/grpc-js';
import { ServerSurfaceCall } from '@grpc/grpc-js/build/src/server-call';
import { Page } from 'playwright';

import { logger } from './browser_logger';
import * as browserControl from './browser-control';
import * as clock from './clock';
import * as cookie from './cookie';
import * as deviceDescriptors from './device-descriptors';
import * as evaluation from './evaluation';
import * as pb from './generated/playwright';
import * as getters from './getters';
import * as interaction from './interaction';
import { class_async_logger } from './keyword-decorators';
import * as locatorHandler from './locator-handler';
import * as network from './network';
import * as pdf from './pdf';
import * as playwrightState from './playwright-state';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog, errorResponse, stringResponse } from './response-util';

@class_async_logger
export class PlaywrightServer {
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

    async callExtensionKeyword(call: ServerWritableStream<pb.Request_KeywordCall, pb.Response_Json>): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const results = await playwrightState.extensionKeywordCall(request, call, this.getState(call));
            for (const result of results) {
                call.write(result);
            }
        } catch (e) {
            call.emit('error', errorResponse(e));
        }
        call.end();
    }

    closeBrowser = this.wrappingState(playwrightState.closeBrowser);
    closeBrowserServer = this.wrapping(playwrightState.closeBrowserServer);
    closeAllBrowsers = this.wrappingState(playwrightState.closeAllBrowsers);
    closeContext = this.wrapping(playwrightState.closeContext);
    closePage = this.wrapping(playwrightState.closePage);
    openTraceGroup = this.wrapping(playwrightState.openTraceGroup);
    closeTraceGroup = this.wrappingState(playwrightState.closeTraceGroup);
    getBrowserCatalog = this.wrapping(playwrightState.getBrowserCatalog);
    getConsoleLog = this.wrapping(playwrightState.getConsoleLog);
    getErrorMessages = this.wrapping(playwrightState.getErrorMessages);

    async getCookies(
        call: ServerUnaryCall<pb.Request_Empty, pb.Response_Json>,
        callback: sendUnaryData<pb.Response_Json>,
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
        call: ServerUnaryCall<pb.Request_Json, pb.Response_Empty>,
        callback: sendUnaryData<pb.Response_Empty>,
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
        call: ServerUnaryCall<pb.Request_Empty, pb.Response_Empty>,
        callback: sendUnaryData<pb.Response_Empty>,
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
        call: ServerUnaryCall<pb.Request_IdWithTimeout, pb.Response_String>,
        callback: sendUnaryData<pb.Response_String>,
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
        call: ServerUnaryCall<pb.Request_Index, pb.Response_String>,
        callback: sendUnaryData<pb.Response_String>,
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
        call: ServerUnaryCall<pb.Request_FilePath, pb.Response_Empty>,
        callback: sendUnaryData<pb.Response_Empty>,
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
    startCoverage = this.wrapping(playwrightState.startCoverage);
    stopCoverage = this.wrapping(playwrightState.stopCoverage);
    mergeCoverage = this.wrapping(playwrightState.mergeCoverage);
    launchBrowserServer = this.wrapping(playwrightState.launchBrowserServer);
    newPersistentContext = this.wrapping(playwrightState.newPersistentContext);
    connectToBrowser = this.wrapping(playwrightState.connectToBrowser);
    goTo = this.wrappingPage(browserControl.goTo);
    pdf = this.wrapping(pdf.savePageAsPdf);
    emulateMedia = this.wrapping(pdf.emulateMedia);

    async goBack(
        call: ServerUnaryCall<pb.Request_Empty, pb.Response_Empty>,
        callback: sendUnaryData<pb.Response_Empty>,
    ): Promise<void> {
        try {
            await this.getActivePage(call).goBack();
            callback(null, emptyWithLog('Did Go Back'));
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async goForward(
        call: ServerUnaryCall<pb.Request_Empty, pb.Response_Empty>,
        callback: sendUnaryData<pb.Response_Empty>,
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
    ariaSnapShot = this.wrappingStatePage(getters.getAriaSnapshot);

    async getPageSource(call: ServerWritableStream<pb.Request_Empty, pb.Response_Json>): Promise<void> {
        try {
            const results = await getters.getPageSource(this.getActivePage(call));
            for (const result of results) {
                call.write(result);
            }
        } catch (e) {
            call.emit('error', errorResponse(e));
        }
        call.end();
    }

    async setTimeout(
        call: ServerUnaryCall<pb.Request_Timeout, pb.Response_Empty>,
        callback: sendUnaryData<pb.Response_Empty>,
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
        call: ServerUnaryCall<pb.Request_Empty, pb.Response_String>,
        callback: sendUnaryData<pb.Response_String>,
    ): Promise<void> {
        try {
            const response = await getters.getTitle(this.getActivePage(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async getUrl(
        call: ServerUnaryCall<pb.Request_Empty, pb.Response_String>,
        callback: sendUnaryData<pb.Response_String>,
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
        call: ServerUnaryCall<pb.Request_Empty, pb.Response_Json>,
        callback: sendUnaryData<pb.Response_Json>,
    ): Promise<void> {
        try {
            const response = await getters.getViewportSize(this.getActivePage(call));
            callback(null, response);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    selectOption = this.wrapping(interaction.selectOption);
    executePlaywright = this.wrapping(browserControl.executePlaywright);
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
    async waitForResponse(call: ServerWritableStream<pb.Request_HttpCapture, pb.Response_Json>): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const results = await network.waitForResponse(request, this.getActivePage(call));
            for (const result of results) {
                logger.info(`Sending response ${result.log}`);
                call.write(result);
            }
        } catch (e) {
            call.emit('error', errorResponse(e));
        }
        call.end();
    }

    waitForNavigation = this.wrappingPage(network.waitForNavigation);
    waitForPageLoadState = this.wrappingPage(network.WaitForPageLoadState);
    getDownloadState = this.wrapping(network.getDownloadState);
    cancelDownload = this.wrapping(network.cancelDownload);

    async waitForFunction(
        call: ServerUnaryCall<pb.Request_WaitForFunctionOptions, pb.Response_Json>,
        callback: sendUnaryData<pb.Response_Json>,
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
        call: ServerUnaryCall<pb.Request_Empty, pb.Response_String>,
        callback: sendUnaryData<pb.Response_String>,
    ): Promise<void> {
        callback(null, { body: 'OK', log: '' });
    }

    highlightElements = this.wrapping(evaluation.highlightElements);
    download = this.wrapping(evaluation.download);
    setViewportSize = this.wrappingPage(browserControl.setViewportSize);
    httpRequest = this.wrappingPage(network.httpRequest);

    async getDevice(
        call: ServerUnaryCall<pb.Request_Device, pb.Response_Json>,
        callback: sendUnaryData<pb.Response_Json>,
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
        call: ServerUnaryCall<pb.Request_Empty, pb.Response_Json>,
        callback: sendUnaryData<pb.Response_Json>,
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
        call: ServerReadableStream<pb.Request_FileBySelector, pb.Response_Empty>,
        callback: sendUnaryData<pb.Response_Empty>,
    ): Promise<void> {
        let buffer = '';
        let lastRequest: pb.Request_FileBySelector | undefined;
        call.on('data', (request: pb.Request_FileBySelector) => {
            void (async () => {
                try {
                    logger.info(`Reading multiplepart uploadFileBySelector`);
                    const newBuffer = request.buffer;
                    buffer += newBuffer;
                    lastRequest = request;
                } catch (e) {
                    callback(errorResponse(e), null);
                }
            })();
        });
        call.on('error', (e) => {
            callback(errorResponse(e), null);
        });
        call.on('end', () => {
            void (async () => {
                try {
                    if (!lastRequest) {
                        callback(errorResponse(new Error('No data received for uploadFileBySelector')), null);
                        return;
                    }
                    const finalRequest = { ...lastRequest, buffer };
                    const result = await interaction.uploadFileBySelector(finalRequest, this.getState(call));
                    callback(null, result);
                } catch (e) {
                    callback(errorResponse(e), null);
                }
            })();
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
        call: ServerUnaryCall<pb.Request_Bool, pb.Response_Empty>,
        callback: sendUnaryData<pb.Response_Empty>,
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
        call: ServerUnaryCall<pb.Request_Json, pb.Response_Empty>,
        callback: sendUnaryData<pb.Response_Empty>,
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
        call: ServerUnaryCall<pb.Request_Json, pb.Response_Empty>,
        callback: sendUnaryData<pb.Response_Empty>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const body = request.body;
            const result = await browserControl.reload(this.getActivePage(call), body);
            callback(null, result);
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async setPeerId(
        call: ServerUnaryCall<pb.Request_Index, pb.Response_String>,
        callback: sendUnaryData<pb.Response_String>,
    ): Promise<void> {
        try {
            const request = call.request;
            if (request === null) throw Error('No request');
            const oldPeer = this.peerMap[call.getPeer()];
            this.peerMap[call.getPeer()] = request.index;
            callback(null, stringResponse(oldPeer, 'Successfully overrode peer id'));
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }
}
