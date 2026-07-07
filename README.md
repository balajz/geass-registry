<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
![Geass](https://img.shields.io/badge/Geass-000000?style=for-the-badge)
![Registry](https://img.shields.io/badge/Registry-7B36ED?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">g-registry</h1>
  <p align="center">
    The central remote template registry for the Geass CLI.
  </p>
  <p align="center">
    <i>Note: The <a href="https://github.com/balajz/geass">Geass CLI</a> is currently under development.</i>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

`g-registry` serves as the core database and remote backend for **Geass**. 

Geass is a tool built to be the "Homebrew for project templates"—allowing developers to search for, filter, and seamlessly download starter boilerplates across any language or framework without having to manually hunt through GitHub.

Instead of hitting the GitHub API live for every search, Geass queries this highly curated registry. This repository stores all the templates, frameworks, and boilerplates as structured YAML, making searches instant and reliable.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To keep the registry clean and avoid duplicate entries, we manage everything using a custom Python CLI tool called `registrar`.

### Installation

You can install the `registrar` CLI directly from the root of this repository.

#### Using uv (Recommended)
```bash
uv tool install ./registrar
```

#### Using pip
```bash
pip install -e ./registrar
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->
## Usage

Once installed, the `registrar` command is available globally. **Always run these commands from the root directory of this repository** so the CLI can locate and update the `index.yaml`.

### Initializing a New Package
If a specific technology or framework isn't in the registry yet, create the package first:
```bash
registrar package init fastapi \
    --name FastAPI \
    --language python \
    --type framework \
    --tag web \
    --tag async
```

### Adding a Repository
Once a package exists, register a GitHub template/boilerplate under it:
```bash
registrar repository add fastapi \
    --owner fastapi \
    --repo full-stack-fastapi-template \
    --kind template \
    --stack react \
    --stack postgres \
    --stars 40000 \
    --official
```

For full documentation of the flags, simply run:
```bash
registrar --help
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

We love it when developers register their own templates, starters, and boilerplates! By adding your repository to the registry, it becomes instantly searchable and downloadable for the entire community.

To get started, please read our [Contributing Guide](CONTRIBUTING.md) to learn how to use the CLI to easily register your templates and submit a pull request.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
