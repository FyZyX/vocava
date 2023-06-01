Translate the following TEXT from ${native_language} to ${target_language}:
TEXT:
"${text}"
Provide an explanation of the translation that could aid a language learner, focusing on any particularly tricky translations, idioms, or cultural nuances.

Respond with a parsable JSON payload as if you were a REST API. Use the following output format:
{
  "translation": "<translation>",
  "explanation": "<explanation>"
}