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

// The `css` generator of Record Selector, evaluated in the frame of the picked
// element. Bundled with @medv/finder into static/css-selector.js by
// node/build.wrapper.js; evaluated through the protocol, so a page's Content
// Security Policy does not apply.

import { finder } from '@medv/finder';

// A CSS selector unique within the element's document, with ` >> ` between the
// selectors of the shadow hosts it sits in: CSS in Playwright pierces open shadow
// roots, and each part is resolved inside the previous one's match.
function cssSelector(element: Element): string {
    const root = element.getRootNode();
    if (root instanceof ShadowRoot) {
        const inner = finder(element, { root: root as unknown as Element });
        return `${cssSelector(root.host)} >> ${inner}`;
    }
    return finder(element);
}

(window as unknown as { __rfbCssSelector: (element: Element) => string }).__rfbCssSelector = cssSelector;
