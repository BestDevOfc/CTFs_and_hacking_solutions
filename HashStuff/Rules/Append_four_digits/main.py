numbers = range(0, 10_000)

def pad_zeroes(number):
    number = f"{number}"
    padding_to_add = 0
    if len(number) != 4:
        padding_to_add = 4-len(number)
    number = '0' * padding_to_add+ f"{number}"
    return number

def convert_to_rule(data):
    final_rule = ''
    for character in data:
        final_rule += f"${character} "
    return final_rule


if __name__ == "__main__":
    custom_rule = open("custom_rule.rule", 'w')
    for num in numbers:
        rule = convert_to_rule('SKY-BTST-'+pad_zeroes(num))
        custom_rule.write(f"{rule}\n")
        print(rule)
    custom_rule.close()
        