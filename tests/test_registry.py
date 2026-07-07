import pytest
from pathlib import Path

from registrar.registry.registry import Registry
from registrar.registry.index import Index
from registrar.models.package import PackageType, Repository, Kind


@pytest.fixture
def temp_registry(tmp_path):
    # Initialize an empty index file so Registry.__init__ can load it
    index_file = tmp_path / "index.yaml"
    Index().save(str(index_file))
    
    return Registry(str(tmp_path))


def test_add_package(temp_registry):
    pkg = temp_registry.add_package(
        id="fastapi",
        name="fastapi",
        language="python",
        type=PackageType.framework,
        aliases=["fapi"],
        tags=["web", "api"]
    )
    
    assert pkg is not None
    assert pkg.package.name == "fastapi"
    assert pkg.package.language == "python"
    
    # Check if directory and file were created
    pkg_file = temp_registry.root / "python" / "fastapi.yaml"
    assert pkg_file.exists()
    
    # Check if package is in the in-memory index
    assert "fastapi" in temp_registry.index.get_language_packages("python")
    
    # Index file on disk should NOT have it yet since we removed inline save
    disk_index = Index.load(temp_registry.root / "index.yaml")
    assert "fastapi" not in disk_index.get_language_packages("python")


def test_flush_index(temp_registry):
    temp_registry.add_package(
        id="gin",
        name="gin",
        language="go",
        type=PackageType.framework
    )
    temp_registry.flush_index()
    
    # Now it should be on disk
    disk_index = Index.load(temp_registry.root / "index.yaml")
    assert "gin" in disk_index.get_language_packages("go")


def test_load_package_by_name(temp_registry):
    temp_registry.add_package("flask", "flask", "python", PackageType.framework)
    
    loaded_pkg = temp_registry.load_package(language="python", name="flask")
    assert loaded_pkg.package.name == "flask"


def test_load_package_by_path(temp_registry):
    pkg = temp_registry.add_package("flask", "flask", "python", PackageType.framework)
    
    # Direct path
    path = temp_registry.root / "python" / "flask.yaml"
    loaded_pkg = temp_registry.load_package(file_path=path)
    
    assert loaded_pkg.package.name == "flask"


def test_load_package_not_found(temp_registry):
    with pytest.raises(FileNotFoundError):
        temp_registry.load_package(language="python", name="missing")


def test_load_package_invalid_args(temp_registry):
    with pytest.raises(ValueError):
        temp_registry.load_package(language="python")  # Missing name


def test_add_repository(temp_registry):
    temp_registry.add_package("react", "react", "javascript", PackageType.library)
    
    repo = Repository(owner="facebook", repo="react")
    temp_registry.add_repository("react", repo)
    
    # Load back to check
    pkg = temp_registry.load_package(language="javascript", name="react")
    assert len(pkg.repositories) == 1
    assert pkg.repositories[0].owner == "facebook"
    assert pkg.repositories[0].repo == "react"


def test_add_repository_not_found(temp_registry):
    repo = Repository(owner="facebook", repo="react")
    with pytest.raises(ValueError):
        temp_registry.add_repository("react", repo)


def test_add_repositories(temp_registry):
    temp_registry.add_package("vue", "vue", "javascript", PackageType.framework)
    
    repos = [
        Repository(owner="vuejs", repo="vue"),
        Repository(owner="vuejs", repo="vue-router")
    ]
    
    temp_registry.add_repositories("vue", repos)
    
    pkg = temp_registry.load_package(language="javascript", name="vue")
    assert len(pkg.repositories) == 2
    assert pkg.repositories[0].repo == "vue"
    assert pkg.repositories[1].repo == "vue-router"
