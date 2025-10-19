package routing

import (
	"contactsAI/contacts/internal/config"
	"contactsAI/contacts/internal/handlers"
	"contactsAI/contacts/internal/validation"
	"github.com/gin-gonic/gin"
)

func SetupRouter(env *config.Env) *gin.Engine {
	router := gin.Default()

	apiGroup := router.Group("/api")

	handlers.RegisterContactsRoutes(apiGroup, env)
	validation.SetupValidation()
	return router
}
