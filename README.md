# desktop-groups
Organizes your desktop

## How do I use it?
Parse a valid desktopgroup file to the script, e.g.:

```bash
python -m desktop-groups C:\multimedia.desktopgroup
```

>[!TIP]
> Create a shortcut on your desktop!

## How do I make my own .desktopgroup file?

The desktopgroup format uses the JSON syntax. Here's how a file could look:

```json
{
    "$schema": "https://raw.githubusercontent.com/Nitro4542/desktop-groups/master/src/desktop-groups/desktopgroups.schema.json",
    "group": {
        "name": "my group",
        "icon": "C:\\icon.ico",
        "items": [
            {
                "name": "Command Prompt",
                "icon": "c:\\cmd.ico",
                "command": "cmd"
            },
            {
                "name": "Paint",
                "icon": "c:\\paint.ico",
                "command": "mspaint"
            }
        ]
    }
}
```

## License
```text
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
```