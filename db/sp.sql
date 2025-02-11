DELIMITER $$
DROP PROCEDURE IF EXISTS 'sp_admin_login' $$
CREATE PROCEDURE `sp_admin_login`(
	IN p_username VARCHAR(45)
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
	IF p_username IS NULL OR p_username = '' THEN
		CALL pnk.sp_err('-1309', 'Invalid username');
		LEAVE Main;
     END IF;
		
	SELECT id, password
     FROM admin.user
     WHERE username = p_username;
        
END Main $$
DELIMITER ;

DELIMTIER $$
DROP PROCEDURE IF EXISTS 'sp_update_admin_last_login' $$
CREATE PROCEDURE `sp_update_admin_last_login`(
	IN p_username VARCHAR(45)
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
	IF p_username IS NULL OR p_username = '' THEN
		CALL pnk.sp_err('-1309', 'Invalid username');
		LEAVE Main;
    END IF;
    
	UPDATE admin.user
    SET lastLoginAt = utc_timestamp()
    WHERE username = p_username;
END Main $$
DELIMITER ;