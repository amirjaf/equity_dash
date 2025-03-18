CREATE OR REPLACE FUNCTION import_tour_table(filepath TEXT, tablename TEXT, schemaname TEXT)
RETURNS VOID AS $$
BEGIN
    RAISE NOTICE 'Filepath: %, Schema: %, Table: %', filepath, schemaname, tablename;
    
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_schema = schemaname AND table_name = tablename
    ) THEN
        RAISE NOTICE 'Table % does not exist, creating it...', tablename;

        EXECUTE format('
            CREATE TABLE %I.%I (
                race FLOAT, 
                tourmode FLOAT,
                psexpfac FLOAT,
                pdpurp2 FLOAT,
                pdpurp FLOAT,
                ocounty FLOAT,
                hisp_b FLOAT,
                lowinc FLOAT,
                distcat FLOAT,
                tautodist FLOAT,
                tourmode2 FLOAT,
                timecat2 FLOAT,
                ttravtime FLOAT,
                timecat_smooth FLOAT
            )', schemaname, tablename);

         -- Create index
        RAISE NOTICE 'Creating composite index on (pdpurp2, ocounty, tourmode2, lowinc, hisp_b, race)...';
        EXECUTE format('
            CREATE INDEX idx_%I_composite 
            ON %I.%I (pdpurp2, ocounty, tourmode2, lowinc, hisp_b, race)',
            tablename, schemaname, tablename);

        RAISE NOTICE 'Composite index created successfully.';
        
        -- Import CSV data
        RAISE NOTICE 'Importing CSV data from file: % into table %', filepath, tablename;
        EXECUTE format('COPY %I.%I FROM %L WITH CSV HEADER', schemaname, tablename, filepath);

        RAISE NOTICE 'Data import completed successfully for table %', tablename;
    ELSE
        RAISE NOTICE 'Table % already exists, no action taken.', tablename;
    END IF;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION import_trip_table(filepath TEXT, tablename TEXT, schemaname TEXT)
RETURNS VOID AS $$
BEGIN
    RAISE NOTICE 'Filepath: %, Schema: %, Table: %', filepath, schemaname, tablename;
    
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_schema = schemaname AND table_name = tablename
    ) THEN
        RAISE NOTICE 'Table % does not exist, creating it...', tablename;

        EXECUTE format('
            CREATE TABLE %I.%I (
                race FLOAT, 
                tripmode FLOAT,
                psexpfac FLOAT,
                dpurp2 FLOAT,
                dpurp FLOAT,
                ocounty FLOAT,
                hisp_b FLOAT,
                lowinc FLOAT,
                distcat FLOAT,
                travdist FLOAT,
                tripmode2 FLOAT,
                timecat2 FLOAT,
                ttravtime FLOAT,
                timecat_smooth FLOAT
            )', schemaname, tablename);

        -- Create index
        RAISE NOTICE 'Creating composite index on (dpurp2, ocounty, tripmode2, lowinc, hisp_b, race)...';
        EXECUTE format('
            CREATE INDEX idx_%I_composite 
            ON %I.%I (dpurp2, ocounty, tripmode2, lowinc, hisp_b, race)',
            tablename, schemaname, tablename);

        RAISE NOTICE 'Composite index created successfully.';

        -- Import CSV data
        RAISE NOTICE 'Importing CSV data from file: % into table %', filepath, tablename;
        EXECUTE format('COPY %I.%I FROM %L WITH CSV HEADER', schemaname, tablename, filepath);

        RAISE NOTICE 'Data import completed successfully for table %', tablename;
    ELSE
        RAISE NOTICE 'Table % already exists, no action taken.', tablename;
    END IF;
END;
$$ LANGUAGE plpgsql;


