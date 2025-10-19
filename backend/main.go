package main

import (
	"log"
	"os"

	"contactsAI/contacts/internal/config"
	"contactsAI/contacts/internal/routing"

	"github.com/joho/godotenv"
)

func main() {
	if os.Getenv("GIN_MODE") != "release" {
		if loadErr := godotenv.Load("./env/.env"); loadErr != nil {
			panic("Error loading .env file")
		}
	}

	env, connErr := config.NewEnv(os.Getenv("DB_URL"))
	if connErr != nil || env.Queries == nil {
		log.Fatalf("Failed to initialize database: %v", connErr)
	}

	router := routing.SetupRouter(env)
	// PORT is set via environment variable
	// Default to 8080 if not set
	if runErr := router.Run(); runErr != nil {
		log.Fatalf("Failed to start server: %v", runErr)
	}
}
