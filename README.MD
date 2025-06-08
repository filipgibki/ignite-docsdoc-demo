Repository with demo app for testing DocsDoc

Structure:
- ignite-todo - demo app source (React)
- docs
    - specs - folder with implementation specs for the demo app
    - end-user - end-user documentation that we will updated

Required tools:
- Node.js for running the ignite-todo
- Python for running the MkDocs documentation generator

Running the app:
```bash
# Prerequisites: Node.js

# Install dependencies
cd ignite-todo
npm install

# Run the app
npm run dev
```

Running the documentation generator:
```bash
# Prerequisites: 
    - Python
    - uv
    - Netskope set for python (https://appfireteam.atlassian.net/wiki/spaces/help/pages/96244793910/HOWTO+Work+with+Netskope+SSL+interception)
    - SSL flag set for uv - 'export UV_NATIVE_TLS=true && source $HOME/.local/bin/env'

# Initiate the virtual environment
cd docs
uv venv
uv sync

# Run the documentation generator
uv run mkdocs serve
```


Testing philosophy:
- Repo will contain carefully crafted commits
- Each commit will be a ne version of the app with added or changed features
- Each commit will contain a "baseline" end-user documentation that we will try to update with DocsDoc

This approach ensures that we can evaluate different approaches to updating the documentation using the same "input data".
