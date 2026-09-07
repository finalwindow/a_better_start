#!/usr/bin/env python3
import random, math, sys
from typing import List, Tuple

def is_prime(n: int) -> bool:
    if n < 2: return False
    small = [2,3,5,7,11,13,17,19,23,29,31,37]
    for p in small:
        if n % p == 0:
            return n == p
    d = n - 1; r = 0
    while d % 2 == 0:
        d //= 2; r += 1
    for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022]:
        if a % n == 0: continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True

def pollard_rho(n: int) -> int:
    # 修复: 限制最大迭代次数，防止偶发死循环（关联 Issue #编号）
    MAX_ITER = 10000
    iter_count = 0
    
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3
    
    while True:
        # 每次重新随机，避免同样参数反复进入死循环
        c = random.randrange(1, n - 1)
        x = random.randrange(0, n - 1)
        y = x
        d = 1
        iter_count = 0
        
        while d == 1:
            if iter_count > MAX_ITER:
                break  # 超过最大迭代，跳出内层循环，外层重试
            x = (pow(x, 2, n) + c) % n
            y = (pow(y, 2, n) + c) % n
            y = (pow(y, 2, n) + c) % n
            d = math.gcd(abs(x - y), n)
            iter_count += 1
            if d == n:
                break
        if d != n and d != 1:
            return d
        
def pollard_rho(n: int) -> int:
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3
    while True:
        c = random.randrange(1, n - 1)
        x = random.randrange(0, n - 1)
        y = x; d = 1
        while d == 1:
            x = (pow(x, 2, n) + c) % n
            y = (pow(y, 2, n) + c) % n
            y = (pow(y, 2, n) + c) % n
            d = math.gcd(abs(x - y), n)
            if d == n: break
        if d != n: return d

def factor_recursive(n: int, res: List[int]) -> None:
    if n == 1: return
    if is_prime(n):
        res.append(n); return
    d = pollard_rho(n)
    while d == n or d == 1 or n % d != 0:
        d = pollard_rho(n)
    factor_recursive(d, res)
    factor_recursive(n // d, res)

def factorize(n: int) -> List[Tuple[int, int]]:
    if n < 2: return []
    if is_prime(n): return [(n, 1)]
    raw = []
    factor_recursive(n, raw)
    raw.sort()
    merged = []
    for p in raw:
        if merged and merged[-1][0] == p:
            merged[-1] = (p, merged[-1][1] + 1)
        else:
            merged.append((p, 1))
    return merged

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python factorize.py <整数>")
        sys.exit(1)
    num = int(sys.argv[1])
    if num < 2:
        print("请输入大于1的整数")
        sys.exit(0)
    print(f"分解: {num}")
    factors = factorize(num)
    parts = [f"{p}^{e}" if e > 1 else str(p) for p, e in factors]
    print(" = ".join([str(num), " * ".join(parts)]))