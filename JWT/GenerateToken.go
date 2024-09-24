package main

import (
	"fmt"
	"os"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var secretKey = []byte{}

func InitJWT() {
	key, err := os.ReadFile("jwt.secret")
	if err != nil {
		panic(err)
	}
	secretKey = key[:]
}

func GenerateAccessToken(username string, role string) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256,
		jwt.MapClaims{
			"username": username,
			"exp":      time.Now().Add(time.Minute * 10).Unix(),
			"role":     role,
			"iat":      time.Now().Unix(),
		})

	signedToken, err := token.SignedString(secretKey)
	if err != nil {
		signedToken = ""
	}
	return signedToken, err
}

func main() {
	InitJWT()
	token, err := GenerateAccessToken("lol", "admin")
	if err != nil {
		fmt.Println("Error generating token:", err)
		return
	}
	fmt.Println("Generated Token:", token)
}
