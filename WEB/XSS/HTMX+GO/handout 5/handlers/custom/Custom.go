package custom

import (
	"github.com/gin-gonic/gin"
)

/*
REDACTED
*/
func Custom404Handler(c *gin.Context) {
	/*
	   REDACTED
	*/
	c.JSON(404, gin.H{"error": "Resource not found"})
}
