https://www.hackerone.com/blog/how-graphql-bug-resulted-authentication-bypass

**Another one:**
- from GQL Voyager
```

    query IntrospectionQuery {
      __schema {
        
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
          ...FullType
        }
        directives {
          name
          description
          
          locations
          args {
            ...InputValue
          }
        }
      }
    }

    fragment FullType on __Type {
      kind
      name
      description
      
      
      fields(includeDeprecated: true) {
        name
        description
        args {
          ...InputValue
        }
        type {
          ...TypeRef
        }
        isDeprecated
        deprecationReason
      }
      inputFields {
        ...InputValue
      }
      interfaces {
        ...TypeRef
      }
      enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        ...TypeRef
      }
    }

    fragment InputValue on __InputValue {
      name
      description
      type { ...TypeRef }
      defaultValue
      
      
    }

    fragment TypeRef on __Type {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                    ofType {
                      kind
                      name
                      ofType {
                        kind
                        name
                      }
                    }
                  }
                }
              }
            }
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

