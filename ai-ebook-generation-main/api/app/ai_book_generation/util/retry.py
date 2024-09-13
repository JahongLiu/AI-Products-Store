def retry(max_retries):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempt_i = 0
            while attempt_i < max_retries:
                try:
                    # Increment attempt counter
                    attempt_i += 1
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"An exception occurred: {e}")
                    print(f"Attempt {attempt_i} of {max_retries}. Retrying...")
            else:
                raise Exception(f"Max retries of function {func} exceeded")

        return wrapper

    return decorator
