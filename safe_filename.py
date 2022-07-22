def mod(x):
    x = x.replace ("  ", "_", 1)
    x = x.replace("   ", "_", 1)
    x = x.replace(" - ", "-", 1)
    x = x.replace(" ", "_")
    x = x.replace("/", "")
    x = x.replace("+", "")
    x = x.replace("ダ", "")
    x = x.replace(")", "")
    x = x.replace("(", "")
    x = x.replace("!", "")
    x = x.replace("|", "")
    return x
