package handlers

import (
	"net/http"

	"contactsAI/contacts/internal/config"

	"github.com/gin-contrib/sessions"
	"github.com/gin-gonic/gin"
	"github.com/markbates/goth/gothic"
)

func RegisterAuthRoutes(router *gin.RouterGroup, env *config.Env) {
	apiGroup := router.Group("/auth")

	apiGroup.GET("/login", login)
	apiGroup.GET("/callback", callback)
	apiGroup.GET("/logout", logout)
}

func login(c *gin.Context) {
	// Provider comes from query parameter: ?provider=openid-connect
	gothUser, err := gothic.CompleteUserAuth(c.Writer, c.Request)
	if err != nil {
		gothic.BeginAuthHandler(c.Writer, c.Request)
		return
	}
	c.JSON(http.StatusOK, gin.H{"user": gothUser})
}

func callback(c *gin.Context) {
	user, err := gothic.CompleteUserAuth(c.Writer, c.Request)
	if err != nil {
		c.JSON(http.StatusInternalServerError, NewErrorResponse(err.Error()))
		return
	}

	session := sessions.Default(c)

	// Store user data in session
	session.Set("user_id", user.UserID)
	session.Set("email", user.Email)
	session.Set("name", user.Name)
	session.Set("avatar", user.AvatarURL)
	session.Set("authenticated", true)

	if err := session.Save(); err != nil {
		c.JSON(http.StatusInternalServerError, NewErrorResponse("failed to save the session"))
		return
	}

	gothic.Logout(c.Writer, c.Request)

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"user": gin.H{
			"id":     user.UserID,
			"email":  user.Email,
			"name":   user.Name,
			"avatar": user.AvatarURL,
		},
	})
}

func logout(c *gin.Context) {
	session := sessions.Default(c)

	session.Clear()

	session.Options(sessions.Options{
		MaxAge: -1,
		Path:   "/",
	})

	if err := session.Save(); err != nil {
		c.JSON(http.StatusInternalServerError, NewErrorResponse("Failed to clear session"))
		return
	}

	gothic.Logout(c.Writer, c.Request)

	c.JSON(http.StatusOK, nil)
}
