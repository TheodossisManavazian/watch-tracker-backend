CREATE TABLE caliber(
    caliber varchar(32),
    brand varchar(32),
    movement varchar(32),
    power_reserve varchar(32),
    qty_jewels varchar(3),
    frequency varchar(32),

    PRIMARY KEY (caliber, brand)
);