DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_admin_login` $$
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
DROP PROCEDURE IF EXISTS `sp_update_admin_last_login` $$
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

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_get_all_product` $$
CREATE PROCEDURE `sp_get_all_product`()
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    SELECT PDT.id, PDT.name, COALESCE(CAST(PDT.p_id AS CHAR), '0') AS parentId, PDT.icon, PDT.describe, PDT.status, PDT.createAt AS createTime
    FROM pnk.products PDT;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_update_product_describe` $$
CREATE PROCEDURE `sp_update_product_describe`(
	IN p_product_id INT,
    IN p_describe TEXT
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    IF p_product_id IS NULL OR p_product_id = '' THEN
		CALL pnk.sp_err('-1209', 'Invalid params');
        LEAVE Main;
    END IF;
    
    UPDATE pnk.products PDT
    SET PDT.describe = CAST(p_describe AS CHAR)
    WHERE PDT.id = p_product_id;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_update_product_detail` $$
CREATE PROCEDURE `sp_update_product_detail`(
	IN p_product_id INT,
    IN p_name VARCHAR(70),
    IN p_parent_id INT,
    IN p_icon VARCHAR(45)
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
	IF p_product_id IS NULL OR p_product_id = '' THEN
		CALL pnk.sp_err('-1209', 'Invalid param');
        LEAVE MAIN;
    END IF;
	
    UPDATE pnk.products
    SET name = p_name, p_id = p_parent_id, icon = p_icon
    WHERE id = p_product_id;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_update_product_status` $$
CREATE PROCEDURE `sp_update_product_status`(
	IN p_product_id INT,
    IN p_status INT
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    IF p_product_id IS NULL OR p_product_id = '' THEN
		CALL pnk.sp_err('-1209', 'Invalid params');
    END IF;
    
    UPDATE pnk.products PDT
    LEFT JOIN pnk.items ITM ON PDT.id = ITM.p_id
    SET PDT.status = p_status, ITM.status = p_status
    WHERE PDT.id = p_product_id OR PDT.p_id = p_product_id;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_delete_product` $$
CREATE PROCEDURE `sp_delete_product`(
	IN p_id INT
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
	
    START TRANSACTION;
    
    IF p_id IS NULL THEN
		CALL pnk.sp_err('-1209', 'Invalid param');
        LEAVE Main;
    END IF;
    
    UPDATE pnk.products PDT
	LEFT JOIN pnk.items ITM ON PDT.id = ITM.p_id
    SET PDT.status = 0, ITM.status = 0
    WHERE PDT.p_id = p_id OR ITM.p_id = p_id;
    
    DELETE FROM pnk.products WHERE id = p_id;
    
    COMMIT;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_add_product` $$
CREATE PROCEDURE `sp_add_product`(
	IN p_product_name VARCHAR(70),
    IN p_parent_id INT,
    IN p_icon VARCHAR(45),
    IN p_describe VARCHAR(500)
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    START TRANSACTION;
    
    -- frontend handle duplicate product insert
    INSERT INTO pnk.products(name, p_id, icon, `describe`, status, createAt)
    VALUES (p_product_name, p_parent_id, p_icon, p_describe, 1, utc_timestamp());
    
    SELECT LAST_INSERT_ID() AS productId;
    COMMIT;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_update_product_parent_id` $$
CREATE PROCEDURE `sp_update_prodcut_parent_id`(
	IN p_original_parent_id INT,
    IN p_new_parent_id INT
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    UPDATE pnk.products
    SET p_id = p_new_parent_id
    WHERE p_id = p_original_parent_id;
END Main $$
DELIMITER ;