Act as my language teacher, I am currently at a fluency of about ${fluency} / 10 in ${target_language}.
Let's play Mad Libs in ${target_language}.
- Create the actual text, using underscores for the words I need to fill in.
- Give me a list of the parts of speech that should go into each blank.

Respond only with a valid JSON payload as if you were a REST API.
Remember to escape any quotes inside a JSON string
Use the following output format:
```json
{
  "text": "<${target_language}-mad-lib-text>",
  "blanks": [
    "<part-of-speech-for-blank-1>",
    "<part-of-speech-for-blank-2>",
    ...
  ]
}
```