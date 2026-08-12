# Browser Library

The keyword library itself. This context is about **how a keyword call reaches a keyword
body** — there are two routes into the same keyword, and they behave differently on purpose.

## Language

**Robot Framework path**:
A keyword call arriving through `run_keyword`, with arguments already converted by Robot
Framework before the library sees them.
_Avoid_: RF path, dynamic API path

**Python path**:
A keyword call arriving by attribute access on the library instance, from a plain Python
script with no Robot Framework run.
_Avoid_: direct call, native call

**Keyword table**:
The mapping the **Robot Framework path** reads (`self.keywords`), keyed by Robot name.
_Avoid_: keyword dict, keyword registry

**Attribute table**:
The mapping the **Python path** reads (`self.attributes`), keyed by both the method name and
the Robot name, so one keyword may appear twice.
_Avoid_: attribute dict

**Argument conversion**:
Turning a plain value into the keyword's declared type using Robot Framework's own
converters — `"middle"` into `MouseButton.middle`, `"1.5s"` into a `timedelta`.
_Avoid_: coercion, casting, parsing

## Relationships

- Both tables hold the *same* keyword methods, stored twice by PythonLibCore. They are
  independent: changing one does not change the other.
- **Argument conversion** happens before the **Robot Framework path** reaches the keyword
  table, and inside the **attribute table** for the **Python path**.
- Trace groups and failure screenshots exist only on the **Robot Framework path**. This is a
  known, accepted difference, not a defect.

## Example dialogue

> **Dev:** "I added conversion for Python callers — won't that convert twice under Robot
> Framework?"
> **Domain expert:** "No. Robot Framework reads the keyword table and never touches the
> attribute table, so the Robot Framework path never enters the wrapper at all."
