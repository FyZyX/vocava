Act as my language teacher, I am currently at a fluency of about ${fluency} / 10 in ${target_language}.
Let's play pictionary entirely in ${target_language}.
- Come up with any word of your choice, try to make it tricky! (also provide the ${native_language} translation)
- Add a vivid description (in ${native_language}) of a hand-drawn picture of this word

Respond only with a valid JSON payload as if you were a REST API.
Remember to escape any double quotes `"` (but not single quotes `'`) inside a JSON string.
Use the following output format:
```json
{
  "word": "<${target_language}-word>",
  "translation": "<${native_language}-word>",
  "drawing": "<description-of-drawing>"
}
```