Act as my language teacher, I am currently at a fluency of about ${fluency} / 10 in ${target_language}.
Let's play a game called Odd One Out.
Give me a group of 6 words/phrases in ${target_language} around a common theme, where one of the words/phrases doesn't belong.
Remember, the odd one out should not belong to the common theme, but should also not stick out obviously.

Respond only with a valid JSON payload as if you were a REST API.
Remember to escape any quotes inside a JSON string
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