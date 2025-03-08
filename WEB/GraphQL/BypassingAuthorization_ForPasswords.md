https://www.hackerone.com/blog/how-graphql-bug-resulted-authentication-bypass
```
{
  __schema {
    types {
      name
      fields {
        name
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
      }
    }
  }
}
```

**Another one:**
```
# Welcome to GraphiQL
#
# GraphiQL is an in-browser tool for writing, validating, and
# testing GraphQL queries.
#
# Type queries into this side of the screen, and you will see intelligent
# typeaheads aware of the current GraphQL type schema and live syntax and
# validation errors highlighted within the text.
#
# GraphQL queries typically start with a "{" character. Lines that starts
# with a # are ignored.
#
# An example GraphQL query might look like:
#
#     {
#       field(arg: "value") {
#         subField
#       }
#     }
#
# Keyboard shortcuts:
#
#  Prettify Query:  Shift-Ctrl-P (or press the prettify button above)
#
#     Merge Query:  Shift-Ctrl-M (or press the merge button above)
#
#       Run Query:  Ctrl-Enter (or press the play button above)
#
#   Auto Complete:  Ctrl-Space (or just start typing)
#


{
  __schema {
    queryType {
      name
    }
    mutationType {
      name
    }
    subscriptionType {
      name
    }
    types {
      kind
      name
      description
      fields(includeDeprecated: true) {
        name
        description
        args {
          name
          description
          type {
            kind
            name
            ofType {
              kind
              name
            }
          }
          defaultValue
        }
        type {
          kind
          name
          ofType {
            kind
            name
          }
        }
        isDeprecated
        deprecationReason
      }
      inputFields {
        name
        description
        type {
          kind
          name
          ofType {
            kind
            name
          }
        }
        defaultValue
      }
      interfaces {
        kind
        name
      }
      enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        kind
        name
      }
    }
    directives {
      name
      description
      locations
      args {
        name
        description
        type {
          kind
          name
          ofType {
            kind
            name
          }
        }
        defaultValue
      }
    }
  }
}

```

<img width="933" alt="Screenshot 2025-01-24 at 8 39 11 PM" src="https://github.com/user-attachments/assets/f3abd4bf-2a19-4c6f-9fe6-aaa0d231dbdd" />
<img width="653" alt="Screenshot 2025-01-24 at 8 39 24 PM" src="https://github.com/user-attachments/assets/519fce34-474e-4c86-a114-dba23bf79157" />
<img width="638" alt="Screenshot 2025-01-24 at 8 39 36 PM" src="https://github.com/user-attachments/assets/6bacc61f-5909-4523-8bda-b9d6c3d65075" />
<img width="579" alt="Screenshot 2025-01-24 at 8 39 52 PM" src="https://github.com/user-attachments/assets/9706a922-a863-4273-a661-9f1ee007274f" />
<img width="570" alt="Screenshot 2025-01-24 at 8 40 09 PM" src="https://github.com/user-attachments/assets/03437e0c-df95-4a88-8638-44e81375eb97" />
<img width="852" alt="Screenshot 2025-01-24 at 9 02 41 PM" src="https://github.com/user-attachments/assets/b54cdb83-c15b-4267-8887-87dc37932e2c" />

