Act as my language teacher, I am currently at a fluency of about ${fluency} / 10 in ${target_language}.
Let's play Mad Libs in ${target_language}.
- Create the actual text, using underscores for the words I need to fill in.
- Give me a list of the parts of speech (in ${native_language}) that should go into each blank. There should be no more than 9 blanks. Remember to use a variety of parts of speech, including nouns, verbs, adjectives, adverbs, etc.

Respond only with a valid JSON payload as if you were a REST API.
Remember to escape any double quotes `"` (but not single quotes `'`) inside a JSON string.
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