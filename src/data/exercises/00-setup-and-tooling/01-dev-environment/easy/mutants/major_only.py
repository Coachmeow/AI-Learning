def is_new_enough(version, minimum):
    return int(version.split(".")[0]) >= int(minimum.split(".")[0])
