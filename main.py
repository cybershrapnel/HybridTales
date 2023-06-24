from typing import List, Dict, Union
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel
import hypercorn
from datetime import datetime
import json
import random
import fnmatch
import os
import glob
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow any method
    allow_headers=["*"],  # Allow any header
)

app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

# Keep track of todo's and stories. Does not persist if Python session is restarted.
_TODOS: Dict[str, List[str]] = {}
_STORIES: Dict[str, Dict[str, str]] = {}
_LOADED_FROM_FILE: Dict[str, bool] = {}
_STORY_ID: int = 0  # Keep track of the highest story id

class TodoItem(BaseModel):
    todo: str

class TodoIndex(BaseModel):
    todo_idx: int

class StoryItem(BaseModel):
    id: int
    title: str
    content: str
    author: str

@app.post("/todos/{username}", status_code=201)
async def add_todo(username: str, todo: TodoItem) -> Dict[str, str]:
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(todo.todo)
    return {"status": 'OK'}

@app.get("/scrape/")
async def scrape(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from the HTML
        content = soup.get_text()
        # Check if content exceeds maximum limit
        if len(content) > 10000:
            # Split content into chunks of 10000 characters
            content_chunks = [content[i:i+10000] for i in range(0, len(content), 10000)]
            return {"content": content_chunks}
        else:
            return {"content": content}
    else:
        return {"error": "Unable to scrape the URL"}

@app.get("/avatars/count_and_sample")
async def get_avatar_count_and_sample() -> Dict[str, Union[int, List[str]]]:
    # List all files in the avatars directory
    files = os.listdir("avatars")

    # Filter out non-text files
    text_files = [f for f in files if f.endswith(".txt")]

    # Get the count of text files
    count = len(text_files)

    # Get a random sample of 10 files, or all files if there are less than 10
    sample_size = min(10, count)
    sample_files = random.sample(text_files, sample_size)

    # Remove the .txt extension and format the filenames
    formatted_sample_files = [f"{i+1}. {f[:-4]}" for i, f in enumerate(sample_files)]

    return {"count": count, "sample": formatted_sample_files}

@app.get("/avatars/{keyword}")
async def get_avatar(keyword: str):
    # Normalize the keyword to lowercase
    keyword = keyword.lower()

    # List all files in the avatars directory
    files = os.listdir("avatars")

    # Try to find a direct match first
    for filename in files:
        if keyword in filename.lower():
            # Read the contents of the matching file
            with open(f"avatars/{filename}", 'r') as file:
                content = file.read()
            return {"avatar": filename, "content": content}

    # If no direct match is found, split the keyword and try to find a match for each word
    words = keyword.split()
    for word in words:
        for filename in files:
            if word in filename.lower():
                # Read the contents of the matching file
                with open(f"avatars/{filename}", 'r') as file:
                    content = file.read()
                return {"avatar": filename, "content": content}

    # If no match is found, return a message indicating this
    return {"message": "No matching avatar found"}

@app.get("/stories", response_model=List[StoryItem])
async def get_stories() -> List[Dict[str, str]]:
    return list(_STORIES.values())

@app.get("/todos/{username}", response_model=List[str])
async def get_todos(username: str) -> List[str]:
    return _TODOS.get(username, [])

@app.delete("/todos/{username}", status_code=204)
async def delete_todo(username: str, todo_index: TodoIndex):
    todos = _TODOS.get(username, [])
    if todo_index.todo_idx < len(todos):
        todos.pop(todo_index.todo_idx)
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.get("/prompts/random")
async def get_random_prompt():
    prompt_files = glob.glob('prompts/*.txt')
    if not prompt_files:
        raise HTTPException(status_code=404, detail="No prompt files found")
    random_file = random.choice(prompt_files)
    with open(random_file, 'r') as f:
        return {"prompt": f.read()}

@app.get("/tales/random")
async def get_random_tale() -> str:
    # Get all subdirectories in the 'tales' directory
    subdirectories = [f.path for f in os.scandir('tales') if f.is_dir()]

    # Select a random subdirectory
    random_subdirectory = random.choice(subdirectories)

    # Get all text files from the selected subdirectory
    file_paths = glob.glob(f'{random_subdirectory}/*.txt')

    # Extract the number from each filename and pair it with the file path
    numbered_files = []
    for file_path in file_paths:
        # Extract the number from the filename
        number = int(os.path.splitext(os.path.basename(file_path))[0].split('-')[-1])
        numbered_files.append((number, file_path))

    # Sort the files based on the number
    numbered_files.sort()

    # Read the content of each file and concatenate it
    content = ""
    for _, file_path in numbered_files:
        with open(file_path, 'r') as f:
            content += f.read() + "\n\n"

    return content

@app.get("/stories/count")
async def get_story_count() -> Dict[str, int]:
    return {"count": len(_STORIES)}

@app.post("/stories/{username}", status_code=201)
async def add_story(username: str, story: StoryItem) -> Dict[str, str]:
    global _STORY_ID
    _STORY_ID += 1
    author = story.author if story.author is not None else username
    _STORIES[story.title] = {"id": _STORY_ID, "title": story.title, "content": story.content, "author": author}
    
    # Save the story to a text file only if it was not loaded from a file
    if story.title not in _LOADED_FROM_FILE:
        filename = "stories/" + datetime.now().strftime("%m-%d-%y-%H-%M-%S") + ".txt"
        with open(filename, 'w') as f:
            f.write(json.dumps(_STORIES[story.title]))
    
    return {"status": 'OK'}
@app.get("/stories/id/{storyId}", response_model=StoryItem)
async def get_story_by_id(storyId: int) -> Dict[str, str]:
    for story in _STORIES.values():
        if story['id'] == storyId:
            return story
    raise HTTPException(status_code=404, detail="Story not found")

@app.get("/stories/{storyId}", response_model=StoryItem)
async def get_story(storyId: str) -> Dict[str, str]:
    story = _STORIES.get(storyId)
    if story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@app.get("/stories/search/{keyword}", response_model=List[StoryItem])
async def search_stories(keyword: str) -> List[Dict[str, str]]:
    return [story for story in _STORIES.values() if keyword.lower() in story['title'].lower()]

@app.get("/stories/author/{authorName}", response_model=List[StoryItem])
async def get_stories_by_author(authorName: str) -> List[Dict[str, str]]:
    return [story for story in _STORIES.values() if story['author'] == authorName]

@app.get("/logo.png")
async def plugin_logo() -> FileResponse:
    return FileResponse('logo.png', media_type='image/png')

@app.get("/openapi.yaml")
async def openapi_spec() -> Response:
    with open("openapi.yaml") as f:
        return Response(f.read(), media_type="text/yaml")

# Load stories from text files when the server starts
for filename in glob.glob('stories/**/*.txt', recursive=True):
    with open(filename, 'r') as f:
        story = json.loads(f.read())
        _STORIES[story['title']] = story
        _LOADED_FROM_FILE[story['title']] = True
        # Update the _STORY_ID if the loaded story's id is higher
        _STORY_ID = max(_STORY_ID, story['id'])

# If no stories were loaded from text files, start _STORY_ID at 1
if _STORY_ID == 0:
    _STORY_ID = 1
