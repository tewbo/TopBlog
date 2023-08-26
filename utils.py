import sys


def levenshtein(str1, str2, add_cost = 1, remove_cost = 1, change_cost = 1):
    dp = [add_cost * j for j in range(len(str2) + 1)]
    for i1 in range(1, len(str1) + 1):
        dp2 = [remove_cost * i1] * (len(str2) + 1)
        for i2 in range(1, len(str2) + 1):
            dp2[i2] = min(dp2[i2 - 1] + add_cost,
                          dp[i2] + add_cost,
                          dp[i2 - 1] + (change_cost if str1[i1 - 1] != str2[i2 - 1] else 0))
        dp = dp2
    return dp[len(str2)]


def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def is_number(s):
    try:
        int(s)
    except ValueError:
        return False
    return True
