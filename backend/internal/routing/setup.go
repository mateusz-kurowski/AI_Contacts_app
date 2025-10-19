package routing

import (
	"time"

	"contactsAI/contacts/internal/config"
	"contactsAI/contacts/internal/handlers"
	"contactsAI/contacts/internal/validation"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func SetupRouter(env *config.Env) *gin.Engine {
	router := gin.Default()
	setupCORS(router)
	apiGroup := router.Group("/api")
	handlers.RegisterContactsRoutes(apiGroup, env)
	validation.SetupValidation()
	return router
}

func setupCORS(router *gin.Engine) {
	config := cors.DefaultConfig()
	config.AllowOrigins = []string{"http://localhost:5173"}
	config.AllowMethods = []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"}
	config.AllowHeaders = []string{"Origin", "Content-Type", "Authorization"}
	config.AllowCredentials = true
	config.MaxAge = 12 * time.Hour

	router.Use(cors.New(config))
}
