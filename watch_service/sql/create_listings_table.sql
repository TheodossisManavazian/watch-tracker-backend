create table listings(
    hash_id CHAR(64),
    listing_code varchar(64),
    listing_url text,
    reference_number varchar(32),
    brand VARCHAR(32),
    model varchar(32),
    dial varchar(32),
    year varchar(4),
    condition varchar(32),
    accessories varchar(128),
    location varchar(128),
    price_usd NUMERIC(10, 2),
    original_price NUMERIC(10, 2),
    original_currency varchar(32),
    exchange_rate NUMERIC(10, 6),
    updated_at TIMESTAMP not NULL,

    PRIMARY KEY(hash_id)
);


CREATE  FUNCTION updated_listing()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';


CREATE TRIGGER inserted_listing_updated_at
    BEFORE INSERT
    ON
        listings
    FOR EACH ROW
EXECUTE PROCEDURE updated_listing();

CREATE TRIGGER updated_listing_update_at
    BEFORE UPDATE
    ON
        listings
    FOR EACH ROW
EXECUTE PROCEDURE updated_listing();