
CREATE TABLE public.watch (
    reference_number character varying(32) NOT NULL,
    brand character varying(32) NOT NULL,
    model character varying(128) DEFAULT ''::character varying,
    description text DEFAULT ''::text,
    updated_at timestamp without time zone NOT NULL,
    nickname character varying(128) DEFAULT ''::character varying,
    caliber character varying(32) DEFAULT ''::character varying,
    case_info jsonb DEFAULT '{}'::jsonb,
    bracelet_info jsonb DEFAULT '{}'::jsonb,
    years_produced character varying(32) DEFAULT ''::character varying,
    pricing jsonb DEFAULT '{}'::jsonb,
    dial character varying(32) DEFAULT ''::character varying
);


ALTER TABLE watch ADD CONSTRAINT watch_pkey PRIMARY KEY (reference_number, brand);
ALTER TABLE watch ADD CONSTRAINT fk_caliber FOREIGN KEY (caliber, brand) REFERENCES public.caliber(caliber, brand);

CREATE  FUNCTION updated_watch()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER updated_watch_updated_at
    BEFORE UPDATE
    ON
        watch
    FOR EACH ROW
EXECUTE PROCEDURE updated_watch();

CREATE TRIGGER inserted_watch_updated_at
    BEFORE INSERT
    ON
        watch
    FOR EACH ROW
EXECUTE PROCEDURE updated_watch();