# API Reference

## Endpoints

All endpoints produces a JSON response.

### GET /questions

Returns a list of all questions

Sample request
```bash
curl http://localhost:5000/questions
curl http://localhost:5000/questions?page=2
```
Sample response
```bash
{
    'questions': [
      {
        'answer': 'Maya Angelou',
        'category': 4,
        'difficulty': 2,
        'id': 5,
        'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      },
      ...
    ],
    'total_questions': 20,
    'categories': {
      '1': 'Art',
      '2': 'Science',
      ...
    },
    'current_category': null
}
```


### POST /questions

Adds a new question or search for a question by the `searchTerm` argument.

Sample request  #1
```bash
curl -d '{"question": ..., "answer": ..., "difficulty": 2, "category": 3}' -H 'Content-Type: application/json' -X POST http://localhost:5000/questions
```

Sample response #1
```bash
{
  'success': true
}
```

Sample request #2
```bash
curl -d '{"searchTerm": "oscar"}' -H 'Content-Type: application/json' -X POST http://localhost:5000/questions
```
Sample response #2
```bash
{
    'questions': [
      {
        'answer': 'Apollo 13',
        'category': 5,
        'difficulty': 4,
        'id': 2,
        'question': "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      },
      ...
    ],
    'total_questions': 20,
    'current_category': null
}
```


### DELETE /questions/<id\>

Deletes question based on id

Sample request  #1
```bash
curl -X DELETE http://localhost:5000/questions/2
```

Sample response #1
```bash
{
  'success': true
}
```


### GET /categories

Returns a list of all the categories

Sample request
```bash
curl http://localhost:5000/categories
```
Sample response
```bash
{
    'categories': {
      '1': 'Geography',
      '2': 'Science',
      ...
    }
}
```


### GET /categories/<id\>/questions

Gets all questions under a certain category.

Sample request
```bash
curl http://localhost:5000/categories/1/questions
```

Sample response
```bash
{
    'questions': [
      {
        'answer': 'Blood',
        'category': 1,
        'difficulty': 4,
        'id': 10,
        'question': "Hematology is a branch of medicine involving the study of what?"
      },
      ...
    ],
    'total_questions': 20,
    'current_category': 1
}
```


### GET /quizzes>

Returns the next question in the quiz or _null_ if at the end.

Sample request
```bash
curl -d '{"previous_questions": [4, 1], "quiz_category": {"type": "Science", "id": 2}' -H 'Content-Type: application/json' -X POST http://localhost:5000/quizzes
```

Sample response
```bash
{
  'success': true
}
```

## Error Handling

All errors are returned as JSON objects

```bash
{
    'success': false,
    'error': 400,
    'message': 'Bad request'
}
```
- 400: Bad request
- 404: Not found
- 405: Method not allowed
- 422: Unprocessed entity
