// Made by Christian Oliveros ( oliveroschristian.wordpress.com )
// Last edit 02/12/2017


// Get Document name from filepath
// filePath : filepath
function getDocumentName(filePath){
	return filePath.split('\\').pop().split('/').pop();
}