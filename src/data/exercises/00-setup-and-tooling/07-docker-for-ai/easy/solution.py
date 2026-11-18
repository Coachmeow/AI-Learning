def run_args(image, volumes, ports, gpus=True):
    """Argument list for `docker run`. volumes/ports map host side -> container side."""
    args = ["docker", "run", "--rm"]
    if gpus:
        args += ["--gpus", "all"]
    for host, inside in volumes.items():
        args += ["-v", f"{host}:{inside}"]
    for host, inside in ports.items():
        args += ["-p", f"{host}:{inside}"]
    args.append(image)
    return args
