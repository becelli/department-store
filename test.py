for i in range(3):
    print(i)


iterator = iter(range(3))
while True:
    try:
        print(next(iterator))
    except StopIteration:
        break
