Act as my language teacher, I am currently at fluency of about ${fluency} / 10 in ${target_language}.
Let's play pictionary entirely in ${target_language}.
- Come up with any word of your choice, try to make it tricky! (also provide the ${native_language} translation)
- Create a prompt in ${native_language} I can give to an AI image generator to produce an image representing the word (don't worry, I won't actually see this, so you can include the word)

Respond only with a valid JSON payload as if you were a REST API.
Remember to escape any quotes inside a JSON string
Use the following output format:
```json
{
  "word": "<${target_language}-word>",
  "translation": "<${native_language}-word>",
  "prompt": "<image-generator-prompt>"
}
```