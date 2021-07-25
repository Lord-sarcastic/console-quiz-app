# console-quiz-app
A console based quiz application written in Python for the Python mentorship track for DSC OAU

## Task description:
Create a console-based quiz application. Should load 20 random (use the random module) from a JSON (use the JSON module) file of more than 20 questions.

Each question should have at least 2 options and at most 4.

User should be able to answer with the option letter, for example: "a" or "b" (hint: convert user input to either upper or lower case for consistency)

User score should be tracked. 

In the event the user stops the app without finishing the questions, it should resume where the user stopped with the exact list of questions and the current score.

## Constraints:
- Solution should be deployed to Github with the repo name: console-quiz-app
- Each question after loaded from the JSON file should be class based. And should have attributes:
    * Question (string), options (tuple), answer (index of the answer in the options tuple), and any other additional attribute.

    And methods:
    * Question.check_answer(<option) returns true or false if the option is the correct option.
    * And any other method you like

- Use PEP coding style
- Ensure to handle edge cases and invalid answers.

Time limit: Thursday, 8pm.

Your repo should be created immediately you see this message and share the link here so I can track your progress.

Let your commits be consistent. I don't want one commit for the entire project. Push as you code.

Let your commit message have the following format:

- When you add a new feature: Feature: Implemented caching for unfinished quiz

- When you add a piece of functionality that's not a new feature: Chore: Added JSON file for questions

- When you fix a bug: Fix: Fixed cases where user edited question file

- When you push an update that has bugs and will not run: Buggy: Saved application state

Have a README file that shows how to run your application

Good luck