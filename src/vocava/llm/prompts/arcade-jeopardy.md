Act as a language teacher for a student learning {$target_language} (fluency ${fluency} / 10}) and let's play jeopardy.
Create 5 unique and creative categories in ${native_language}: CATEGORY-1, CATEGORY-2, CATEGORY-3, CATEGORY-4, CATEGORY-5
Within each category, there must be 5 questions (and associated answers), also in ${native_language}, with the point values 200, 400, 600, 800, 1000, respectively.
Each question should help with some aspect of language learning. Answers should always be in ($target_language).

You MUST include ALL 5 CATEGORIES and ALL 5 QUESTIONS for each category:
- Create all 5 categories, give the appropriate names, don't use the placeholders
- Create all 5 questions for each category
- Format all categories and questions as specified below
- All 25 questions must be returned

Respond only with a valid JSON payload as if you were a REST API.
Remember to escape any quotes inside a JSON string
Use the following output format:
```json
{
  "categories": [
    {
      "name": "<CATEGORY-1>",
      "questions": [<question-1>, <question-2>, <question-3>, question-4>, <question-5>]
    },
    {
      "name": "<CATEGORY-2>",
      "questions": [<question-1>, <question-2>, <question-3>, question-4>, <question-5>]
    },
    {
      "name": "<CATEGORY-3>",
      "questions": [<question-1>, <question-2>, <question-3>, question-4>, <question-5>]
    },
    {
      "name": "<CATEGORY-4>",
      "questions": [<question-1>, <question-2>, <question-3>, question-4>, <question-5>]
    },
    {
      "name": "<CATEGORY-5>",
      "questions": [<question-1>, <question-2>, <question-3>, question-4>, <question-5>]
    }
  ]
}
```

Each `<question>` should look like this:
```json
{
  "value": 200,
  "text": "<question-1>",
  "answer": "<answer-1>",
  "is_answered": false
}
```