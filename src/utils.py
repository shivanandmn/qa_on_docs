def separate_args(args, separator):
    args = {
        k.replace(f"{separator}_", ""): v
        for k, v in args.__dict__.items()
        if k.startswith(separator)
    }
    return args
