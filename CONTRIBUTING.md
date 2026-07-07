# Contributing to the Geass Registry

We love it when developers register their own templates, starters, and boilerplates! By adding your repository to this registry, it becomes instantly searchable and downloadable for anyone using the Geass CLI.

## How to Register Your Template

While you *can* manually edit the YAML files, we **highly recommend** using the `registrar` CLI tool. It automatically handles YAML formatting, updates the internal index, and prevents duplicate entries.

### 1. Set Up the CLI

First, clone this repository and install the CLI tool from the root directory:

```bash
# If you use uv (Recommended)
uv tool install ./registrar

# If you use pip
pip install -e ./registrar
```

### 2. Register the Core Package (If Needed)

Check if the framework or language for your template already exists in the registry. If it doesn't, initialize it first:

```bash
registrar package init myframework \
    --name MyFramework \
    --language python \
    --type framework \
    --tag web
```

### 3. Add Your Repository

Register your GitHub template or boilerplate under the relevant package:

```bash
registrar repository add myframework \
    --owner your-username \
    --repo your-cool-template \
    --kind template \
    --stack react \
    --stars 120
```

### 4. Submit Your Pull Request

Once you have added your repository and the YAML files are updated:

1. Create a new branch for your addition: `git checkout -b add/your-cool-template`
2. Commit your changes: `git commit -m "Add your-cool-template to myframework"`
3. Push to your fork: `git push origin add/your-cool-template`
4. Open a Pull Request!

Once merged, your template will be officially available in the Geass ecosystem. Thank you for sharing your work!
