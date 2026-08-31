# The Report is a typed document, not the JSON dict

A **Report** is built once, as frozen dataclasses, and the HTML page and the JSON document are
two **Renderings** over it. The obvious cheaper alternative was to make the JSON dict itself the
Report and render the page from that dict — it was already a designed artifact, and it would
have cost almost no new code.

It was rejected because the defect this replaced was **silent divergence**: two independent
assemblies over the same queries, each having quietly gained and lost fields the other did not
have, with nothing anywhere that could notice. A dict makes a Rendering ignoring a field
invisible; a type makes it a fact you can see and, where it is deliberate, read as a choice.
That is the whole reason for the indirection between `report.py` and `render_json.py`, and it is
not visible from the code — hence this note.

A Rendering may show less than the Report holds. It may never reach past the Report to
`queries.py` for something the Report does not carry: that is how the two assemblies grew apart
the first time.
