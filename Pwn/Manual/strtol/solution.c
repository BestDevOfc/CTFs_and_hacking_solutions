// bcs strtol tries to convert ex: "999" string to long integer, but RANDOM_STRING I just did: \\\\ = 0 which prints flag
  printf("%d\n", strtol(entry, NULL, 10));
  if ((entry_number = strtol(entry, NULL, 10)) == 0) {
    puts(flag);
    fseek(stdin, 0, SEEK_END);
    exit(0);
  }