from pathlib import Path

import yaml

from ..models.package import (
    Package,
    PackageDetails,
    PackageMetaData,
    PackageType,
    Repository,
)
from .index import Index

INDEX_FILE = "index.yaml"


class Registry:
    index: Index
    root: Path

    def __init__(self, root: str):
        self.root = Path(root)
        self.index = Index.load(Path(root, INDEX_FILE))

    def save_package(self, package: Package, language: str) -> None:
        path = Path(self.root, language, f"{package.package.id}.yaml")
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                package.model_dump(mode="json"),
                f,
                sort_keys=False,
                allow_unicode=True,
            )

    def load_package(
        self,
        *,
        language: str | None = None,
        name: str | None = None,
        file_path: Path | None = None,
    ) -> Package:
        if file_path is not None:
            return self._load_package(file_path)

        if language is not None and name is not None:
            path = self.root / language / f"{name}.yaml"
            return self._load_package(path)

        raise ValueError("either file_path or language and name must be provided")

    def _load_package(self, path: Path) -> Package:
        if not path.exists():
            raise FileNotFoundError(f"package file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            return Package.model_validate(yaml.safe_load(f))

    def add_package(
        self,
        id: str,
        name: str,
        language: str,
        type: PackageType,
        aliases: list[str] = [],
        tags: list[str] = [],
    ) -> Package | None:
        """
        add a package to the registry, create a new directory for the language if none exists.
        creates a pacakge file and add package details to it.
        it doesn't add repositories to the package.
        It creates a package entry, so that repositories can be add in future.
        example:
            - add_package("fastapi", "FastAPI", "python", PackageType.framework)
            - add_package("cobra", "Cobra", "go", PackageType.framework)
        """
        # check if the language directory exists, create it if not
        if language not in self.index.languages:
            Path(self.root, language).mkdir(parents=True, exist_ok=True)
            self.index.languages[language] = []

        package = Package(
            package=PackageDetails(
                id=id,
                name=name,
                language=language,
                type=type,
            ),
            metadata=PackageMetaData(
                aliases=aliases,
                tags=tags,
            ),
        )

        self.save_package(package, language)
        # add the package to the index
        self.index.add_package(package.package.id, language)
        return package

    def flush_index(self) -> None:
        """Flushes the in-memory index to the index file."""
        self.index.save(self.root / INDEX_FILE)

    def add_repository(self, package_name: str, repository: Repository) -> None:
        """
        Adds a repository to a package.
        example:
             for this repo https://github.com/fastapi/full-stack-fastapi-template
            - add_repository("fastapi", Repository(owner="fastapi", repo="full-stack-fastapi-template"))
        """
        pkg_idx = self.index.get_package(package_name)
        if pkg_idx is None:
            raise ValueError(f"package not found: {package_name}")

        package = self.load_package(file_path=self.root / pkg_idx.path)
        
        for existing_repo in package.repositories:
            if existing_repo.owner.lower() == repository.owner.lower() and existing_repo.repo.lower() == repository.repo.lower():
                raise ValueError(f"Repository '{repository.owner}/{repository.repo}' already exists in package '{package_name}'.")
                
        package.repositories.append(repository)
        self.save_package(package, pkg_idx.language)

    def add_repositories(
        self, package_name: str, repositories: list[Repository]
    ) -> None:
        """
        Adds multiple repositories to a package.
        example:
            - add_repositories("fastapi", [Repository(owner="fastapi", repo="full-stack-fastapi-template"), ...])
        """
        pkg_idx = self.index.get_package(package_name)
        if pkg_idx is None:
            raise ValueError(f"package not found: {package_name}")

        package = self.load_package(file_path=self.root / pkg_idx.path)
        
        existing_keys = {(r.owner.lower(), r.repo.lower()) for r in package.repositories}
        for new_repo in repositories:
            key = (new_repo.owner.lower(), new_repo.repo.lower())
            if key in existing_keys:
                raise ValueError(f"Repository '{new_repo.owner}/{new_repo.repo}' already exists in package '{package_name}'.")
            existing_keys.add(key)
            package.repositories.append(new_repo)
            
        self.save_package(package, pkg_idx.language)
