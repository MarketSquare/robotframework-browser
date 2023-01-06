# Introduction

Browser library offers three main ways to creating new functionality for Browser library: Plugin API,
[extending library with a JavaScript module](https://marketsquare.github.io/robotframework-browser/Browser.html#Extending%20Browser%20library%20with%20a%20JavaScript%20module)
and building [new libraries](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#extending-existing-test-libraries)
on top the Browser library. Each way offers their own unique pros and cons.
Plugin API and extending Browser library allows similar access to the library Python public API.

# Initialisation order

When instance is created from the Browser library, example when library is imported in the test data, there is an order
in the initialisation. At first all classes defining Browser library keywords are discovered. As a second event,
keywords from JavaScript module are discovered. As a third and last event, keywords from plugins are discovered.

# Plugins

Browser library offers plugins as a way to modify, add library keywords and modify some of the internal functionality
without creating new library or hacking the source code. See 
[plugin example](https://github.com/MarketSquare/robotframework-browser/blob/main/docs/plugins/example) 
how plugins can be implemented.

## Importing plugins

Importing plugins is similar when importing Robot Framework libraries. It is possible import plugin with using
physical path or with plugin name exactly in same way as importing libraries in Robot Framework. Browser library
plugins are searched from the same module search path as Robot Framework searches libraries. It is only possible
to import plugins written in Python, other programming languages or Robot Framework test data is not supported.
Like with Robot Framework library imports, plugin names are case sensitive and spaces are not supported in the
plugin name. It is possible to import multiple plugins at the same time by separating plugins with comma.
It is possible to have space before and after the comma. Plugins are imported in the order they defined in the
plugins argument. If two or more plugins declare the same keyword or modify the same method/attribute in the library,
the last plugin to perform the changes will overwrite the changes made by other plugins. Example of plugin imports:

```
| Library | Browser | plugins=${CURDIR}/MyPlugin.py                   | # Imports plugin with physical path |
| Library | Browser | plugins=plugins.MyPlugin, plugins.MyOtherPlugin | # Imports two plugins with name     |
```

## Plugin arguments

When Browser library creates instances from the plugin classes, it will by default initiate the class with a single
argument, called `library`. `library` is the instance of the Browser library and it provides access to the library
Public API.

It is also possible to provide optional arguments to the plugins. Arguments must be separated with a semicolon from
the plugin. Browser library will not convert arguments to any specific type and everything is by default unicode.
Plugin is responsible for converting the argument to proper types. Example of importing plugin with arguments:

```
| Library | Browser | plugins=plugins.Plugin;ArgOne;ArgTwo | # Import two plugins with two arguments: ArgOne and ArgTwo |
```

It is also possible to provide variable number of arguments and keywords arguments. Named arguments must be defined
first, variable number of arguments as second and keywords arguments as last. All arguments must be separated with
semicolon. Example if plugin `__init__` is defined like this:

```
class Plugin(LibraryComponent):

    def __init__(self, ctx, arg, *varargs, **kwargs):
        # Code to implement the plugin.
```

Then, for example, it is possible to plugin with these arguments:

```
| Library | Browser | plugins=plugins.Plugin;argument1;varg1;varg2;kw1=kwarg1;kw2=kwarg2 |
```

Then the argument1 is given the arg in the `__init__`. The `varg1` and `varg2` variable number arguments are given to
the `*varargs` argument in the `__init__`. Finally, the `kw1=kwarg1` and `kw2=kwarg2` keyword arguments are given to
the `**kwargs` in the `__init__`. As in Python, there can be zero or more variable number and keyword arguments.

## Plugin API

Generally speaking, plugins are not any different from the classes that are used to implement keyword in the Browser
library. Example like with
[Cookie](https://github.com/MarketSquare/robotframework-browser/blob/main/Browser/keywords/cookie.py) class inherits
the
[LibraryComponent](https://github.com/MarketSquare/robotframework-browser/blob/main/Browser/base/librarycomponent.py)
and uses `@keyword` decorator to mark which methods are exposed as keywords.

Plugins must be implemented as Python classes and plugins must inherit the Browser library LibraryComponent class.
Plugin `__init__` must support at least one argument: `library`. Also optional arguments are supported,
see Plugin arguments for more details how to provide optional arguments to plugins.

Browser library uses Robot Framework
[dynamic library API](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api),
with help of the [Python Library Core](https://github.com/robotframework/PythonLibCore). The main difference, when
compared to libraries using dynamic library API, is that plugins are not responsible for implementing the dynamic
library API. Browser library is handling the dynamic library API requirements towards Robot Framework. For plugins
this means that methods that implements keywords, must be decorated with `@keyword` decorator. The `@keyword`
decorator can be imported from Robot Framework and used in the following way:

```
from robot.api.deco import keyword

class Plugin(LibraryComponent):

    @keyword
    def plugin_keyword(self):
        with self.playwright.grpc_channel() as stub:  
            # More code here to implement the keyword
```

# Handling plugins failures

Browser library does not suppress exception raised during plugin import or during keywords discovery from the plugins.
In this case the whole library import will fail and keywords can not be used from that import.

By default when exceptions raised by Browser library keywords will trigger the run on failure functionality, this also
applies keywords created or modified by the plugins. But it must be noted that plugins can alter the library run on
failure functionality and refer to the plugin documentation for further details.

# Generating keyword documentation

To separate keywords which are added or modified by plugins, Browser will add `plugin` keyword tag to all keywords
added or modified from plugins. When Browser library keyword documentation, with plugins, is generated by
[libdoc](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#library-documentation-tool-libdoc)
it is easy to separate keywords which are added or modified by plugins. Keyword documentation can be example generated
by following command:

`python -m robot.libdoc Browser::plugins=/path/to/Plugin.py ./Browser.html`
