![image info](./logo.png)

HybridTales Plugin for ChatGPT
# built from [FastAPI] ChatGPT plugins quickstart

How to install the plugin on OpenAI ChatGPT
![image info](https://steemitimages.com/p/C3TZR1g81UNaPs7vzNXHueW5ZM76DSHWEY7onmfLxcK2iNuUcdr1dVtynRCFB2KSzbefvezcfrSCrWFWnt5grMqDkHvN2TYc2Dz1ZN255PxgAPnCgM6CiSr)

And then make sure you enable the plugin after installation.

![image info](https://steemitimages.com/p/C3TZR1g81UNaPs7vzNXHueW5ZM76DSHWEY7onmfLxcK2iNz8wLEhRSHzHYZmVHYTxmizYrYJ5e4iZ5fLVmAw6SMUDwu2DD4TkWV2NcK7KpzrCcBhTyGidGS?format=match&mode=fit&width=500)

## Setup

To install the required packages for this plugin, run the following command to create a virtual environment and install the packages:

```bash
python -m venv venv
```
```bash
venv\Scripts\activate.bat
```
```bash
pip install -r requirements.txt
```

To run the plugin, enter the following command:
```bash
hypercorn main:app --bind 0.0.0.0:443 --certfile certificate.crt --keyfile private.key --log-level debug
```

or use uvicorn for localhost testing (can also use hypercorn with ssl on localhost)

```bash
uvicorn main:app --reload
```

Once the local server is running:

1. Navigate to https://chat.openai.com. 
2. In the Model drop down, select "Plugins" (note, if you don't see it there, you don't have access yet).
3. Select "Plugin store"
4. Select "Develop your own plugin"
5. Enter in `localhost:443` if testing local or your domain name if live. Then select "Find manifest file".
6. Must have SSL certs installed. I suggest getting a free 3-month ssl cert from zerossl for testing and experimentation.
*** You can run on port 8000 or 443 with some slight changes to code without ssl but I would not recoment it and it's easier to just setup the ssl from the start as this is setup for it. Comment out line in file and comment the other one. This git is setup to run a localhost or a domain on port 443 for https access as required by OpenAI Plugins. You can use localhost without ssl only.

The plugin should now be installed and enabled! You can start with a question like "What is on my todo list" or "create a random story and add it to the stories list" and then try adding something to it as well! You can simply ask to see either list.

## Using the API via Swagger
[http://localhost:8000/docs](NanoCheeZe MEQUAVIS HybridTales API)]()

You can access the API documentation and make queries using Swagger. Follow the steps below to get started:

1. You can run the project locally or from your domain.
2. Open your web browser and visit [http://localhost:8000/docs](http://localhost:8000/docs). (or your domain instead of localhost)
3. On the API page, you'll find an interactive interface that allows you to explore and test the different API routes and endpoints.

![image info](./swagger.png)

## Getting help

If you run into issues or have questions building a plugin, please join our [Developer community forum](https://community.openai.com/c/chat-plugins/20).
