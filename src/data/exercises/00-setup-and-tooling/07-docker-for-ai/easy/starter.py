def run_args(image, volumes, ports, gpus=True):
    """Argument list for `docker run`. volumes/ports map host side -> container side."""
    args = ["docker", "run", "--rm"]
    if gpus:
        args += ["--gpus", "all"]
    # TODO: add "-v", "host:container" for each volume, then "-p", "host:container" for each port
    args.append(image)
    return args
