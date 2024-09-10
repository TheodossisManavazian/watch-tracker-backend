CREATE TABLE links(
    reference_number VARCHAR(32),
    brand VARCHAR(32),
    watch_link TEXT,
    image_link TEXT,
    links JSONB,

    PRIMARY KEY (reference_number, brand),
    FOREIGN KEY (reference_number, brand) REFERENCES watch(reference_number, brand)
);
