Translate the following TEXT from ${native_language} to ${target_language}:
TEXT:
"${text}"

Provide an explanation of the translation that could aid a language learner, focusing on any particularly tricky translations, idioms, or cultural nuances.

Respond only with a valid JSON payload as if you were a REST API.
Remember to escape any quotes inside a JSON string.
DO NOT include any comments or invalid JSON like `...`.
Use the following output template:
```json
{
  "translation": "<translation>",
  "explanation": "<explanation>"
}
```