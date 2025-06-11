liczba_t = int(input())
for i in range(liczba_t):
    v1,v2 = map(int,input().split())
    print(int(2*v1*v2/(v1 + v2)))
