CREATE TABLE image_mappings(
    reference_number VARCHAR(32),
    brand VARCHAR(32),
    image_name VARCHAR(128),

    PRIMARY KEY (reference_number, brand),
    FOREIGN KEY (reference_number, brand) REFERENCES watch(reference_number, brand)
);

