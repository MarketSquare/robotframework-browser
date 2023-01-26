# Introduction

There are three main ways to create new functionality for Browser library: Plugin API,
[extending the library with a JavaScript module](https://marketsquare.github.io/robotframework-browser/Browser.html#Extending%20Browser%20library%20with%20a%20JavaScript%20module)
and building [new libraries](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#extending-existing-test-libraries)
on top the Browser library. Each way offers their own unique pros and cons.
Plugin API and extending Browser library allow similar access to the Python public API library.

# Initialisation order

When an instance is created from the Browser library, for example when Browser library is imported in the test data, there is an order
of the initialisation. At first all classes defining Browser library keywords are discovered. As a second event,
keywords from the JavaScript module are discovered. As a third and last event, keywords from plugins are discovered.

# Plugins

Browser library offers plugins as a way to modify and add library keywords, while also modifying some of the internal functionality of Browser library
without creating a new library or hacking the source code. See 
[plugin example](https://github.com/MarketSquare/robotframework-browser/blob/main/docs/plugins/example) 
on how plugins can be implemented.

## Importing plugins

Importing plugins is similar to importing Robot Framework libraries. It is possible to import plugin using a
physical path or with exact name of the plugin in the same way libraries are imported in Robot Framework. Browser library
plugins are found from the same module search path as Robot Framework searches libraries. It is only possible
to import plugins written in Python, other programming languages or Robot Framework test data is not supported.
Like with Robot Framework library imports, plugin names are case sensitive and spaces are not supported in the
plugin name. It is possible to import multiple plugins at the same time by separating the plugins with a comma.
It is possible to have space before and after the comma. Plugins are imported in the order they are defined in the
plugins argument. If two or more plugins declare the same keyword or modify the same method/attribute in the library,
the last plugin to perform the changes will overwrite the changes made by other plugins. Example of plugin imports:

```robotframework
Library     Browser     plugins=${CURDIR}/MyPlugin.py                       # Imports plugin with physical path
```


```robotframework
Library     Browser     plugins=plugins.MyPlugin, plugins.MyOtherPlugin     # Imports two plugins with name
```

## Plugin arguments

When Browser library creates instances from the plugin classes, it will by default initiate the class with a single
argument, called `library`. `library` is the instance of the Browser library and it provides access to the library
Public API.

It is also possible to provide optional arguments to the plugins. Arguments must be separated with a semicolon from
the plugin. Browser library will not convert arguments to any specific type and everything is by default unicode.
The plugin is responsible for converting the arguments to proper types. Example of importing plugin with arguments:

```robotframework
Library     Browser     plugins=plugins.Plugin;ArgOne;ArgTwo     # Import two plugins with two arguments: ArgOne and ArgTwo
```

It is also possible to provide a variable number of arguments and keywords arguments. Named arguments must be defined
first, variable number of arguments second, and keywords arguments last. All arguments must be separated with a
semicolon. For example, if plugin `__init__` is defined like this:

```python
from Browser.base.librarycomponent import LibraryComponent


class Plugin(LibraryComponent):

    def __init__(self, library, arg, *varargs, **kwargs):
        # Code to implement the plugin.
```

Then it is possible to plugin with these arguments:

```robotframework
Library     Browser     plugins=plugins.Plugin;argument1;varg1;varg2;kw1=kwarg1;kw2=kwarg2
```

Then argument1 is given the arg in the `__init__`. The `varg1` and `varg2` variable number arguments are given to
the `*varargs` argument in the `__init__`. Finally, the `kw1=kwarg1` and `kw2=kwarg2` keyword arguments are given to
the `**kwargs` in the `__init__`. In Python, there can be zero or more variable number and keyword arguments.

## Plugin API

Generally speaking, plugins are not any different from the classes that are used to implement keywords in the Browser
library. For instance, the
[Cookie](https://github.com/MarketSquare/robotframework-browser/blob/main/Browser/keywords/cookie.py) class inherits
the
[LibraryComponent](https://github.com/MarketSquare/robotframework-browser/blob/main/Browser/base/librarycomponent.py)
and uses the `@keyword` decorator to mark which methods are exposed as keywords.

Plugins must be implemented as Python classes and plugins must inherit the Browser library LibraryComponent class.
Plugin `__init__` must support at least one positional argument `library` which will grant access to the Browser object.
Also, optional arguments are supported. See Plugin arguments for more details how to provide optional arguments to plugins.

Browser library uses Robot Framework's
[dynamic library API](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api),
with the help of the [Python Library Core](https://github.com/robotframework/PythonLibCore). The main difference when
compared to libraries using dynamic library API, is that plugins are not responsible for implementing the dynamic
library API. Browser library is handling the dynamic library API requirements towards Robot Framework. For plugins,
this means that methods that implement keywords must be decorated with the `@keyword` decorator. The `@keyword`
decorator can be imported from Robot Framework and used in the following way:

```python
from robot.api.deco import keyword
from Browser.base.librarycomponent import LibraryComponent

class Plugin(LibraryComponent):

    @keyword
    def plugin_keyword(self):
        # More code here to implement the keyword
```


### Implementing keywords

In the next example you see a more complex example.
It implements the init function to initialize a custom javascript module "*jsplugin.js*"
that contains a function `mouseWheel`.
This javascript module has the same requirements as the js keyword extensions of Browser library.
These keywords are however not exposed to Robot Framework but can be called from a Python function
using the `self.call_js_keyword` function.
See Python keyword `mouse_wheel`.

The second Python keyword `get_location_object` uses the Browser keyword `Evaluate Javascript`
to get the location object from the browser. As long as no access to Playwright is needed,
`Evaluate Javascript` may be sufficient.
To call a Browser library keyword from a plugin, use `self.library.<keyword name to call>` syntax.
You can call any Browser keyword that way.


Python plugin example:
```python
import json
from pathlib import Path
from robot.api import logger
from robot.api.deco import keyword
from robot.utils import DotDict
from Browser import Browser
from Browser.base.librarycomponent import LibraryComponent


class ExamplePlugin(LibraryComponent):
    def __init__(self, library: Browser):
        super().__init__(library)
        self.initialize_js_extension(Path(__file__).parent / "jsplugin.js")

    @keyword
    def mouse_wheel(self, x: int, y: int):
        """This keyword calls a custom javascript keyword from the file jsplugin.js."""
        return self.call_js_keyword("mouseWheel", x=x, y=y, logger=None, page=None)

    @keyword
    def get_location_object(self) -> dict:
        """Returns the location object of the current page.

        This keyword calls the python keyword `Evaluate Javascript` to get the location object."""
        location_dict = self.library.evaluate_javascript(None, f"window.location")
        logger.info(f"Location object:\n {json.dumps(location_dict, indent=2)}")
        return DotDict(location_dict)
```

Javascript plugin example "*jsplugin.js*":
```javascript
async function mouseWheel(x, y, logger, page) {
    logger(`Mouse wheel at ${x}, ${y}`);
    await page.mouse.wheel(x, y);
    logger("Returning a funny string");
    return await page.evaluate("document.scrollingElement.scrollTop");
}

exports.__esModule = true;
exports.mouseWheel = mouseWheel;
```

# Handling plugin failures

Browser library does not suppress exceptions raised during plugin importation or during keyword discovery from the plugins.
In this case the whole library import will fail and keywords can not be used from that import.

By default exceptions raised by Browser library keywords will trigger the run on failure functionality, and this also
applies to keywords created or modified by the plugins. However, it must be noted that plugins can alter the library run on
failure functionality. Refer to the plugin documentation for further details.

# Generating keyword documentation

To separate keywords which are added or modified by plugins, Browser will add a `plugin` keyword tag to all keywords
added or modified by plugins. Because of this, when Browser library keyword documentation is generated by
[libdoc](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#library-documentation-tool-libdoc)
it is easy to separate keywords which are added or modified by plugins. Browser keyword documentation that includes plugins can be generated with the  following command:

`libdoc Browser::plugins=/path/to/Plugin.py Browser.html`
