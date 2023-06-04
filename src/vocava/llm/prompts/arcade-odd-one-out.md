Act as my language teacher, I am currently at a fluency of about ${fluency} / 10 in ${target_language}.
Let's play a game called Odd One Out.
Give me a group of 5 words/phrases in ${target_language} around a common theme.
Then, add one new word to the group in ${target_language}, except this one doesn't belong to the common theme, though it also shouldn't obviously stand out.
Shuffle the group of all 6 words so the odd one out is in a random spot.

Respond only with a valid JSON payload as if you were a REST API.
Remember to escape any double quotes `"` (but not single quotes `'`) inside a JSON string.
Use the following output format:
```json
{
  "${target_language}": {
    "words": ["<word-phrase-1>", "<word-phrase-2>", ...],
    "theme": "<common-theme>",
    "answer": "<odd-one-out>"
  },
  "${native_language}": {
    "words": ["<translated-word-phrase-1>", "<translated-word-phrase-2>", ...],
    "theme": "<translated-common-theme>",
    "answer": "<translated-odd-one-out>"
  }
}
```