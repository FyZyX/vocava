Translate the following ARTICLE from ${target_language} to ${native_language}:

ARTICLE TITLE:
${title}
---
ARTICLE DESCRIPTION:
${description}
---
ARTICLE CONTENT:
${text}
---

Respond only with a valid JSON payload as if you were a REST API.
Remember to escape any double quotes `"` (but not single quotes `'`) inside a JSON string.
DO NOT include any comments or invalid JSON like `...`.
Use the following output template:
```json
{
  "title": "<translated-title>",
  "description": "<translated-description>",
  "content": "<translated-content>"
}
```