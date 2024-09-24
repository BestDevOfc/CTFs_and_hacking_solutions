data = open("subclasses.txt", 'r').read().split('<class ')

# input(data[101])

index = 0
for element in data:
    if r'''flask.helpers._PackageBoundObject''' in element:
        print(index)
    index += 1