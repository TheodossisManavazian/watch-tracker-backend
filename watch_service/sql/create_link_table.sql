CREATE TABLE links(
    reference_number VARCHAR(32),
    brand VARCHAR(32),
    links JSONB,

    PRIMARY KEY (reference_number, brand),
    FOREIGN KEY (reference_number, brand) REFERENCES watch(reference_number, brand)
);

