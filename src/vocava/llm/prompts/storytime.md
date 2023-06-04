Create a short, engaging story suitable for a language learner at a fluency level of ${fluency} / 10.
Fluency of 1 / 10 should be story a child could understand. Fluency of 10 / 10 should contain sophisticated language at nearly native capability.
The story should be in ${target_language} and revolve around the theme: "${concept}".
Additionally, generate a list of at least three reading comprehension questions and associated answers.
Finally, translate all of this into ${native_language} for the learner's convenience.

Respond with a parsable JSON payload as if you were a REST API.
Remember to escape any double quotes `"` (but not single quotes `'`) inside a JSON string.
Use the following output format:
{
  "story": {
    "$target_language": "<story>",
    "$native_language": "<translated-story>"
  },
  "questions": [
    {"question_$target_language": "<question-1>", "answer_$target_language": "<answer-1>", "question_$native_language": "<translated-question-1>", "answer_$native_language": "<translated-answer-1>"},
    ...
  ]   
}