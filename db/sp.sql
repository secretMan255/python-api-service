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
    LEFT JOIN pnk.main_product MAIN ON PDT.id = MAIN.p_id
    SET PDT.status = p_status, ITM.status = p_status, MAIN.status = p_status
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
    
    DELETE FROM pnk.main_product MAIN WHERE MAIN.p_id = p_id; 
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

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_get_all_item` $$
CREATE PROCEDURE `sp_get_all_item`()
Main: BEGIN
	SELECT id, name, `describe`, price, qty, img, p_id AS parentId, shipping_fee, shippingFee, status, createAt AS createTime
    FROM pnk.items;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_update_item_detail` $$
CREATE PROCEDURE `sp_update_item_detail`(
	IN p_item_id INT,
    IN p_item_name VARCHAR(45),
    IN p_parent_id int,
    IN p_item_price DECIMAL(7, 2),
    IN p_qty INT,
    IN p_img VARCHAR(45)
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    IF p_item_id IS NULL THEN
		CALL pnk.sp_err('-1209', 'Invalid param');
        LEAVE Main;
    END IF;
    
    UPDATE pnk.items
    SET name = p_item_name, price = p_item_price, p_id = p_parent_id, qty = p_qty, img = p_img
    WHERE id = p_item_id;
    
    SELECT p_item_id, p_item_name, p_parent_id, p_item_price, p_qty, p_img;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_update_item_describe` $$
CREATE PROCEDURE `sp_update_item_describe`(
	IN p_item_id INT,
    IN p_describe VARCHAR(500)
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    IF p_item_id IS NULL THEN
		CALL pnk.sp_err('-1209', 'Invalid param');
        LEAVE Main;
    END IF;
    
    UPDATE pnk.items
    SET `describe` = p_describe
    WHERE id = p_item_id;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_update_item_status` $$
CREATE PROCEDURE `sp_update_item_status`(
	IN p_item_id INT,
    IN p_status INT
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    IF p_item_id IS NULL THEN
		CALL pnk.sp_err('-1209', 'Invalid param');
        LEAVE Main;
    END IF;
    
    UPDATE pnk.items
    SET status = p_status
    WHERE id = p_item_id;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_delete_item` $$
CREATE PROCEDURE `sp_delete_item`(
	IN p_item_id INT
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    IF p_item_id IS NULL THEN
		CALL pnk.sp_err('-1209', 'Invalid param');
        LEAVE Main;
    END IF;
    
    DELETE FROM pnk.items
    WHERE id = p_item_id;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_update_item_parent_id` $$
CREATE PROCEDURE `sp_update_item_parent_id`(
	IN p_origin_id INT,
    IN p_new_id INT
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    IF p_origin_id IS NULL THEN
		call sp_err('-1209', 'Invalid param');
        LEAVE Main;
    END IF;
    
    UPDATE pnk.items
    SET p_id = p_new_id
    WHERE p_id = p_origin_id;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_add_item` $$
CREATE PROCEDURE `sp_add_item`(
	IN p_item_name VARCHAR(45),
    IN p_parent_id INT,
    IN p_quantity INT,
    IN p_price DECIMAL(7, 2),
    IN p_image VARCHAR(45),
    IN p_describe VARCHAR(500)
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
	START TRANSACTION;
    
    IF p_item_name = '' OR p_price IS NULL OR p_quantity IS NULL OR p_parent_id IS NULL THEN
		CALL pnk.sp_err('-1209', 'Invalid param');
        LEAVE Main;
    END IF;
    
    INSERT INTO pnk.items(name, `describe`, price, qty, img, p_id, shipping_fee, status, createAt)
    VALUES (p_item_name, p_describe, p_price, p_quantity, p_image, p_parent_id, 0, 1, utc_timestamp());
    
    SELECT LAST_INSERT_ID() AS itemId;
    COMMIT;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_get_carousel` $$
CREATE PROCEDURE `sp_get_carousel`()
Main: BEGIN
	SELECT id, name, p_id AS parentId
    FROM pnk.image;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_update_carousel` $$
CREATE PROCEDURE `sp_update_carousel`(
	IN p_id INT,
	IN p_name VARCHAR(45),
    IN p_parent_id INT
)
    SQL SECURITY INVOKER
Main: BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;

	IF p_id IS NULL THEN
		CALL pnk.sp_err('-1209', 'Invalid param');
        LEAVE Main;
	END IF;
    
	UPDATE pnk.image
    SET name = p_name, p_id = p_parent_id
    WHERE id = p_id;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_add_carousel` $$
CREATE PROCEDURE `sp_add_carousel`(
	IN p_name VARCHAR(45),
    IN p_parentId INT
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
	START TRANSACTION;

	IF p_name IS NULL OR p_name = '' OR p_parentId IS NULL THEN
		CALL pnk.sp_err('-1209', 'Invalid param');
        LEAVE Main;
    END IF;
    
    INSERT INTO pnk.image (name, p_id, status)
    VALUE (p_name, p_parentID, 1);
    
    SELECT LAST_INSERT_ID() AS itemId;
    COMMIT;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_update_carousel_parent_id` $$
CREATE PROCEDURE `sp_update_carousel_parent_id`(
	IN p_origin_id INT,
    IN p_new_id INT
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    IF p_origin_id IS NULL OR p_new_id IS NULL THEN
		CALL pnk.sp_err('-1209', 'Invalid param');
        LEAVE Main;
    END IF;
    
	UPDATE pnk.image
    SET p_id = p_new_id
    WHERE p_id = p_origin_id;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_get_main_product` $$
CREATE PROCEDURE `sp_get_main_product`()
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    SELECT MAIN.id, MAIN.p_id AS parentId, PRO.name
    FROM pnk.main_product MAIN
    INNER JOIN pnk.products PRO ON MAIN.p_id = PRO.id
    WHERE PRO.status = 1;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_delete_main_product` $$
CREATE PROCEDURE `sp_delete_main_product`(
	IN p_id INT
)
    SQL SECURITY INVOKER
Main: BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;
    
    IF p_id IS NULL THEN
		CALL pnk.sp_err('-1209', 'Invalid param');
        LEAVE Main;
    END IF;
    
    DELETE FROM pnk.main_product
    WHERE id = p_id;
END Main $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_add_main_product` $$
CREATE PROCEDURE `sp_add_main_product`(
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

	INSERT INTO pnk.main_product (p_id, createAt, status)
    VALUES (p_id, utc_timestamp(), 1);
    
    SELECT LAST_INSERT_ID AS id;
    
    COMMIT;
END Main $$
DELIMITER ;