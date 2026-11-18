def run_args(image, volumes, ports, gpus=True):
    args = ["docker", "run", "--rm"]
    if gpus:
        args += ["--gpus", "all"]
    for host, inside in volumes.items():
        args += ["-v", f"{inside}:{host}"]
    for host, inside in ports.items():
        args += ["-p", f"{inside}:{host}"]
    args.append(image)
    return args
