nifty = open("Nifty50", "r")
contents = []

for x in nifty:
    x = "BSE:" + x
    contents.append(x)
nifty.close()
nifty = open("Nifty50", "w")

nifty.writelines(contents)
nifty.close()
