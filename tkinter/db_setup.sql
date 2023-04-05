CREATE TABLE ProductStock(Name LONGTEXT NOT NULL, Code INT NOT NULL PRIMARY KEY, Count INT NOT NULL, UNIQUE INDEX Code_idx (Code ASC) VISIBLE);

CREATE TABLE ComponentStock(Name LONGTEXT NOT NULL, Code INT NOT NULL PRIMARY KEY, Count INT NOT NULL, UNIQUE INDEX Code_idx (Code ASC) VISIBLE);

CREATE TABLE ComponentStockStateCount(`Code` INT NOT NULL, 
`in-stock Count` INT NOT NULL, 
`Rejected Count` INT NOT NULL, 
`Lost Count` INT NOT NULL, 
`Defective Count` INT NOT NULL, 
CONSTRAINT `Code` FOREIGN KEY (`Code`) REFERENCES ComponentStock(Code) ON DELETE CASCADE ON UPDATE CASCADE, 
INDEX `Code_idx` (`Code` ASC) VISIBLE);


CREATE TABLE ComponentsPerProduct
(
`Product Code` INT NOT NULL, 
FOREIGN KEY (`Product Code`) REFERENCES ProductStock(Code) ON DELETE CASCADE ON UPDATE CASCADE, 

`Component Code` INT NOT NULL, 
FOREIGN KEY (`Component Code`) REFERENCES ComponentStock(Code) ON DELETE CASCADE ON UPDATE CASCADE, 

CodeCount INT NOT NULL
);



-- DROP TABLE ComponentStockStateCount;
-- DROP TABLE ComponentsPerProduct;
-- DROP TABLE ProductStock;
-- DROP TABLE ComponentStock;
