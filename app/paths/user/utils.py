def hasErrors(errors):
    count = 0
    for error in errors:
        count += len(errors[error])
    return count != 0
