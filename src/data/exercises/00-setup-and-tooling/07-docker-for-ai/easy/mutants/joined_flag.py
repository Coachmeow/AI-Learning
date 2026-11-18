def run_args(image, volumes, ports, gpus=True):
    args = ["docker", "run", "--rm"]
    if gpus:
        args += ["--gpus", "all"]
    for host, inside in volumes.items():
        args.append(f"-v {host}:{inside}")
    for host, inside in ports.items():
        args.append(f"-p {host}:{inside}")
    args.append(image)
    return args
