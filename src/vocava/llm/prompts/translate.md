Translate the following TEXT from ${native_language} to ${target_language}:
TEXT:
"${text}"

Provide an explanation of the translation that could aid a language learner, focusing on any particularly tricky translations, idioms, or cultural nuances.
Additionally, provide part of speech tagging on the translation, as well as a word-by-word translation. This should return a list of objects obtained by splitting the words in the translation, attaching their part-of-speech and translations.

Respond only with a valid JSON payload as if you were a REST API.
Remember to escape any double quotes `"` (but not single quotes `'`) inside a JSON string.
DO NOT include any comments or invalid JSON like `...`.
Use the following output template:
```json
{
  "translation": "<${target_language}-translation>",
  "explanation": "<${native_language}-explanation>",
  "dictionary": [
    {"word": "<word-1-of-${target_language}-translation>", "original": "<corresponding-word-in-original-${native_language}-text>", "pos": "<part-of-speech>"},
    ...
  ]
}
```