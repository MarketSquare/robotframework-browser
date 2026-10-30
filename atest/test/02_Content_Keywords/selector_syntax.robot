*** Settings ***
Documentation     Browser's own selector syntax on top of Playwright's: `>>>`, a leading
...               `>>>` and `label=`, and the same characters inside quoted text.

Resource          imports.resource

Suite Setup       New Page    ${ROOT_URL}selector-syntax.html
Suite Teardown    Close Page

*** Test Cases ***
A Frame Separator Inside Quotes Is Text
    Get Text    text="Save >>> later"    ==    Save >>> later
    Get Text    "Save >>> later"    ==    Save >>> later
    Get Element Count    css=button:has-text("Save >>> later")    ==    1

A Label Engine Inside Quotes Is Text
    Get Text    text="label=Email"    ==    label=Email

A Quoted Text Before A Frame Separator Is Kept
    Get Text    css=iframe[id="outer"] >>> text="Frame code"    ==    Frame code

Label Finds An Input By Its Label Element
    Fill Text    label=Email address    someone@example.com
    Get Property    id=email    value    ==    someone@example.com
    Get Property    label="Email address"s    value    ==    someone@example.com

Label Finds An Input Inside Its Label
    Fill Text    label=Phone    12345
    Get Property    id=phone    value    ==    12345

Label Finds An Input Labelled By Another Element
    Fill Text    label=City    Berlin
    Get Property    id=city    value    ==    Berlin

Label Finds An Element By Its Aria Label
    Get Attribute    label=Map widget    id    ==    map

Label Matches Case Insensitive Substrings Unless Quoted With s
    Get Element Count    label=email ADDRESS    ==    1
    Get Element Count    label="email ADDRESS"s    ==    0
    Get Element Count    label=/^e-?mail/i    ==    1

Label Chains With Other Clauses
    Get Attribute    css=body >> label=Phone    id    ==    phone

Label Works Inside A Frame
    Fill Text    id=outer >>> label=Frame code    42
    Get Property    id=outer >>> id=code    value    ==    42

Label Works In Any Frame
    Fill Text    >>> label=Inner pin    1234
    Get Property    id=outer >>> id=inner >>> id=pin    value    ==    1234

A Selector Prefix Of Nested Frames Works For Get Element By
    ${old} =    Set Selector Prefix    id=outer >>> id=inner >>>
    TRY
        ${element} =    Get Element By    Label    Inner pin
        Get Property    ${element}    value    ==    1234
    FINALLY
        Set Selector Prefix    ${old}
    END

A Label With An Apostrophe Needs No Quotes
    Fill Text    label=Customer's name >> nth=0    Ada
    Get Property    id=customer    value    ==    Ada

Frame Separators Without Whitespace Keep Their Old Meaning
    Get Element Count    body>>>button    ==    2

A Part Next To A Frame Separator Must Not Be Empty
    Run Keyword And Expect Error    *has an empty part next to ">>>"*    Get Text    id=outer >>>

A Leading Frame Separator Fails On Matches In Several Frames Even Without Strict Mode
    ${old} =    Set Strict Mode    False
    TRY
        Run Keyword And Expect Error    *multiple frames*    Get Element Count    >>> css=label
    FINALLY
        Set Strict Mode    ${old}
    END

A Selector Prefix Of Only A Frame Separator Works For Get Element By
    ${old} =    Set Selector Prefix    >>>
    TRY
        ${element} =    Get Element By    Label    Frame code
        Get Attribute    ${element}    id    ==    code
    FINALLY
        Set Selector Prefix    ${old}
    END

A Quoted Frame Separator Is No Frame For Focus States
    Wait For Elements State    text="Save >>> later"    defocused    timeout=2s
