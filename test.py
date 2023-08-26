import os

import dzen

f = open("in.in")
for l in f.readlines():
    expect, file = l.strip().split(" ")
    try:
        got = dzen.do_main(None, f"../zn/images/{file}")
    except:
        got = "Error"
    print(file, expect, got, expect == str(got))