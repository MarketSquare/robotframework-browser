import { IPlaywrightServer, PlaywrightService } from './generated/playwright_grpc_pb';
import { chromium, firefox, webkit, Browser, BrowserContext, Page } from 'playwright';
import { sendUnaryData, ServerUnaryCall, Server, ServerCredentials } from 'grpc';
import { Response, Request, SelectEntry } from './generated/playwright_pb';

// This is necessary for improved typescript inference
/*
 * If obj is not trueish call callback with new Error containing message
 */
function exists<T1, T2>(obj: T1, callback: sendUnaryData<T2>, message: string): asserts obj is NonNullable<T1> {
    if (!obj) {
        callback(new Error(message), null);
    }
}

// Can't have an async constructor, this is a workaround
async function createBrowserState(browserType: string, headless: boolean): Promise<BrowserState> {
    let browser;
    if (browserType === 'firefox') {
        browser = await firefox.launch({ headless: headless });
    } else if (browserType === 'chromium') {
        browser = await chromium.launch({ headless: headless });
    } else if (browserType === 'webkit') {
        browser = await webkit.launch({ headless: headless });
    } else {
        throw new Error('unsupported browser');
    }
    const context = await browser.newContext();
    context.setDefaultTimeout(parseFloat(process.env.TIMEOUT || '10000'));
    const page = await context.newPage();
    return new BrowserState(browser, context, page);
}

class BrowserState {
    constructor(browser: Browser, context: BrowserContext, page: Page) {
        this.browser = browser;
        this.context = context;
        this.page = page;
    }
    browser: Browser;
    context: BrowserContext;
    page: Page;
}

function emptyWithLog(text: string): Response.Empty {
    const response = new Response.Empty();
    response.setLog(text);
    return response;
}

class PlaywrightServer implements IPlaywrightServer {
    private browserState?: BrowserState;

    async closeBrowser(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, 'Tried to close browser but none was open');
        await this.browserState.browser.close();
        this.browserState = undefined;
        console.log('Closed browser');
        const response = emptyWithLog('Closed browser');
        callback(null, response);
    }

    async openBrowser(
        call: ServerUnaryCall<Request.openBrowser>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        const browserType = call.request.getBrowser();
        const url = call.request.getUrl();
        const headless = call.request.getHeadless();
        console.log('Open browser: ' + browserType);
        this.browserState = await createBrowserState(browserType, headless);
        if (url) {
            await this.browserState.page.goto(url);
            callback(null, emptyWithLog(`Succesfully opened browser ${browserType} to ${url}.`));
        } else {
            callback(null, emptyWithLog(`Succesfully opened browser ${browserType}.`));
        }
    }

    async goTo(call: ServerUnaryCall<Request.goTo>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, 'Tried to open URl but had no browser open');
        const url = call.request.getUrl();
        console.log('Go to URL: ' + url);

        await this.browserState.page.goto(url).catch((e) => callback(e, null));
        const response = emptyWithLog('Succesfully opened URL');
        callback(null, response);
    }

    async goBack(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, 'Tried to go back in history but no browser was open');
        await this.browserState.page.goBack().catch((e) => callback(e, null));
        console.log('Go Back');
        const response = emptyWithLog('Did Go Back');
        callback(null, response);
    }

    async goForward(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, 'Tried to go forward in history but no browser was open');
        await this.browserState.page.goForward().catch((e) => callback(e, null));
        console.log('Go BForward');
        const response = emptyWithLog('Did Go Forward');
        callback(null, response);
    }

    async getTitle(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        exists(this.browserState, callback, 'Tried to get title, no open browser');
        console.log('Getting title');
        const title = await this.browserState.page.title().catch((e) => {
            callback(e, null);
            throw e;
        });
        const response = new Response.String();
        response.setBody(title);
        callback(null, response);
    }

    async getUrl(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        exists(this.browserState, callback, 'Tried to get page URL, no open browser');
        console.log('Getting URL');
        const url = this.browserState.page.url();
        const response = new Response.String();
        response.setBody(url);
        callback(null, response);
    }

    async getTextContent(
        call: ServerUnaryCall<Request.selector>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        exists(this.browserState, callback, 'Tried to find text on page, no open browser');
        const selector = call.request.getSelector();
        const content = await this.browserState.page.textContent(selector).catch((e) => {
            callback(e, null);
            throw e;
        });
        const response = new Response.String();
        response.setBody(content?.toString() || '');
        callback(null, response);
    }

    // TODO: work some of getDomProperty and getBoolProperty's duplicate code into a root function
    async getSelectContent(
        call: ServerUnaryCall<Request.selector>,
        callback: sendUnaryData<Response.Select>,
    ): Promise<void> {
        exists(this.browserState, callback, 'Tried to get Select element contents, no open browser');
        const selector = call.request.getSelector();
        const page = this.browserState.page;

        type Value = [string, string, boolean];
        const content: Value[] = await page.$$eval(selector + ' option', (elements) =>
            (elements as HTMLOptionElement[]).map((elem) => [elem.label, elem.value, elem.selected]),
        );

        const response = new Response.Select();
        content.forEach((option) => {
            const [label, value, selected] = [option[0], option[1], option[2]];
            const entry = new SelectEntry();
            entry.setLabel(label);
            entry.setValue(value);
            entry.setSelected(selected);
            response.addEntry(entry);
        });
        callback(null, response);
    }

    async selectOption(
        call: ServerUnaryCall<Request.selectOption>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        exists(this.browserState, callback, 'Tried to select ``select`` element option, no open browser');
        const selector = call.request.getSelector();
        const matcher = call.request.getMatcherjson();
        console.log(`Selecting from element ${selector} options ${matcher}`);
        const result = await this.browserState.page.selectOption(selector, JSON.parse(matcher)).catch((e) => {
            callback(e, null);
            throw e;
        });

        if (result.length == 0 && !matcher.includes('5b67de39-5e23-42cc-aadb-1dc053c41a48')) {
            console.log("Couldn't select any options");
            const error = new Error(`No options matched ${matcher}`);
            callback(error, null);
        }
        const response = emptyWithLog(`Selected options ${result} in element ${selector}`);
        callback(null, response);
    }

    async _getDomProperty<T>(call: ServerUnaryCall<Request.getDomProperty>, callback: sendUnaryData<T>) {
        exists(this.browserState, callback, 'Tried to get DOM property, no open browser');
        const selector = call.request.getSelector();
        const property = call.request.getProperty();

        const element = await this.browserState.page.$(selector).catch((e) => {
            callback(e, null);
            throw e;
        });
        exists(element, callback, "Couldn't find element: " + selector);

        const result = await element.getProperty(property).catch((e) => {
            callback(e, null);
            throw e;
        });
        const content = await result.jsonValue();
        console.log(`Retrieved dom property for element ${selector} containing ${content}`);
        return content;
    }

    async getDomProperty(
        call: ServerUnaryCall<Request.getDomProperty>,
        callback: sendUnaryData<Response.String>,
    ): Promise<void> {
        const content = await this._getDomProperty(call, callback).catch((e) => callback(e, null));
        const response = new Response.String();
        response.setBody(content);
        callback(null, response);
    }

    async getBoolProperty(
        call: ServerUnaryCall<Request.getDomProperty>,
        callback: sendUnaryData<Response.Bool>,
    ): Promise<void> {
        const content = await this._getDomProperty(call, callback).catch((e) => callback(e, null));
        const response = new Response.Bool();
        response.setBody(content || false);
        callback(null, response);
    }

    async inputText(call: ServerUnaryCall<Request.inputText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, 'Tried to input text, no open browser');
        const inputText = call.request.getInput();
        const selector = call.request.getSelector();
        const type = call.request.getType();
        if (type) {
            await this.browserState.page.type(selector, inputText).catch((e) => callback(e, null));
        } else {
            await this.browserState.page.fill(selector, inputText).catch((e) => callback(e, null));
        }

        const response = emptyWithLog('Input text: ' + inputText);
        callback(null, response);
    }

    async typeText(call: ServerUnaryCall<Request.typeText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, 'Tried to type text, no open browser');
        const selector = call.request.getSelector();
        const text = call.request.getText();
        const delay = call.request.getDelay();
        const clear = call.request.getClear();
        if (clear) {
            await this.browserState.page.fill(selector, '').catch((e) => callback(e, null));
        }
        await this.browserState.page.type(selector, text, { delay: delay }).catch((e) => callback(e, null));

        const response = emptyWithLog('Type text: ' + text);
        callback(null, response);
    }

    async fillText(call: ServerUnaryCall<Request.fillText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, 'Tried to fill text, no open browser');
        const selector = call.request.getSelector();
        const text = call.request.getText();
        await this.browserState.page.fill(selector, text).catch((e) => callback(e, null));

        const response = emptyWithLog('Fill text: ' + text);
        callback(null, response);
    }

    async clearText(call: ServerUnaryCall<Request.clearText>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, 'Tried to clear text field, no open browser');
        const selector = call.request.getSelector();
        await this.browserState.page.fill(selector, '').catch((e) => callback(e, null));

        const response = emptyWithLog('Text field cleared.');
        callback(null, response);
    }

    async press(call: ServerUnaryCall<Request.press>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, 'Tried to input text, no open browser');
        const selector = call.request.getSelector();
        const keyList = call.request.getKeyList();
        for (const i of keyList) {
            await this.browserState.page.press(selector, i).catch((e) => callback(e, null));
        }
        const response = emptyWithLog('Pressed keys: ' + keyList);
        callback(null, response);
    }

    async click(call: ServerUnaryCall<Request.selector>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, 'Tried to click element, no open browser');

        const selector = call.request.getSelector();
        await this.browserState.page.click(selector).catch((e) => callback(e, null));
        const response = emptyWithLog('Clicked element: ' + selector);
        callback(null, response);
    }

    async clickWithOptions(
        call: ServerUnaryCall<Request.selectorOptions>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        exists(this.browserState, callback, 'Tried to click element, no open browser');

        const selector = call.request.getSelector();
        const options = call.request.getOptions();
        await this.browserState.page.click(selector, JSON.parse(options)).catch((e) => callback(e, null));
        const response = emptyWithLog('Clicked element: ' + selector + ' \nWith options: ' + options);
        callback(null, response);
    }

    async focus(call: ServerUnaryCall<Request.selector>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, 'Tried to focus element, no open browser');

        const selector = call.request.getSelector();
        await this.browserState.page.focus(selector).catch((e) => callback(e, null));
        const response = emptyWithLog('Focused element: ' + selector);
        callback(null, response);
    }

    async checkCheckbox(
        call: ServerUnaryCall<Request.selector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        exists(this.browserState, callback, 'Tried to check checkbox, no open browser');
        const selector = call.request.getSelector();
        await this.browserState.page.check(selector).catch((e) => callback(e, null));
        const response = emptyWithLog('Checked checkbox: ' + selector);
        callback(null, response);
    }
    async uncheckCheckbox(
        call: ServerUnaryCall<Request.selector>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        exists(this.browserState, callback, 'Tried to uncheck checkbox, no open browser');
        const selector = call.request.getSelector();
        await this.browserState.page.uncheck(selector).catch((e) => callback(e, null));
        const response = emptyWithLog('Unhecked checkbox: ' + selector);
        callback(null, response);
    }

    async setTimeout(call: ServerUnaryCall<Request.timeout>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, 'Tried to set timeout, no open browser');
        const timeout = call.request.getTimeout();
        this.browserState.context.setDefaultTimeout(timeout);
        const response = emptyWithLog('Set timeout to: ' + timeout);
        callback(null, response);
    }

    async health(call: ServerUnaryCall<Request.Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        const response = new Response.String();
        response.setBody('OK');
        callback(null, response);
    }

    async screenshot(
        call: ServerUnaryCall<Request.screenshot>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        exists(this.browserState, callback, 'Tried to take screenshot, no open browser');
        // Add the file extension here because the image type is defined by playwrights defaults
        const path = call.request.getPath() + '.png';
        console.log(`Taking a screenshot of current page to ${path}`);
        await this.browserState.page.screenshot({ path: path }).catch((e) => callback(e, null));

        const response = emptyWithLog('Succesfully took screenshot');
        callback(null, response);
    }

    async addStyleTag(
        call: ServerUnaryCall<Request.addStyleTag>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        exists(this.browserState, callback, 'Tried to add style tag, no open browser');
        const content = call.request.getContent();
        await this.browserState.page.addStyleTag({ content: content });
        const response = emptyWithLog('added Style: ' + content);
        callback(null, response);
    }

    async waitForElementsState(
        call: ServerUnaryCall<Request.selectorOptions>,
        callback: sendUnaryData<Response.Empty>,
    ): Promise<void> {
        exists(this.browserState, callback, 'Tried to wait for an element, no open browser');
        console.log('Waiting for element state');
        const selector = call.request.getSelector();
        const options = JSON.parse(call.request.getOptions());
        await this.browserState.page.waitForSelector(selector, options).catch((e) => {
            callback(e, null);
            throw e;
        });
        const response = emptyWithLog('Wait for Element with selector: ' + selector);
        callback(null, response);
    }

    async executeJavascriptOnPage(
        call: ServerUnaryCall<Request.jsExecution>,
        callback: sendUnaryData<Response.jsResult>
    ): Promise<void> {
        console.log("JEE JS");
        const response = new Response.jsResult();
        response.setLog("DUMMY");
        response.setResult("Hello dummy");
        callback(null, response);
    }
}

const server = new Server();
server.addService<IPlaywrightServer>(PlaywrightService, new PlaywrightServer());
const port = process.env.PORT || '0';
server.bind(`localhost:${port}`, ServerCredentials.createInsecure());
console.log(`Listening on ${port}`);
server.start();
