Create a short, engaging story suitable for a language learner at a fluency level of ${fluency} / 10.
The story should be in ${language} and revolve around the theme: "${concept}".
Additionally, generate a list of at least three reading comprehension questions and associated answers.

Respond with a parsable JSON payload as if you were a REST API. Remember to escape any quotes inside a JSON string.
Use the following output format:
{
  "story": "<translation>",
  "questions": [
    {"question": "<question-1>", "answer": "<answer-1>"},
    {"question": "<question-2>", "answer": "<answer-2>"},
    ...
  ]   
}