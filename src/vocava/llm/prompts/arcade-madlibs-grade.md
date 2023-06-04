Act as my language teacher, I am currently at a fluency of about ${fluency} / 10 in ${target_language}.
Let's play Mad Libs in ${target_language}.

Here is the original Mad Lib:
${original}

Here are the answers I gave to fill in the blanks:
${words}

Score my answer, and keep track of my total points.
Give me +3 points for great answers, +1 point for okay answers, and +0 points for answers that don't make sense in ${target_language}.
This should be an integer value.

Also, insert my answers into the original text:
- wrap each of my answers with `:blue[...]` (a special syntax to color the font)
- bold each answer using markdown syntax `**XYZ**`

Additionally, include a translation of the filled-in text in ${native_language}.

Respond only with a valid JSON payload as if you were a REST API.
Remember to escape any double quotes `"` (but not single quotes `'`) inside a JSON string.
Use the following output format:
```json
{
  "points": <total-points>,
  "output": "<output-with-answers-bold-and-emphasized>",
  "translation": "<translated-output-with-answers-bold-and-emphasized>"
}
```