# Google Cloud Platform

Google Cloud Platform provides `storage buckets` to store data for projects. It also provided a Pythonic configuration to read, write, store, and delete data from those buckets. This folder has the functions and modules relating Google Bucket storage.

__Note__: Before using the functions, add your `SERVICE ACCOUNT CREDENTIALS` to the environment variables. Follow the instructions [here](https://m2msupport.net/m2msupport/generate-service-account-key-in-google-cloud-platform-gcp/) to generate `JSON` key file and store it as a variable, following instructions [here](https://saturncloud.io/blog/how-to-access-data-in-google-cloud-bucket-for-a-python-tensorflow-learning-program/).

### Google CLI authentication
* In order to authenticate gcloud cli in a local or remote machine, you have to have the [google cloud project](https://developers.google.com/workspace/marketplace/create-gcp-project) setup on the GCP platform.
* Make sure to install [gcloud sdk](https://cloud.google.com/sdk/docs/install) in both the local and remote machine
__Note__: If you are running the project on a remote machine, Run `gcloud auth login --no-browser` in the terminal, and copy the `gcloud auth login --remote-bootstrap=......` link in the local machine with web browser, after choosing an account, copy the link `https://localhost:......` on to the remote machine to complete the authentication process.
* Run `gcloud auth login` to authenticate google account in your IDE.
* After authentication you can see the active accounts using the command `gcloud auth list`, in which there is a `*` on the active account. Along with this you can see projects using `gcloud projects list`, and set a default project using `gcloud config set project 'PROJECT_ID'`
* When running a Google cloud VM instance, to set GCP SSH in config, you need to have [Google SDK](https://cloud.google.com/sdk/docs/install) installed in your system first, after installing open the Google SDK console and follow the instructions, then set Google VM SSH in `config` by running `gcloud compute config-ssh`.

# TODO: There is a python package "[geobeam](https://github.com/GoogleCloudPlatform/dataflow-geobeam)" to read GIS data from Google cloud data storage.
