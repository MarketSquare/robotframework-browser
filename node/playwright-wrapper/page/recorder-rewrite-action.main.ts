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

// Runs the page half, recorder-rewrite-action.ts, in the page; importing that
// module runs nothing. Bundled into static/recorder-rewrite-action.js by
// node/build.wrapper.js, it runs in the main world of every frame, as an init
// script and in the frames already open.

import { defineRewritePickedSelector, patchReportAction } from './recorder-rewrite-action';

patchReportAction(window as unknown as Record<string, unknown>);
defineRewritePickedSelector(window as unknown as Record<string, unknown>);
