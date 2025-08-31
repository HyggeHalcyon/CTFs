s = b"BCEz4u1q^Ru2Am0o8^lX^45wd/e5u^?;)^    ^`e1d08b82581bg86|"
decoded = ''.join(chr(ord(c) ^ 0x01) for c in s)
print(decoded)

# CBD{5t0p_St3@l1n9_mY_54ve.d4t_>:(_!!!!_ad0e19c93490cf97}