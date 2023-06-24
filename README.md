![image info](./logo.png)

HybridTales Plugin for ChatGPT

This is a much more complicated verssion of a demonstration plugin I posted here:
[https://github.com/cybershrapnel/chatgpt-plugins-fastapi-quickstart](https://github.com/cybershrapnel/chatgpt-plugins-fastapi-quickstart)
If you find anything too complicated in this project then check out the old repo for educational purposes as it is a great place for anybody to start in regards to building a plugin.

How to install the plugin on OpenAI ChatGPT
![image info](https://steemitimages.com/p/C3TZR1g81UNaPs7vzNXHueW5ZM76DSHWEY7onmfLxcK2iNuUcdr1dVtynRCFB2KSzbefvezcfrSCrWFWnt5grMqDkHvN2TYc2Dz1ZN255PxgAPnCgM6CiSr)

And then make sure you enable the plugin after installation.

![image info](https://steemitimages.com/p/C3TZR1g81UNaPs7vzNXHueW5ZM76DSHWEY7onmfLxcK2iNz8wLEhRSHzHYZmVHYTxmizYrYJ5e4iZ5fLVmAw6SMUDwu2DD4TkWV2NcK7KpzrCcBhTyGidGS?format=match&mode=fit&width=500)

## Setup for your own plugin server

Clone this git into your desired location.

To install the required packages for this plugin, run the following commands to create a virtual environment and install the packages:

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

To relaunch your server from a new window you will need to reactivate your virtual Python space.

Simply type:
```bash
venv\Scripts\activate.bat
hypercorn main:app --bind 0.0.0.0:443 --certfile certificate.crt --keyfile private.key --log-level debug
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
[NanoCheeZe MEQUAVIS HybridTales API](https://nanocheeze.com/docs) - HybridTales API

You can access the API documentation and make queries using Swagger. Follow the steps below to get started:

1. You can run the project locally or from your domain to access the API. The API is interactive.
2. Open your web browser and visit [http://localhost/docs](http://localhost/docs). (or your domain instead of localhost)
3. On the API page, you'll find an interactive interface that allows you to explore and test the different API routes and endpoints.

![image info](./swagger.png)

