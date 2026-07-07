from enum import Enum

from pydantic import BaseModel, Field

from .kind import Kind


class PackageType(str, Enum):
    unknown = "unknown"
    framework = "framework"
    library = "library"
    package = "package"


class PackageDetails(BaseModel):
    id: str
    name: str
    language: str
    type: PackageType = PackageType.unknown


class PackageMetaData(BaseModel):
    aliases: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class Repository(BaseModel):
    owner: str
    repo: str
    kind: Kind = Kind.unknown
    stack: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    official: bool = False
    priority: int = 50
    notes: str = ""


class Package(BaseModel):
    version: int = 1
    package: PackageDetails
    metadata: PackageMetaData
    repositories: list[Repository] = Field(default_factory=list)
