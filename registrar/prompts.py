from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, NumberValidator

from registrar.models.kind import Kind
from registrar.models.package import PackageType


def prompt_for_package_name(default: str) -> str:
    result = inquirer.text(
        message="enter package name:", default=default, validate=EmptyInputValidator()
    ).execute()
    return result


def prompt_for_language(default: str = "") -> str:
    result = inquirer.text(
        message="enter language:", default=default, validate=EmptyInputValidator()
    ).execute()

    return result


def prompt_for_package_type() -> PackageType:
    result = inquirer.select(
        message="select package type:",
        choices=[
            PackageType.unknown.value,
            PackageType.library.value,
            PackageType.package.value,
            PackageType.framework.value,
        ],
        default=PackageType.unknown.value,
    ).execute()

    return result


def prompt_for_multiple_values(msg: str) -> list[str]:
    result = inquirer.text(
        message=f"{msg} (comma-separated):",
    ).execute()
    return [t.strip() for t in result.split(",") if t.strip()]


def prompt_for_owner(default: str = "") -> str:
    result = inquirer.text(
        message="enter repository owner (e.g., 'fastapi'): ",
        default=default,
        validate=EmptyInputValidator(),
    ).execute()
    return result


def prompt_for_repo(default: str = "") -> str:
    result = inquirer.text(
        message="enter repository name: ",
        default=default,
        validate=EmptyInputValidator(),
    ).execute()
    return result


def prompt_for_kind() -> Kind:
    result = inquirer.select(
        message="select repository kind: ",
        choices=[
            Kind.unknown.value,
            Kind.template.value,
            Kind.starter.value,
            Kind.boilerplate.value,
        ],
        default=Kind.unknown.value,
    ).execute()
    return result


def prompt_for_yes_no(msg: str) -> bool:
    result = inquirer.confirm(message=msg).execute()
    return result


def prompt_for_int(msg: str) -> int:
    result = inquirer.text(
        message=msg,
        validate=NumberValidator(),
    ).execute()
    return int(result)


if __name__ == "__main__":
    some = prompt_for_int(msg="")
    print(f"some: {some}")
