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
