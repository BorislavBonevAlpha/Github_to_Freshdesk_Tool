
# Validating the number of arguments required to run the command
def validate_params_count(params: list[str], count: int) -> None:
    if len(params) != count:
        raise ValueError(
            f'Invalid number of arguments. Expected: {count}; received: {len(params)}.")')
