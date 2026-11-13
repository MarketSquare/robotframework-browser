*** Settings ***
Resource          recorder.resource

Suite Setup       Allow Recording Headless    ${True}
Suite Teardown    Allow Recording Headless    ${False}
Test Setup        Open Form And Name Resource
Test Teardown     Run Keywords    End Any Recording Session    AND    Close Page    ALL    AND    Wait For All Promises

Test Tags         recorder

*** Test Cases ***
Every Recorded Selector Finds Exactly The Clicked Element
    [Documentation]    Playwright's generator picks a different selector shape for each element
    ...    of the page. Each translated selector must find the element that was clicked, and only it.
    # Playwright holds every click back for 500 ms.
    [Timeout]    2 minutes
    New Page    ${RECORDER_SELECTORS_URL}
    # Minimized in the bottom right corner, the toolbar covers none of the clicked elements.
    Evaluate JavaScript
    ...    ${None}
    ...    () => { sessionStorage.setItem('rfb.toolbar.position', JSON.stringify({x: 5000, y: 5000})); sessionStorage.setItem('rfb.toolbar.collapsed', 'true'); }
    Mark Clicked Elements    ${None}
    Mark Clicked Elements    id=frame >>> body
    ${promise} =    Promise To    Record Keyword    Click Everything    ${None}
    Toolbar State Should Be    recording
    VAR    @{targets}
    ...    css=h2
    ...    css=button >> nth=0
    ...    css=button >> nth=1
    ...    css=button >> nth=2
    ...    css=button >> nth=3
    ...    css=button >> nth=4
    ...    css=button >> nth=5
    ...    css=button >> nth=6
    ...    css=button >> nth=7
    ...    css=button >> nth=8
    ...    css=li button >> nth=0
    ...    css=li button >> nth=1
    ...    css=[data-testid="main-content"]
    ...    css=[data-testid="Main"]
    ...    css=input >> nth=0
    ...    css=input >> nth=1
    ...    id=named
    ...    css=input[title]
    ...    css=img
    ...    css=span >> nth=0
    ...    css=span >> nth=1
    ...    css=span >> nth=2
    ...    css=.no-text >> nth=0
    ...    css=.no-text >> nth=1
    ...    id=agree
    ...    css=[role=tab]
    ...    css=[role=checkbox]
    ...    css=.box >> nth=0
    ...    css=.box >> nth=1
    ...    css=.dot >> nth=0
    ...    css=.dot >> nth=1
    ...    css=.wrapped >> nth=0
    ...    css=.wrapped >> nth=1
    ...    css=input[aria-label=""]
    ...    css=.twin >> nth=0
    ...    css=span >> text=Twin
    ...    css=.split
    ...    text=Price
    ...    css=.labelled
    ...    text=In shadow
    ...    id=frame >>> text=In frame
    ...    id=frame >>> css=input
    FOR    ${index}    ${target}    IN ENUMERATE    @{targets}
        Click    ${target}
        Wait Until Calls    ${index + 1}
    END
    ${selectors} =    Evaluate JavaScript    ${None}
    ...    () => window.__rfbToolbarState.calls.map((call) => call.values[0].raw)
    Log Many    @{selectors}
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    FOR    ${index}    ${selector}    IN ENUMERATE    @{selectors}
        ${clicked} =    Evaluate JavaScript    ${selector}    (element) => element.__clicked
        Should Be Equal As Integers    ${clicked}    ${index}    ${targets}[${index}] was recorded as ${selector}
    END

Translated Selectors Match Like Playwright
    [Documentation]    Each form the recorder rewrites must find the same elements as
    ...    Playwright's internal original; forms passed through verbatim are not listed.
    New Page    ${RECORDER_SELECTORS_URL}
    FOR    ${internal}    IN
    ...    internal:role=button[name="Save"i]
    ...    internal:role=button[name="Save"s]
    ...    internal:role=button[name="SAVE"i]
    ...    internal:role=button[name=/^Save/]
    ...    internal:role=button[name="Say \\"hi\\" \\\\ now"s]
    ...    internal:role=button[pressed=true]
    ...    internal:role=button[expanded=false]
    ...    internal:role=heading[level=2]
    ...    internal:role=heading[name="Heading Level Two"i][level=2]
    ...    internal:role=tab[selected=true]
    ...    internal:role=checkbox[checked=true]
    ...    internal:role=button[name="In shadow"i]
    ...    internal:role=listitem >> nth=1
    ...    internal:role=listitem >> internal:role=button[name="Edit"i]
    ...    internal:text="Plain text"i
    ...    internal:text="plain TEXT"i
    ...    internal:text="Plain text"s
    ...    internal:text="Plain text twice"s
    ...    internal:text="Split text"s
    ...    internal:text="Split text"i
    ...    internal:text="Price (1.5) \\"net\\""s
    ...    internal:text="Price (1.5) \\"net\\""i
    ...    internal:text="\\"net\\""i
    ...    internal:text="Twin"s
    ...    internal:text=/^Twins?$/
    ...    internal:text="/not a regex/"i
    ...    css=div >> internal:has-text="Twin"i
    ...    div >> internal:has-text=/^Twin$/
    ...    div >> internal:has-text="Twins"s
    ...    internal:role=paragraph >> internal:has-text="Card one"i >> i
    ...    internal:testid=[data-testid="main-content"s]
    ...    internal:testid=[data-testid="Main"s]
    ...    internal:testid=[data-testid="main"i]
    ...    internal:attr=[placeholder="Email"i]
    ...    internal:attr=[placeholder="email"s]
    ...    internal:attr=[placeholder="email"]
    ...    internal:attr=[placeholder="EMAIL" I]
    ...    internal:attr=[title="Phone number"s]
    ...    internal:attr=[alt="logo"i]
    ...    internal:attr=[id="frame"s] >> internal:control=enter-frame >> internal:role=button[name="In frame"i]
    ...    internal:attr=[id="frame"s] >> internal:control=enter-frame >> internal:attr=[placeholder="email"i]
    ...    internal:label="Map widget"i
    ...    internal:label="map"i
    ...    internal:label="Full name"s
    ...    internal:control=any-frame >> internal:role=button[name="In frame"i]
    ...    internal:control=any-frame >> internal:attr=[id="inner"s] >> internal:control=enter-frame >> internal:role=button[name="Two frames deep"i]
        ${translated} =    Evaluate    Browser.recorder.action_mapper.to_browser_selector($internal)
        ...    modules=Browser.recorder.action_mapper
        Should Not Be Equal    ${translated}    ${internal}
        ${expected} =    Get Element Count    ${internal}
        Should Be True    ${expected} > 0    ${internal} finds nothing
        Get Element Count    ${translated}    ==    ${expected}    ${internal} -> ${translated}
    END
