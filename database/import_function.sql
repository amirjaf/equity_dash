CREATE OR REPLACE FUNCTION import_tour_table(filepath TEXT, tablename TEXT, schemaname TEXT)
RETURNS VOID AS $$
DECLARE
    column_count INT;
BEGIN
    -- Debug: Log filepath and tablename
    RAISE NOTICE 'Filepath: %, Table: %', filepath, tablename;
    
    -- Check if the table exists
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_schema = schemaname AND table_name = tablename
    ) THEN
        -- Debug: Table creation log
        RAISE NOTICE 'Table % does not exist, creating it...', tablename;

        -- Dynamically create the table if it doesn't exist
        EXECUTE format('
            CREATE TABLE equity.%I (
                RACE FLOAT, 
                tourmode FLOAT,
                psexpfac FLOAT,
                pdpurp2 FLOAT,
                pdpurp FLOAT,
                ocounty FLOAT,
                HISP_B FLOAT,
                lowinc FLOAT,
                distcat FLOAT,
                tautodist FLOAT,
                tourmode2 FLOAT,
                timecat2 FLOAT,
                ttravtime FLOAT
            )', tablename);

        -- Debug: Log CSV import action
        RAISE NOTICE 'Importing CSV data from file: % into table %', filepath, tablename;

        -- Import CSV data
        EXECUTE format('COPY equity.%I FROM %L WITH CSV HEADER', tablename, filepath);

        -- Debug: Successful completion log
        RAISE NOTICE 'Data import completed successfully for table %', tablename;
    ELSE
        -- Debug: Table already exists, no action taken
        RAISE NOTICE 'Table % already exists, no action taken.', tablename;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION import_trip_table(filepath TEXT, tablename TEXT, schemaname TEXT)
RETURNS VOID AS $$
DECLARE
    column_count INT;
BEGIN
    -- Debug: Log filepath and tablename
    RAISE NOTICE 'Filepath: %, Table: %', filepath, tablename;
    
    -- Check if the table exists
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_schema = schemaname AND table_name = tablename
    ) THEN
        -- Debug: Table creation log
        RAISE NOTICE 'Table % does not exist, creating it...', tablename;

        -- Dynamically create the table if it doesn't exist
        EXECUTE format('
            CREATE TABLE equity.%I (
                RACE FLOAT, 
                tripmode FLOAT,
                psexpfac FLOAT,
                dpurp2 FLOAT,
                dpurp FLOAT,
                ocounty FLOAT,
                HISP_B FLOAT,
                lowinc FLOAT,
                distcat FLOAT,
                travdist FLOAT,
                tripmode2 FLOAT,
                timecat2 FLOAT,
                ttravtime FLOAT
            )', tablename);

        -- Debug: Log CSV import action
        RAISE NOTICE 'Importing CSV data from file: % into table %', filepath, tablename;

        -- Import CSV data
        EXECUTE format('COPY equity.%I FROM %L WITH CSV HEADER', tablename, filepath);

        -- Debug: Successful completion log
        RAISE NOTICE 'Data import completed successfully for table %', tablename;
    ELSE
        -- Debug: Table already exists, no action taken
        RAISE NOTICE 'Table % already exists, no action taken.', tablename;
    END IF;
END;
$$ LANGUAGE plpgsql;

