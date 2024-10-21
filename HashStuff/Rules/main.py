# appends 2 digits + all possible special characters (not their permutations)


rules_file = open(f"append_2_numbers_special_character_exclamation.rule", 'w')
special_chars = r'''~!@#$%^&*()_+-=[]\{}|;':"<>?,./`'''
for number in range(0, 100):
    num = str(number)
    if len(num) == 1:
        num = f"0{num}"
    
    # Append rule:
    for special_char in special_chars:
        rule = f"{num}{special_char}"
        final_rule = ''
        for char in rule:
            final_rule += f"${char} "
        print(final_rule)
        rules_file.write(f"{final_rule}\n")
rules_file.close()