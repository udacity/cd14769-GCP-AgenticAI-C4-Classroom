# Module 06 Exercise

## Environment

GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=global

TOOLBOX_URL=http://127.0.0.1:5001

MYSQL_HOST=<your mysql server IP address>
MYSQL_USER=<mysql user>
MYSQL_PASSWORD=<mysql password>


Make sure you replace <your project ID> with the ID for your project.

Use a LOCATION of global: the Gemini models these exercises use are served
there. In the course's lab projects, a regional location such as
us-central1 answers 404 NOT_FOUND.

## Additional Setup

### ADK A2A

In the parent directory from this one, you'll run:
```bash
adk web --a2a
```
