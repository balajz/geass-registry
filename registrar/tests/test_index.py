import pytest
from pathlib import Path

from registrar.registry.index import Index


@pytest.fixture
def empty_index():
    return Index()


def test_add_package(empty_index):
    empty_index.add_package("fastapi", "python")
    
    # Check if package is in languages
    packages = empty_index.get_language_packages("python")
    assert "fastapi" in packages
    assert len(packages) == 1
    
    # Check if package can be fetched directly
    pkg = empty_index.get_package("fastapi")
    assert pkg is not None
    assert pkg.language == "python"
    # Note: path is constructed as language/name.yaml in add_package
    assert pkg.path == "python/fastapi.yaml"


def test_add_duplicate_package(empty_index):
    empty_index.add_package("fastapi", "python")
    empty_index.add_package("fastapi", "python")
    
    # Check that it wasn't added twice to languages
    packages = empty_index.get_language_packages("python")
    assert len(packages) == 1
    
    # Check another language just in case
    empty_index.add_package("fastapi", "go")  # The method has an early return if name exists
    # Wait, the current implementation checks `if name in self.packages: return`
    # So the second call with a different language will also be ignored.
    packages_go = empty_index.get_language_packages("go")
    assert len(packages_go) == 0


def test_get_non_existent_package(empty_index):
    assert empty_index.get_package("non-existent") is None
    assert empty_index.get_language_packages("rust") == []


def test_save_and_load(tmp_path, empty_index):
    # Add some data
    empty_index.add_package("fastapi", "python")
    empty_index.add_package("gin", "go")
    
    index_file = tmp_path / "index.yaml"
    
    # Save to temp file
    empty_index.save(str(index_file))
    
    # Load from temp file
    loaded_index = Index.load(index_file)
    
    assert "fastapi" in loaded_index.get_language_packages("python")
    assert "gin" in loaded_index.get_language_packages("go")
    
    pkg = loaded_index.get_package("fastapi")
    assert pkg.language == "python"
    assert pkg.path == "python/fastapi.yaml"


def test_load_empty_file(tmp_path):
    index_file = tmp_path / "empty.yaml"
    index_file.write_text("")
    
    loaded_index = Index.load(index_file)
    assert len(loaded_index.languages) == 0
    assert len(loaded_index.packages) == 0
