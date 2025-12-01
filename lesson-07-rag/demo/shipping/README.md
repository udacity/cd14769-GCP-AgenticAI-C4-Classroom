# Module 06 Demo

## Environment

GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=us-central1

TOOLBOX_URL=http://127.0.0.1:5001

MYSQL_HOST=<your mysql server IP address>
MYSQL_USER=<mysql user>
MYSQL_PASSWORD=<mysql password>

DATASTORE_PROJECT_ID=<your project ID>
DATASTORE_ENGINE_ID=<your data store ID>
DATASTORE_LOCATION=global


Make sure you replace <your project ID> with the ID for your project.

Using a LOCATION of us-central1 is usually the best bet in the United States,
but consider other cloud data center locations for elsewhere.

See below for the values that are needed for the TOOLBOX_URL and the
various MYSQL environment variables

The Datastore location should be set to "global".
The Datastore Engine ID should be set to the AI Applications App ID.

## Additional Setup

### Google Cloud Storage and AI Applications

There are a number of files in the "demo" folder to upload to GCS and then
index using AI Applications.

To create a Cloud Storage bucket and upload to it:
1. In the Google Cloud Console, go to the "Cloud Storage" configuration.
   (Hint: You can search for it in the search bar)
2. Select "Create bucket"
3. Enter the name you want for the bucket.
4. Select "Create"
5. If there is a pop-up about Public access, confirm that you want Enforce
   public access prevention enabled.
6. You'll be taken to an (empty) file listing. You can drag and drop the
   files from the "docs" directory here.

To create your AI Application and data store:
1. In the Google Cloud Console, go to the "AI Application" configuration.
   (Hint: You can search for it in the search bar)
2. Select "Create App"
3. Select "Custom search (general)"
4. Leave the app settings unchanged
5. Enter an App name
6. Enter a company name for the app
7. Select "Continue"
8. You'll be taken to the Data Stores page. Select "Create Data Store"
9. Select "Cloud Storage" to import the data from the bucket we created above
10. Select "Unstructured documents"
11. Set the Synchronization frequency to "One time"
12. Choose the GCS bucket you uploaded the files to above
13. Enter a Data store name. It is usually a good idea to have it a name
    based on the App name you chose
14. Select "Create"
15. You'll be taken back to the last step of the Create App. Select "Create"

The system will then begin to load and index the documents. You can see
the status of this by selecting the "Data" menu item on the left when
looking at the App information.

If you return to the list of AI Apps, you will see the ID that is used
for this AI App instance. This is the value of the "DATASTORE_ENGINE_ID" above.

### ADK A2A

In the parent directory from this one, you'll run:
```bash
adk web --a2a
```

### Setup Google Cloud SQL

If you do not already have an SQL instance to use:

1. In the Google Cloud Console, go to the "Cloud SQL" configuration. (Hint:
   You can search for it in the search bar.)
2. Select "Create Instance"
3. Choose MySQL
4. Select the Enterprise edition. **Not** the "Enterprise Plus" edition
5. Select Edition preset: Sandbox
6. Choose Database version: MySQL 8.0
7. Set the Instance ID
8. Set the root password
9. Choose the "us-central1" region with a Single zone. (You can choose
   another region, but it should be the one that most of your project runs in.)
10. Select Customize your instance
11. Change the Machine configuration to 1 vCPU
12. You can leave other settings alone and select the "Create instance" button.

Once the instance is created / updated, you can get the Public IP address
from the list of instances and enter it as the value for MYSQL_HOST in your
.env file.

You can then connect to the database server using the local mysql command
with something like:

```
mysql -h <ip_address> -u root -p 
```

You can then load in the database and files with a MySQL command
`\s docs/shipping.sql`.

You then need to permit your user to the database with a MySQL commands such as
```mysql
GRANT SELECT ON `db_name`.* TO `user_name`@`%`;
GRANT INSERT, UPDATE ON `db_name`.orders TO `user_name`@`%`;
```

### Setup and run MCP Toolbox

See [here](https://googleapis.github.io/genai-toolbox/getting-started/introduction/)
for how to download the toolbox server for your platform.

To run the MCP server:
1. From the command line, change directories to where your tools.yaml file is
2. Make sure the MYSQL environment variables are exported in your current
   command line
    - If this is using bash, for example, you might do this as something like
      `export $(grep -v '^#' .env | xargs)`
3. Run `/path/to/toolbox --tools-file tools.yaml`
    - If you need to use another port, you can include a --port parameter

Update the TOOLBOX_URL in the .env file to specify the hostname (usually
localhost) and port the MCP Server is listening to.