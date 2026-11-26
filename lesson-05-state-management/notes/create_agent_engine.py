import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))  # the .env in the folder you run it from

import vertexai

project = os.environ.get("GOOGLE_CLOUD_PROJECT")
location = os.environ.get("GOOGLE_CLOUD_LOCATION")
print(f"connecting to {project}@{location}")
client = vertexai.Client(
  project=project,
  location=location,
)

agent_engine = client.agent_engines.create()

# Optionally, print out the Agent Engine resource name. You will need the
# resource name to interact with your Agent Engine instance later on.
print(agent_engine.api_resource.name)