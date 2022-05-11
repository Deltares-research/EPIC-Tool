## v0.21.0 (2022-05-11)

### Feat

- **epic_app/models/epic_user.py**: Added is_advisor property for EpicUsers, adapted related code

## v0.20.0 (2022-05-10)

### Feat

- **epic_answers.py**: We now list a summary of selected programs
- **views.py;serializers/report_serializer.py;models/epic_answers.py**: It is now possible to get a detailed summary of each question based on their (sub)type

## v0.19.0 (2022-05-06)

### Feat

- **serializers/progress_serializer.py;views.py;urls.py**: Added end point from /api/program/id/progress to retrieve the progress for the current logged in epic user, added serializer and adapted tests

## v0.18.0 (2022-05-04)

### Feat

- **epic_app/serializers/answer_serializer.py;epic_app/views.py**: We can now patch selected programs, adapted tests
- **epic_app/views.py**: Edited partial_update to allow admin to change values
- **views.py**: We now assign a valid serializer when creating answers from the endpoint /api/answer/
- **views.py**: Streamlined get-list get-detail (get / retrieve) for answers. Adapted tests
- **views.py**: API Client can now retrieve a serialized answer for a question without knowing either type
- **views.py**: Added endpoint for flat questions

### Refactor

- **views.py;urls.py**: Removed previous 'questions' viewsets as the 'QuestionViewSet' replaces the whole set.

## v0.17.0 (2022-05-03)

### Feat

- **generate_entity_admin.py**: Allow display of users in an organization
- **epic_app/admin_models/generate_entity_admin.py**: We can now generate epic users from the organization page
- **views.py;epic_user_serializer.py**: Added logic to update user's password
- **epic_app/serializers/epic_user_serializer.py**: Added serializer for EpicOrganization. Adapted and extended related tests
- **epic_app/models/epic_user.py**: Added organization as a model. Adapted setup and tests

### Refactor

- **epic_app/admin_models**: Moved admin models to different module for better maintenance of the django tree.

## v0.16.0 (2022-04-29)

### Feat

- **epic_app/importers/xlsx_question_importer.py**: Fixed question importer to include the group as a filtering condition
- **epic_app/importers**: We now import xlsx files instead of csv to make it more straightforward for end users

### Refactor

- **importers/xlsx**: Moved xlsx importers to its own module for better maintainance.

## v0.15.0 (2022-04-20)

### Fix

- **epic_answers.py**: fixed integrity check for base question after end-to-end testing.

### Feat

- **epic_answers.py;epic_questions.py**: Added constraints to answers so only specified question types can be added

## v0.14.0 (2022-04-19)

### Feat

- **epic_app/models/epic_questions.py**: Added Key Agency Actions table
- **answer_serializer.py**: Fixed posting answers
- **epic_app/views.py**: Changed views for answers so it's possible to post as an user or an admin

### Fix

- **epic_questions.py**: Fixed meta inheritance on questions to allow unique relationships

### Refactor

- **answer_serializer.py**: Removed serializer for raw answer as it is not necessary anymore
- **epic_answers**: Split answers from questions

## v0.13.0 (2022-04-15)

### Feat

- **epic_app/admin.py**: Added admin action to generate all linkages from available programs
- **epic_app/admin.py**: Added admin views to import national framework and evolution questions
- **question_csv_importer.py**: Added csv importers for NationalFrameworkQuestion and EvolutionQuestion

### Refactor

- **importers**: Extracted each importer in a separate file for better consistency
- **importers**: Moved importers into a separate directory to allow better maintainance

## v0.12.1 (2022-04-15)

### Refactor

- **views.py**: Improved EpicUserViewSet class definition; Extended related GET - detail test.

## v0.12.0 (2022-04-15)

### Feat

- **epic_app/views.py;question_serializer.py**: We now expose a get to get (all/detail) a question category for a given program
- **epic_app/urls.py;epic_app/serializers/question_serializer.py**: We now expose each question category individually
- **epic_app/serializers/epic_user_serializer.py**: Now we expose the list of selected programs for a given user
- **epic_app/models/epic_user.py**: Extended user definition to include list of selected programs

## v0.11.0 (2022-04-11)

### Feat

- **epic_app/serializers/answer_serializer.py**: Extended answer serializer definition to match question types
- **epic_app/models/epic_questions.py**: Now questions return a new (or existing) answer for the requested user. Added tests
- **epic_app/models/epic_questions.py**: Added answer types

## v0.10.0 (2022-04-08)

### Feat

- **epic_app/serializers/question_serializer.py**: Improved serializer so we have information of its subtypes directly
- **epic_app/models/epic_questions.py**: Added one-to-one constraint for linkages question by overriding the default save method
- **epic_app/models/epic_questions.py**: Added class for questions and created one model class per type from the mockups

### Refactor

- **epic_app/serializers**: Moved serializers into different directory to better maintain them
- **epic_app/models**: Moved models into separate directory for better maintainability

## v0.9.0 (2022-04-06)

### Feat

- **epic_app/importers.py**: Now we properly import the descriptions

## v0.8.0 (2022-04-06)

### Feat

- **epic_app/serializers.py**: Exposed description for programs

## v0.7.1 (2022-04-06)

### Fix

- **epic_app/serializers.py**: Fixed agency attribute for program serializer

## v0.7.0 (2022-04-06)

### Refactor

- **epic_app/importers.py**: modified agency null (should be blank) attribute, refactored importer code to reduce duplicity

### Feat

- **epic_app/importers.py;epic_app/models.py**: Added import csv functionality
- **epic_app/admin.py**: Added agency admin to import csv, adjusted tests
- **epic_app/models.py**: Updated program to include description and a unique name case-insensitive attribute
- **epic_app/models.py;epic_app/serializers.py**: Added Agency as a model and serializer, a cluster of programs

## v0.6.0 (2022-04-05)

### Refactor

- **epic_app/importers.py**: Extracted import logic for better maintainabilit

### Feat

- **epic_app/admin.py**: Added basic import functionality
- **urls.py**: Added redirection for the admin page
- **epic_app/urls.py**: We now directly redirect the default path to /api

## v0.5.0 (2022-03-23)

### Feat

- **epic_app/admin.py;epic_app/models.py;epic_app/templates/**: Added simple logic to enable future CSV importing of Areas, added templates

## v0.4.0 (2022-03-23)

### Feat

- **epic_app/models.py;epic_app/serializers.py;epic_app/views.py**: Added logic to serialize all data with their nested relationships
- **epic_app/models.py**: Extended logic so that clusters can be made
- **epic_app/admin.py**: Added relationships between area-group-program-question

## v0.3.0 (2022-03-23)

### Feat

- **settings.py**: Added middleware CORS to allow ui / backend communication with the /api/ url

## v0.2.0 (2022-03-22)

### Feat

- **epic_app/serializers.py**: Fixed posting answers through the browser regardless of the logged in user
- **epic_app/serializers.py**: Now the users api browser will not display the password which will be validated and required on post
- **epic_app/**: Changed serializers and views to require authentication for get / post data
- **epic_app/models.py**: Replaced cross-reference tables with single Answer and two foreign keys; adapted views and serializers

### Fix

- **epic_app**: Removed outdated reference to previous serializers / views
- **epic_app/admin.py**: Minor syntax fix

## v0.1.0 (2022-03-21)

### Fix

- **epic_app/serializers.py**: Fixed usage of wrong fields in the serializers
- **epic_app/serializers.py**: corrected typo

### Feat

- **epic_core/urls.py**: Stable urls just for epicuser table
- **epic_app/urls.py**: Added routing for the epic_app rest calls
- **epic_app/views.py**: Added ViewSet for all the existing serialized models
- **serializers.py**: Added JSON serializers
- **migrations/models.py**: Created basic models and cross-reference tables to be modified in the admin page
- **poetry**: Added poetry as package handler
- Small markdown fix
- Small markdown fix
- Small markdown fix
