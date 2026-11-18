def run_args(image, volumes, ports, gpus=True):
    args = ["docker", "run", "--rm"]
    if gpus:
        args += ["--gpus", "all"]
    args.append(image)
    for host, inside in volumes.items():
        args += ["-v", f"{host}:{inside}"]
    for host, inside in ports.items():
        args += ["-p", f"{host}:{inside}"]
    return args
