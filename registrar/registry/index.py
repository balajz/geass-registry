from pathlib import Path
from typing import Dict

import yaml
from pydantic import BaseModel, Field


class PackageIdx(BaseModel):
    language: str
    path: str


class Index(BaseModel):
    languages: Dict[str, list[str]] = Field(default_factory=dict)
    packages: Dict[str, PackageIdx] = Field(default_factory=dict)

    @classmethod
    def load(cls, path: str | Path) -> "Index":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return cls.model_validate(data)

    def save(self, path: str | Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                self.model_dump(),
                f,
                sort_keys=False,
                allow_unicode=True,
            )

    def add_package(self, name: str, language: str) -> None:
        if name in self.packages:
            return

        path = str(Path(language, name).with_suffix(".yaml"))
        self.packages[name] = PackageIdx(language=language, path=path)

        if language in self.languages:
            self.languages[language].append(name)
        else:
            self.languages[language] = [name]

    def get_language_packages(self, language: str) -> list[str]:
        return self.languages.get(language, [])

    def get_package(self, name: str) -> PackageIdx | None:
        return self.packages.get(name)
