-- execute immediate from 'steps/01_setup_stages.sql' using (environment => '{{environment}}');
execute immediate from 'steps/01_setup_raws.sql' using (environment => '{{environment}}');